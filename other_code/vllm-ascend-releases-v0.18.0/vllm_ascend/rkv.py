#
# Copyright (c) 2026.
#
# R-KV cache compression helpers for vLLM-Ascend.
#

import math

import torch
import torch.nn.functional as F


_SIMILARITY_MAX_CHUNK = 256
_SIMILARITY_MAX_PAIR_ELEMENTS = 2 * 1024 * 1024


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


def _similarity_chunk_size(seq_len: int) -> int:
    return min(_SIMILARITY_MAX_CHUNK, max(1, _SIMILARITY_MAX_PAIR_ELEMENTS // max(1, seq_len)))


def _select_retain_indices(
    similarity_mask: torch.Tensor,
    retain_ratio: float,
    retain_direction: str,
) -> tuple[torch.Tensor, torch.Tensor]:
    seq_len = similarity_mask.size(-1)
    valid = similarity_mask.any(dim=-1)

    if retain_direction == "last":
        retain = seq_len - 1 - similarity_mask.flip(-1).to(torch.long).argmax(dim=-1)
    elif retain_direction == "first":
        retain = similarity_mask.to(torch.long).argmax(dim=-1)
    elif retain_direction in ("last_percent", "first_percent"):
        topk = min(seq_len, max(1, int(seq_len * retain_ratio)))
        seq_indices = torch.arange(seq_len, device=similarity_mask.device, dtype=torch.long)
        seq_indices = seq_indices.unsqueeze(0).expand_as(similarity_mask)
        if retain_direction == "last_percent":
            masked_indices = seq_indices.masked_fill(~similarity_mask, -1)
            retain = torch.topk(masked_indices, k=topk, dim=-1).values[:, -1]
            valid = retain >= 0
        else:
            masked_indices = seq_indices.masked_fill(~similarity_mask, seq_len)
            retain = torch.topk(masked_indices, k=topk, dim=-1, largest=False).values[:, -1]
            valid = retain < seq_len
    else:
        raise ValueError(f"Unsupported R-KV retain direction: {retain_direction}")

    return retain, valid


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
    num_heads, seq_len = key_states.shape[:2]

    key_norm = key_states / (key_states.norm(dim=-1, keepdim=True) + 1e-8)
    chunk_size = _similarity_chunk_size(seq_len)
    redundancy_scores = torch.empty((num_heads, seq_len), device=key_states.device, dtype=key_states.dtype)

    for head_idx in range(num_heads):
        head_key_norm = key_norm[head_idx]
        score_sum = torch.zeros(seq_len, device=key_states.device, dtype=key_states.dtype)
        for start in range(0, seq_len, chunk_size):
            end = min(start + chunk_size, seq_len)
            similarity_chunk = torch.matmul(head_key_norm[start:end], head_key_norm.transpose(0, 1))
            diagonal = torch.arange(start, end, device=key_states.device)
            similarity_chunk[torch.arange(end - start, device=key_states.device), diagonal] = 0.0

            similarity_mask = similarity_chunk > threshold
            retain, valid = _select_retain_indices(similarity_mask, retain_ratio, retain_direction)
            row_idx = torch.arange(end - start, device=key_states.device)[valid]
            similarity_chunk[row_idx, retain[valid]] = 0.0
            score_sum += similarity_chunk.sum(dim=0)

        redundancy_scores[head_idx] = score_sum / seq_len

    return redundancy_scores.softmax(dim=-1)


def _sample_similarity_rows(seq_len: int, sample_size: int, device: torch.device) -> torch.Tensor:
    sample_size = min(seq_len, max(1, sample_size))
    if sample_size == seq_len:
        return torch.arange(seq_len, device=device, dtype=torch.long)
    if sample_size == 1:
        return torch.tensor([seq_len - 1], device=device, dtype=torch.long)
    return torch.arange(sample_size, device=device, dtype=torch.long) * (seq_len - 1) // (sample_size - 1)


def calculate_sampled_similarity(
    key_states: torch.Tensor,
    sample_size: int,
    threshold: float = 0.5,
    retain_ratio: float = 0.2,
    retain_direction: str = "last",
) -> torch.Tensor:
    """Approximate redundancy score using evenly sampled source rows.

    Full R-KV cosine redundancy is O(seq_len^2) per layer. In decode service
    mode that cost can dominate TPOT, so long caches use a bounded row sample
    while preserving the same representative-retention rule.
    """
    key_states = key_states[0]
    num_heads, seq_len = key_states.shape[:2]
    sample_indices = _sample_similarity_rows(seq_len, sample_size, key_states.device)
    sample_count = sample_indices.numel()

    key_norm = key_states / (key_states.norm(dim=-1, keepdim=True) + 1e-8)
    redundancy_scores = torch.empty((num_heads, seq_len), device=key_states.device, dtype=key_states.dtype)
    sample_row_idx = torch.arange(sample_count, device=key_states.device)

    for head_idx in range(num_heads):
        head_key_norm = key_norm[head_idx]
        sampled_key_norm = head_key_norm.index_select(0, sample_indices)
        similarity = torch.matmul(sampled_key_norm, head_key_norm.transpose(0, 1))
        similarity[sample_row_idx, sample_indices] = 0.0

        similarity_mask = similarity > threshold
        retain, valid = _select_retain_indices(similarity_mask, retain_ratio, retain_direction)
        row_idx = sample_row_idx[valid]
        similarity[row_idx, retain[valid]] = 0.0
        redundancy_scores[head_idx] = similarity.sum(dim=0) / sample_count

    return redundancy_scores.softmax(dim=-1)


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
        similarity_sample_size: int = 128,
    ) -> None:
        if budget <= window_size:
            raise ValueError("R-KV budget must be greater than window_size")
        self.budget = budget
        self.window_size = window_size
        self.kernel_size = kernel_size
        self.mix_lambda = mix_lambda
        self.retain_ratio = retain_ratio
        self.retain_direction = retain_direction
        self.similarity_sample_size = max(0, similarity_sample_size)

    def _calculate_similarity(self, key_states: torch.Tensor) -> torch.Tensor:
        kv_cache_len = key_states.shape[-2]
        if self.similarity_sample_size and kv_cache_len > self.similarity_sample_size:
            return calculate_sampled_similarity(
                key_states,
                sample_size=self.similarity_sample_size,
                retain_ratio=self.retain_ratio,
                retain_direction=self.retain_direction,
            )
        return calculate_similarity(
            key_states,
            retain_ratio=self.retain_ratio,
            retain_direction=self.retain_direction,
        )

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

        similarity_cos = self._calculate_similarity(key_states)[:, :-observation]
        final_score = attn_cache * self.mix_lambda - similarity_cos * (1 - self.mix_lambda)

        keep_old = self.budget - observation
        indices = final_score.topk(keep_old, dim=-1).indices
        indices = indices.unsqueeze(-1).expand(-1, -1, -1, head_dim)

        key_past = key_states[:, :, :-observation, :].gather(dim=2, index=indices)
        value_past = value_states[:, :, :-observation, :].gather(dim=2, index=indices)
        key_recent = key_states[:, :, -observation:, :]
        value_recent = value_states[:, :, -observation:, :]

        return torch.cat([key_past, key_recent], dim=2), torch.cat([value_past, value_recent], dim=2)
