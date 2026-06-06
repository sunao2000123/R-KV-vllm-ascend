#
# Copyright (c) 2026.
#
# R-KV cache compression helpers for vLLM-Ascend.
#

import math
import time
from collections.abc import Iterator
from contextlib import contextmanager

import torch
import torch.nn.functional as F
from vllm.logger import logger

from vllm_ascend import envs as envs_ascend


def _rkv_trace_enabled() -> bool:
    return envs_ascend.VLLM_ASCEND_RKV_TRACE


def _format_trace_fields(fields: dict[str, object]) -> str:
    return " ".join(f"{key}={value}" for key, value in fields.items() if value is not None)


def rkv_trace_log(event: str, **fields: object) -> None:
    if not _rkv_trace_enabled():
        return
    formatted = _format_trace_fields(fields)
    if formatted:
        logger.info("RKV_TRACE %s %s", event, formatted)
    else:
        logger.info("RKV_TRACE %s", event)


def _sync_trace_device(tensor: torch.Tensor | None) -> None:
    if tensor is None:
        return
    device = tensor.device
    if device.type == "npu":
        npu = getattr(torch, "npu", None)
        if npu is not None and hasattr(npu, "synchronize"):
            npu.synchronize()
    elif device.type == "cuda" and hasattr(torch, "cuda") and torch.cuda.is_available():
        torch.cuda.synchronize(device)


@contextmanager
def rkv_trace_timer(
    event: str,
    tensor: torch.Tensor | None = None,
    **fields: object,
) -> Iterator[None]:
    if not _rkv_trace_enabled():
        yield
        return
    _sync_trace_device(tensor)
    start = time.perf_counter()
    try:
        yield
    finally:
        _sync_trace_device(tensor)
        rkv_trace_log(
            event,
            elapsed_ms=f"{(time.perf_counter() - start) * 1000:.3f}",
            **fields,
        )


def compute_attention_scores(
    query_states: torch.Tensor,
    key_states: torch.Tensor,
    pooling: str = "max",
) -> torch.Tensor:
    """Return per-KV-head attention logits used by R-KV scoring.

    Args:
        query_states: [batch, q_heads, q_len, head_dim].
        key_states: [batch, kv_heads, kv_len, head_dim].
    """
    batch_size, q_heads, q_len, head_dim = query_states.shape
    kv_heads = key_states.shape[1]
    query_group_size = q_heads // kv_heads

    if query_group_size == 1:
        return torch.matmul(query_states, key_states.transpose(2, 3)) / math.sqrt(head_dim)

    query_states = query_states.view(batch_size, kv_heads, query_group_size, q_len, head_dim)
    key_states = key_states.unsqueeze(2)
    attn_weights = torch.matmul(query_states, key_states.transpose(3, 4)) / math.sqrt(head_dim)

    if pooling == "mean":
        return attn_weights.mean(dim=2)
    if pooling == "max":
        return attn_weights.max(dim=2).values
    raise ValueError(f"Unsupported R-KV pooling method: {pooling}")


def calculate_similarity(
    key_states: torch.Tensor,
    threshold: float = 0.5,
    retain_ratio: float = 0.2,
    retain_direction: str = "last",
) -> torch.Tensor:
    """Calculate the redundancy score from key cosine similarity.

    This mirrors the paper/reference implementation: highly similar keys are
    penalized, while one representative similar key is retained.
    """
    key_states = key_states[0]
    num_heads = key_states.shape[0]

    with rkv_trace_timer(
        "calculate_similarity.normalize",
        key_states,
        num_heads=num_heads,
        seq_len=key_states.shape[-2],
    ):
        key_norm = key_states / (key_states.norm(dim=-1, keepdim=True) + 1e-8)

    with rkv_trace_timer(
        "calculate_similarity.cosine_matmul",
        key_states,
        num_heads=num_heads,
        seq_len=key_states.shape[-2],
    ):
        similarity_cos = torch.matmul(key_norm, key_norm.transpose(-1, -2))

    with rkv_trace_timer(
        "calculate_similarity.retain_mask",
        key_states,
        num_heads=num_heads,
        threshold=threshold,
        retain_ratio=retain_ratio,
        retain_direction=retain_direction,
    ):
        for head_idx in range(num_heads):
            similarity_cos[head_idx].fill_diagonal_(0.0)

        similarity_mask = similarity_cos > threshold
        seq_len = similarity_mask.size(-1)
        topk = min(seq_len, max(1, int(seq_len * retain_ratio)))
        seq_indices = torch.arange(seq_len, device=similarity_mask.device)

        indices = torch.where(
            similarity_mask,
            seq_indices,
            torch.zeros_like(similarity_mask, dtype=torch.long),
        )

        if retain_direction == "last":
            similarity_retain = torch.max(indices, dim=-1)[0]
        elif retain_direction == "first":
            similarity_retain = torch.min(indices, dim=-1)[0]
        elif retain_direction == "last_percent":
            similarity_retain = torch.topk(indices, k=topk, dim=-1)[0][:, :, 0]
        elif retain_direction == "first_percent":
            similarity_retain = torch.topk(indices, k=topk, dim=-1, largest=False)[0][:, :, -1]
        else:
            raise ValueError(f"Unsupported R-KV retain direction: {retain_direction}")

        batch_idx = torch.arange(num_heads, device=key_states.device).unsqueeze(1).repeat(
            1,
            similarity_retain.size(1),
        )
        seq_idx = torch.arange(similarity_retain.size(1), device=key_states.device).unsqueeze(0).repeat(
            num_heads,
            1,
        )
        similarity_cos[batch_idx, seq_idx, similarity_retain] = 0

    with rkv_trace_timer("calculate_similarity.softmax", key_states, num_heads=num_heads):
        return similarity_cos.mean(dim=1).softmax(dim=-1)


