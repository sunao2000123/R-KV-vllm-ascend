#
# Copyright (c) 2026.
#
# R-KV cache compression helpers for vLLM-Ascend.
#

import math

import torch
import torch.nn.functional as F


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

    key_norm = key_states / (key_states.norm(dim=-1, keepdim=True) + 1e-8)
    similarity_cos = torch.matmul(key_norm, key_norm.transpose(-1, -2))

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

    batch_idx = torch.arange(num_heads, device=key_states.device).unsqueeze(1).repeat(1, similarity_retain.size(1))
    seq_idx = torch.arange(similarity_retain.size(1), device=key_states.device).unsqueeze(0).repeat(num_heads, 1)
    similarity_cos[batch_idx, seq_idx, similarity_retain] = 0

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

        if kv_cache_len <= self.budget:
            return key_states, value_states

        observation = min(self.window_size, query_states.shape[-2], kv_cache_len - 1)
        if observation <= 0:
            return key_states[:, :, -self.budget :, :], value_states[:, :, -self.budget :, :]

        attn_weights = compute_attention_scores(query_states, key_states)
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

        similarity_cos = calculate_similarity(
            key_states,
            retain_ratio=self.retain_ratio,
            retain_direction=self.retain_direction,
        )[:, :-observation]
        final_score = attn_cache * self.mix_lambda - similarity_cos * (1 - self.mix_lambda)

        keep_old = self.budget - observation
        indices = final_score.topk(keep_old, dim=-1).indices
        indices = indices.unsqueeze(-1).expand(-1, -1, -1, head_dim)

        key_past = key_states[:, :, :-observation, :].gather(dim=2, index=indices)
        value_past = value_states[:, :, :-observation, :].gather(dim=2, index=indices)
        key_recent = key_states[:, :, -observation:, :]
        value_recent = value_states[:, :, -observation:, :]

        return torch.cat([key_past, key_recent], dim=2), torch.cat([value_past, value_recent], dim=2)
