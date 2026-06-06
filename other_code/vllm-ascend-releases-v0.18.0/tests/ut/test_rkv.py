import unittest
from unittest.mock import patch

import torch

from vllm_ascend.rkv import (
    RKVCompressor,
    calculate_sampled_similarity,
    calculate_similarity,
)


def _reference_similarity_last(
    key_states: torch.Tensor,
    threshold: float,
) -> torch.Tensor:
    key_states = key_states[0]
    key_norm = key_states / (key_states.norm(dim=-1, keepdim=True) + 1e-8)
    scores = []
    for head_idx in range(key_norm.shape[0]):
        similarity = torch.matmul(key_norm[head_idx], key_norm[head_idx].transpose(0, 1))
        similarity.fill_diagonal_(0.0)
        for row_idx in range(similarity.shape[0]):
            similar_indices = torch.nonzero(similarity[row_idx] > threshold).flatten()
            if similar_indices.numel() > 0:
                similarity[row_idx, similar_indices[-1]] = 0.0
        scores.append(similarity.mean(dim=0).softmax(dim=-1))
    return torch.stack(scores, dim=0)


class TestRKVCompressor(unittest.TestCase):

    def test_calculate_similarity_matches_reference_with_chunking(self):
        torch.manual_seed(0)
        key_states = torch.randn(1, 2, 9, 4)

        with patch("vllm_ascend.rkv._SIMILARITY_MAX_CHUNK", 2):
            actual = calculate_similarity(key_states, threshold=0.25, retain_direction="last")

        expected = _reference_similarity_last(key_states, threshold=0.25)
        torch.testing.assert_close(actual, expected)

    def test_calculate_sampled_similarity_matches_exact_when_sampling_all_rows(self):
        torch.manual_seed(0)
        key_states = torch.randn(1, 2, 9, 4)

        actual = calculate_sampled_similarity(
            key_states,
            sample_size=9,
            threshold=0.25,
            retain_direction="last",
        )
        expected = calculate_similarity(key_states, threshold=0.25, retain_direction="last")

        torch.testing.assert_close(actual, expected)

    def test_update_kv_reduces_cache_to_budget(self):
        torch.manual_seed(0)
        compressor = RKVCompressor(budget=6, window_size=2, kernel_size=3)
        key_states = torch.randn(1, 2, 12, 4)
        value_states = torch.randn(1, 2, 12, 4)
        query_states = torch.randn(1, 4, 2, 4)

        compressed_key, compressed_value = compressor.update_kv(
            key_states,
            query_states,
            value_states,
        )

        self.assertEqual(compressed_key.shape, (1, 2, 6, 4))
        self.assertEqual(compressed_value.shape, (1, 2, 6, 4))
        torch.testing.assert_close(compressed_key[:, :, -2:, :], key_states[:, :, -2:, :])
        torch.testing.assert_close(compressed_value[:, :, -2:, :], value_states[:, :, -2:, :])

    def test_update_kv_uses_sampled_similarity_for_large_cache(self):
        torch.manual_seed(0)
        compressor = RKVCompressor(
            budget=6,
            window_size=2,
            kernel_size=3,
            similarity_sample_size=4,
        )
        key_states = torch.randn(1, 2, 12, 4)
        value_states = torch.randn(1, 2, 12, 4)
        query_states = torch.randn(1, 4, 2, 4)

        with patch("vllm_ascend.rkv.calculate_similarity") as mock_exact:
            compressed_key, compressed_value = compressor.update_kv(
                key_states,
                query_states,
                value_states,
            )

        mock_exact.assert_not_called()
        self.assertEqual(compressed_key.shape, (1, 2, 6, 4))
        self.assertEqual(compressed_value.shape, (1, 2, 6, 4))


if __name__ == "__main__":
    unittest.main()