class RKVCompressor:
    """R-KV redundancy-aware KV cache compressor.

    The input/output layout follows the HuggingFace reference:
    key/value: [1, kv_heads, seq_len, head_dim],
    query: [1, q_heads, q_len, head_dim].
    """

    def __init__(
        self,
        budget: int,
        window_size: int = 8,
        kernel_size: int = 7,
        mix_lambda: float = 0.07,
        retain_ratio: float = 0.2,
        retain_direction: str = "last",
    ) -> None:
        if budget <= window_size:
            raise ValueError("R-KV budget must be greater than window_size")
        self.budget = budget
        self.window_size = window_size
        self.kernel_size = kernel_size
        self.mix_lambda = mix_lambda
        self.retain_ratio = retain_ratio
        self.retain_direction = retain_direction

    def update_kv(
        self,
        key_states: torch.Tensor,
        query_states: torch.Tensor,
        value_states: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        head_dim = query_states.shape[-1]
        kv_cache_len = key_states.shape[-2]
        rkv_trace_log(
            "update_kv_start",
            kv_cache_len=kv_cache_len,
            query_len=query_states.shape[-2],
            budget=self.budget,
            window_size=self.window_size,
            kv_heads=key_states.shape[1],
            q_heads=query_states.shape[1],
            dtype=key_states.dtype,
            device=key_states.device,
        )

        if kv_cache_len <= self.budget:
            rkv_trace_log(
                "update_kv_skip",
                reason="under_budget",
                kv_cache_len=kv_cache_len,
                budget=self.budget,
            )
            return key_states, value_states

        observation = min(self.window_size, query_states.shape[-2], kv_cache_len - 1)
        if observation <= 0:
            rkv_trace_log("update_kv_skip", reason="no_observation_window", kv_cache_len=kv_cache_len)
            return key_states[:, :, -self.budget :, :], value_states[:, :, -self.budget :, :]

        with rkv_trace_timer(
            "update_kv.attention_scores",
            query_states,
            kv_cache_len=kv_cache_len,
            observation=observation,
        ):
            attn_weights = compute_attention_scores(query_states, key_states)

        with rkv_trace_timer(
            "update_kv.attention_pool",
            query_states,
            observation=observation,
            kernel_size=self.kernel_size,
        ):
            attn_weights_sum = (
                F.softmax(
                    attn_weights[:, :, -observation:, :-observation],
                    dim=-1,
                    dtype=torch.float32,
                )
                .mean(dim=-2)
                .to(query_states.dtype)
            )
            attn_cache = F.max_pool1d(
                attn_weights_sum,
                kernel_size=self.kernel_size,
                padding=self.kernel_size // 2,
                stride=1,
            )

        with rkv_trace_timer(
            "update_kv.similarity",
            key_states,
            kv_cache_len=kv_cache_len,
            observation=observation,
        ):
            similarity_cos = calculate_similarity(
                key_states,
                retain_ratio=self.retain_ratio,
                retain_direction=self.retain_direction,
            )[:, :-observation]

        keep_old = self.budget - observation
        with rkv_trace_timer(
            "update_kv.score_topk",
            key_states,
            keep_old=keep_old,
            mix_lambda=self.mix_lambda,
        ):
            final_score = attn_cache * self.mix_lambda - similarity_cos * (1 - self.mix_lambda)
            indices = final_score.topk(keep_old, dim=-1).indices
            indices = indices.unsqueeze(-1).expand(-1, -1, -1, head_dim)

        with rkv_trace_timer(
            "update_kv.gather_cat",
            key_states,
            keep_old=keep_old,
            observation=observation,
        ):
            key_past = key_states[:, :, :-observation, :].gather(dim=2, index=indices)
            value_past = value_states[:, :, :-observation, :].gather(dim=2, index=indices)
            key_recent = key_states[:, :, -observation:, :]
            value_recent = value_states[:, :, -observation:, :]
            compressed_key = torch.cat([key_past, key_recent], dim=2)
            compressed_value = torch.cat([value_past, value_recent], dim=2)

        rkv_trace_log(
            "update_kv_done",
            old_len=kv_cache_len,
            new_len=compressed_key.shape[-2],
            observation=observation,
            keep_old=keep_old,
        )
        return compressed_key, compressed_value
