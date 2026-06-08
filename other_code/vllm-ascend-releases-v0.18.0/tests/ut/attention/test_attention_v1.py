from unittest.mock import MagicMock, patch

import torch

from tests.ut.base import TestBase
from vllm_ascend.attention.attention_v1 import (AscendAttentionBackend,
                                                AscendAttentionBackendImpl,
                                                AscendAttentionMetadataBuilder,
                                                AscendAttentionState,
                                                _RKV_SELECTION_CACHE,
                                                _rkv_breakpoint)
from vllm_ascend.attention.utils import AscendCommonAttentionMetadata
from vllm_ascend.utils import AscendDeviceType


class TestAscendAttentionBackend(TestBase):

    def setUp(self):
        self.mock_config = MagicMock()

        mock_parallel_config = MagicMock()
        mock_parallel_config.prefill_context_parallel_size = 1
        mock_parallel_config.decode_context_parallel_size = 1

        self.mock_config.parallel_config = mock_parallel_config

        self.utils_patcher = patch(
            'vllm_ascend.attention.utils.get_current_vllm_config',
            return_value=self.mock_config)
        self.utils_patcher.start()

        from vllm_ascend.attention.utils import enable_cp
        enable_cp.cache_clear()

    def test_get_name(self):
        self.assertEqual(AscendAttentionBackend.get_name(), "CUSTOM")

    def test_get_impl_cls(self):
        self.assertEqual(AscendAttentionBackend.get_impl_cls(),
                         AscendAttentionBackendImpl)

    def test_get_builder_cls(self):
        self.assertEqual(AscendAttentionBackend.get_builder_cls(),
                         AscendAttentionMetadataBuilder)

    def test_get_kv_cache_shape_not(self):
        result = AscendAttentionBackend.get_kv_cache_shape(10, 20, 30, 40)
        self.assertEqual(result, (2, 10, 20, 30, 40))

    def test_swap_blocks(self):
        src_kv_cache = [torch.zeros((10, 20)), torch.zeros((10, 20))]
        dst_kv_cache = [torch.zeros((10, 20)), torch.zeros((10, 20))]
        src_to_dst = torch.tensor([[0, 1], [2, 3]])
        AscendAttentionBackend.swap_blocks(src_kv_cache, dst_kv_cache,
                                           src_to_dst)
        self.assertTrue(torch.all(dst_kv_cache[0][1] == src_kv_cache[0][0]))
        self.assertTrue(torch.all(dst_kv_cache[1][3] == src_kv_cache[1][2]))

    def test_copy_blocks(self):
        kv_caches = [torch.zeros((10, 20)), torch.zeros((10, 20))]
        src_to_dists = torch.tensor([[0, 1], [2, 3]])
        AscendAttentionBackend.copy_blocks(kv_caches, src_to_dists)
        self.assertTrue(torch.all(kv_caches[0][1] == kv_caches[0][0]))
        self.assertTrue(torch.all(kv_caches[1][3] == kv_caches[1][2]))


class TestAscendAttentionMetadataBuilder(TestBase):

    def setUp(self):
        self.mock_vllm_config = MagicMock()
        self.mock_vllm_config.speculative_config = None
        self.mock_vllm_config.model_config.max_model_len = 640
        self.mock_vllm_config.model_config.hf_text_config.sliding_window = None
        self.mock_vllm_config.cache_config.block_size = 64
        self.mock_vllm_config.compilation_config.cudagraph_mode = None
        self.mock_vllm_config.scheduler_config.max_num_seqs = 10
        self.mock_vllm_config.scheduler_config.decode_max_num_seqs = 10
        self.mock_vllm_config.scheduler_config.chunked_prefill_enabled = False
        self.mock_device = 'cpu:0'
        torch.Tensor.pin_memory = lambda x: x  # noqa
        self.builder = AscendAttentionMetadataBuilder(None, None,
                                                      self.mock_vllm_config,
                                                      self.mock_device)

    def test_reorder_batch(self):
        mock_input_batch = MagicMock()
        mock_scheduler_output = MagicMock()

        result = self.builder.reorder_batch(mock_input_batch,
                                            mock_scheduler_output)

        self.assertFalse(result)

    @patch('vllm_ascend.attention.attention_v1.AscendMetadata')
    def test_build(self, mock_ascend_metadata):
        common_attn_metadata = AscendCommonAttentionMetadata(
            query_start_loc=torch.tensor([0, 2, 5, 9]),
            query_start_loc_cpu=torch.tensor([0, 2, 5, 9]),
            seq_lens_cpu=torch.tensor([4, 5, 6]),
            num_reqs=3,
            num_actual_tokens=15,
            max_query_len=6,
            decode_token_per_req=torch.tensor([1, 1, 1]),
            block_table_tensor=torch.zeros((10, 10)),
            slot_mapping=torch.tensor(range(20)),
            actual_seq_lengths_q=torch.tensor([0, 1, 2]),
            positions=torch.tensor([10, 10]),
            attn_state=AscendAttentionState.ChunkedPrefill,
            num_computed_tokens_cpu=None,
            seq_lens=None,
            max_seq_len=6)
        mock_model = MagicMock()

        self.builder.build(1, common_attn_metadata, mock_model)


class TestAscendAttentionBackendImpl(TestBase):

    def setUp(self):
        self.mock_event = MagicMock()
        self.mock_event.record.return_value = None
        self.mock_event.wait.return_value = None
        _RKV_SELECTION_CACHE.clear()

        self.mock_stream = MagicMock()
        self.event_patcher = patch('torch_npu.npu.Event',
                                   return_value=self.mock_event)
        self.stream_patcher = patch('torch_npu.npu.current_stream',
                                    return_value=self.mock_stream)

        self.event_patcher.start()
        self.stream_patcher.start()

        self.layer = MagicMock()
        self.layer.layer_name = "test_layer"
        self.layer._k_scale_float = 1.0
        self.layer._v_scale_float = 1.0
        self.attention_type = MagicMock()
        self.attention_type.DECODER = "decoder"
        self.attention_type.ENCODER = "encoder"
        self.attn_metadata = MagicMock()
        self.attn_metadata.return_value = "1"
        self.layer_no_quant = MagicMock(
            spec=['layer_name', '_k_scale_float', '_v_scale_float'])
        self.layer_no_quant.layer_name = "test_layer"
        self.layer_no_quant._k_scale_float = 1.0
        self.layer_no_quant._v_scale_float = 1.0
        self.mock_vllm_config = MagicMock()
        self.config_patcher = patch(
            'vllm_ascend.attention.attention_v1.get_current_vllm_config',
            return_value=self.mock_vllm_config)
        self.config_patcher.start()

        self.impl = AscendAttentionBackendImpl(
            num_heads=8,
            head_size=64,
            scale=1.0,
            num_kv_heads=8,
            alibi_slopes=None,
            sliding_window=None,
            kv_cache_dtype="float16",
            logits_soft_cap=None,
            attn_type=self.attention_type.DECODER,
            kv_sharing_target_layer_name=None)

        self.impl_192 = AscendAttentionBackendImpl(
            num_heads=8,
            head_size=192,
            scale=1.0,
            num_kv_heads=8,
            alibi_slopes=None,
            sliding_window=None,
            kv_cache_dtype="float16",
            logits_soft_cap=None,
            attn_type=self.attention_type.DECODER,
            kv_sharing_target_layer_name=None)

        self.impl_error = AscendAttentionBackendImpl(
            num_heads=8,
            head_size=192,
            scale=1.0,
            num_kv_heads=8,
            alibi_slopes=None,
            sliding_window=None,
            kv_cache_dtype="float16",
            logits_soft_cap=None,
            attn_type=None,
            kv_sharing_target_layer_name=None)

        self.impl_swa = AscendAttentionBackendImpl(
            num_heads=8,
            head_size=64,
            scale=1.0,
            num_kv_heads=8,
            alibi_slopes=None,
            sliding_window=1024,
            kv_cache_dtype="float16",
            logits_soft_cap=None,
            attn_type=self.attention_type.DECODER,
            kv_sharing_target_layer_name=None)

    def _enable_rkv_for_test(self):
        self.impl.rkv_enabled = True
        self.impl.rkv_compressor = MagicMock()
        self.impl.rkv_compressor.budget = 1024
        self.impl.rkv_compressor.window_size = 8
        self.impl.rkv_compressor.kernel_size = 7
        self.impl.rkv_compressor.mix_lambda = 0.1
        self.impl.rkv_compressor.retain_ratio = 0.1
        self.impl.rkv_compressor.retain_direction = "last"
        self.impl.rkv_compressor.similarity_sample_size = 16
        self.impl.rkv_compressor.selection_mode = "aggregate"
        self.impl.rkv_share_selection = True
        self.impl.rkv_query_cache = {}
        self.impl.vllm_config.speculative_config = None
        self.impl.vllm_config.model_config.use_mla = False
        self.impl.key_cache = torch.zeros(2, 128, 8, 64)
        self.impl.value_cache = torch.zeros(2, 128, 8, 64)

    def _rkv_metadata(self, attn_state, seq_len=1):
        metadata = MagicMock()
        metadata.attn_state = attn_state
        metadata.block_tables = torch.zeros(1, 32, dtype=torch.long)
        metadata.rkv_req_ids = ["req"]
        metadata.rkv_reset_req_ids = []
        metadata.seq_lens_list = [seq_len]
        metadata.actual_seq_lengths_q = [1]
        metadata.rkv_compressed_lens = None
        return metadata

    @patch.dict('os.environ', {'VLLM_ASCEND_RKV_BREAKPOINT': 'log'})
    @patch('vllm_ascend.attention.attention_v1.logger')
    def test_rkv_breakpoint_logs_when_enabled(self, mock_logger):
        _rkv_breakpoint("runtime_enabled", req_count=1)

        mock_logger.warning.assert_called_once()

    @patch.dict('os.environ',
                {'VLLM_ASCEND_RKV_BREAKPOINT': 'runtime_enabled'})
    @patch('vllm_ascend.attention.attention_v1.logger')
    def test_rkv_breakpoint_can_stop_on_event(self, mock_logger):
        with self.assertRaisesRegex(RuntimeError, "RKV_BREAKPOINT runtime_enabled"):
            _rkv_breakpoint("runtime_enabled", req_count=1)

        mock_logger.warning.assert_called_once()

    @patch('vllm_ascend.attention.attention_v1.enable_cp', return_value=False)
    @patch('vllm_ascend.attention.attention_v1._EXTRA_CTX')
    def test_rkv_query_cache_updates_only_in_decode(self, mock_extra_ctx,
                                                    mock_enable_cp):
        self._enable_rkv_for_test()
        mock_extra_ctx.capturing = False
        mock_extra_ctx.is_draft_model = False
        query = torch.randn(1, 8, 64)

        metadata = self._rkv_metadata(AscendAttentionState.ChunkedPrefill)
        self.impl._update_rkv_query_cache(query, metadata)
        self.assertNotIn("req", self.impl.rkv_query_cache)

        metadata = self._rkv_metadata(
            AscendAttentionState.DecodeOnly,
            seq_len=self.impl._rkv_query_cache_start_len() - 1)
        self.impl.rkv_query_cache["req"] = torch.randn(8, 8, 64)
        self.impl._update_rkv_query_cache(query, metadata)
        self.assertNotIn("req", self.impl.rkv_query_cache)

        metadata = self._rkv_metadata(
            AscendAttentionState.DecodeOnly,
            seq_len=self.impl._rkv_query_cache_start_len())
        self.impl._update_rkv_query_cache(query, metadata)
        self.assertIn("req", self.impl.rkv_query_cache)

    @patch('vllm_ascend.attention.attention_v1.enable_cp', return_value=False)
    @patch('vllm_ascend.attention.attention_v1._EXTRA_CTX')
    def test_rkv_query_cache_resets_reused_req_id(self, mock_extra_ctx,
                                                  mock_enable_cp):
        self._enable_rkv_for_test()
        mock_extra_ctx.capturing = False
        mock_extra_ctx.is_draft_model = False
        self.impl.rkv_query_cache["req"] = torch.randn(8, 8, 64)
        query = torch.randn(1, 8, 64)
        metadata = self._rkv_metadata(
            AscendAttentionState.DecodeOnly,
            seq_len=self.impl._rkv_query_cache_start_len())
        metadata.rkv_reset_req_ids = ["req"]

        self.impl._update_rkv_query_cache(query, metadata)

        self.assertEqual(self.impl.rkv_query_cache["req"].shape[0], 1)
        self.assertTrue(torch.equal(self.impl.rkv_query_cache["req"], query))

    @patch('vllm_ascend.attention.attention_v1.enable_cp', return_value=False)
    @patch('vllm_ascend.attention.attention_v1._EXTRA_CTX')
    def test_rkv_compression_runs_with_available_query(self, mock_extra_ctx,
                                                       mock_enable_cp):
        self._enable_rkv_for_test()
        mock_extra_ctx.capturing = False
        mock_extra_ctx.is_draft_model = False
        self.impl.rkv_query_cache["req"] = torch.randn(1, 8, 64)
        metadata = self._rkv_metadata(AscendAttentionState.DecodeOnly,
                                      seq_len=4096)
        key_states = torch.randn(1, 8, 16, 64)
        indices = torch.arange(1016).unsqueeze(0)
        self.impl.rkv_compressor.select_indices.return_value = (indices, 8)

        with patch.object(self.impl, '_gather_rkv_key',
                          return_value=key_states) as mock_gather, \
                patch.object(self.impl, '_write_rkv_selection',
                             return_value=1024) as mock_write:
            self.impl._maybe_compress_rkv(torch.randn(1, 8, 64), metadata)

        mock_gather.assert_called_once()
        self.impl.rkv_compressor.select_indices.assert_called_once()
        mock_write.assert_called_once()

    @patch('vllm_ascend.attention.attention_v1.enable_cp', return_value=False)
    @patch('vllm_ascend.attention.attention_v1._EXTRA_CTX')
    def test_rkv_compression_clears_query_cache(self, mock_extra_ctx,
                                                mock_enable_cp):
        self._enable_rkv_for_test()
        mock_extra_ctx.capturing = False
        mock_extra_ctx.is_draft_model = False
        self.impl.rkv_query_cache["req"] = torch.randn(8, 8, 64)
        metadata = self._rkv_metadata(AscendAttentionState.DecodeOnly,
                                      seq_len=4096)
        key_states = torch.randn(1, 8, 16, 64)
        indices = torch.arange(1016).unsqueeze(0)
        self.impl.rkv_compressor.select_indices.return_value = (indices, 8)

        with patch.object(self.impl, '_gather_rkv_key',
                          return_value=key_states) as mock_gather, \
                patch.object(self.impl, '_write_rkv_selection',
                             return_value=1024) as mock_write:
            self.impl._maybe_compress_rkv(torch.randn(1, 8, 64), metadata)

        mock_gather.assert_called_once()
        self.impl.rkv_compressor.select_indices.assert_called_once()
        mock_write.assert_called_once()
        self.assertNotIn("req", self.impl.rkv_query_cache)
        self.assertEqual(metadata.rkv_compressed_lens, [1024])

    @patch('vllm_ascend.attention.attention_v1.enable_cp', return_value=False)
    @patch('vllm_ascend.attention.attention_v1._EXTRA_CTX')
    def test_rkv_compression_reuses_shared_selection(self, mock_extra_ctx,
                                                     mock_enable_cp):
        self._enable_rkv_for_test()
        mock_extra_ctx.capturing = False
        mock_extra_ctx.is_draft_model = False
        metadata = self._rkv_metadata(AscendAttentionState.DecodeOnly,
                                      seq_len=4096)
        key_states = torch.randn(1, 8, 16, 64)
        indices = torch.arange(1016).unsqueeze(0)
        self.impl.rkv_compressor.select_indices.return_value = (indices, 8)

        with patch.object(self.impl, '_gather_rkv_key',
                          return_value=key_states) as mock_gather, \
                patch.object(self.impl, '_write_rkv_selection',
                             return_value=1024) as mock_write:
            self.impl.rkv_query_cache["req"] = torch.randn(1, 8, 64)
            self.impl._maybe_compress_rkv(torch.randn(1, 8, 64), metadata)
            self.impl.rkv_query_cache["req"] = torch.randn(1, 8, 64)
            self.impl._maybe_compress_rkv(torch.randn(1, 8, 64), metadata)

        mock_gather.assert_called_once()
        self.impl.rkv_compressor.select_indices.assert_called_once()
        self.assertEqual(mock_write.call_count, 2)

    def test_forward_no_attn_metadata(self):
        """Test forward pass when attn_metadata is None"""
        query = torch.randn(10, 8 * 64)
        key = torch.randn(10, 8 * 64)
        value = torch.randn(10, 8 * 64)
        kv_cache = torch.empty(2, 0, 0, 8, 64)
        layer = self.layer_no_quant
        output = torch.empty_like(query)

        output = self.impl.forward(layer, query, key, value, kv_cache, None,
                                   output)

        assert output.shape == (10, 8 * 64)

    @patch('torch_npu._npu_reshape_and_cache')
    @patch('torch_npu.npu_fused_infer_attention_score')
    @patch('vllm_ascend.ascend_forward_context.get_forward_context')
    def test_forward_fused_infer_attention(
            self, mock_get_forward_context,
            mock_npu_fused_infer_attention_score, mock_npu_reshape_and_cache):
        """Test forward pass in PrefillCacheHit state"""
        query = torch.randn(10, 8, 64)
        key = torch.randn(10, 8, 64)
        value = torch.randn(10, 8, 64)
        kv_cache = torch.empty(2, 5, 128, 8, 64)
        output = torch.empty_like(query)
        metadata = self.attn_metadata
        metadata.attn_state = AscendAttentionState.PrefillCacheHit
        metadata.attn_mask = torch.randn(1, 1, 10, 10)
        metadata.query_lens = torch.tensor([10])
        metadata.seq_lens = torch.tensor([10])
        metadata.actual_seq_lengths_q = [10]
        metadata.block_tables = torch.zeros(1, 5, dtype=torch.long)
        metadata.num_actual_tokens = 10
        metadata.num_decode_tokens = 0
        metadata.num_decodes = 0
        metadata.num_prefills = 10
        metadata.slot_mapping = torch.zeros(10, dtype=torch.long)
        layer = self.layer_no_quant

        mock_get_forward_context.return_value = MagicMock(capturing=False)
        mock_npu_fused_infer_attention_score.return_value = (torch.ones(
            10, 8, 64), torch.ones(10, 8, 64))
        output = self.impl.forward(layer, query, key, value, kv_cache,
                                   metadata, output)

        mock_npu_fused_infer_attention_score.assert_called_once()
        assert output.shape == (10, 8, 64)

    @patch('vllm_ascend.attention.attention_v1.using_paged_attention')
    @patch('torch_npu._npu_paged_attention')
    @patch('torch_npu._npu_reshape_and_cache')
    @patch('vllm_ascend.ascend_forward_context.get_forward_context')
    def test_forward_paged_attention(self, mock_get_forward_context,
                                     mock_npu_reshape_and_cache,
                                     mock_paged_attention,
                                     mock_using_paged_attention):
        """Test forward pass in DecodeOnly state"""
        query = torch.randn(4, 8 * 64)
        key = torch.randn(4, 8 * 64)
        value = torch.randn(4, 8 * 64)
        kv_cache = torch.empty(2, 5, 128, 8, 64)
        output = torch.empty_like(query)

        metadata = self.attn_metadata
        metadata.attn_state = AscendAttentionState.DecodeOnly
        metadata.seq_lens = torch.tensor([4])
        metadata.block_tables = torch.zeros(1, 5, dtype=torch.long)
        metadata.num_actual_tokens = 4
        metadata.slot_mapping = torch.zeros(4, dtype=torch.long)
        metadata.num_decodes = 4
        metadata.num_prefills = 0
        layer = self.layer_no_quant
        mock_using_paged_attention.return_value = True

        mock_get_forward_context.return_value = MagicMock(capturing=False)

        output = self.impl.forward(layer, query, key, value, kv_cache,
                                   metadata, output)

        mock_paged_attention.assert_called_once()
        assert output.shape == (4, 8 * 64)

    @patch('vllm_ascend.ascend_forward_context.get_forward_context')
    @patch('torch_npu.npu_fused_infer_attention_score')
    @patch('torch_npu._npu_reshape_and_cache')
    def test_forward_decode_only_swa(self, mock_npu_reshape_and_cache,
                                     mock_fused_infer_attention_score,
                                     mock_get_forward_context):
        """Test forward pass in DecodeOnly state"""
        query = torch.randn(10, 8 * 64)
        key = torch.randn(10, 8 * 64)
        value = torch.randn(10, 8 * 64)
        kv_cache = torch.empty(2, 5, 128, 8, 64)
        output = torch.empty(10, 8, 64)

        mock_get_forward_context.return_value = MagicMock(capturing=False)

        metadata = self.attn_metadata
        metadata.attn_state = AscendAttentionState.DecodeOnly
        metadata.seq_lens = torch.tensor([10] * 10)
        metadata.block_tables = torch.zeros(1, 5, dtype=torch.long)
        metadata.num_actual_tokens = 100
        metadata.slot_mapping = torch.zeros(10, dtype=torch.long)
        metadata.num_decodes = 10
        metadata.num_prefills = 0
        layer = self.layer_no_quant
        mock_fused_infer_attention_score.return_value = (torch.ones(10, 8,
                                                                    64), 1)
        output = self.impl_swa.forward(layer, query, key, value, kv_cache,
                                       metadata, output)
        print(output.shape)
        mock_fused_infer_attention_score.assert_called_once()
        assert output.shape == (10, 8, 64)

    @patch('vllm_ascend.ascend_forward_context.get_forward_context')
    @patch('torch_npu._npu_paged_attention')
    @patch('torch_npu.npu_fused_infer_attention_score')
    @patch('torch_npu._npu_reshape_and_cache')
    def test_forward_decode_only_swa_seq_len_mismatch(
            self, mock_npu_reshape_and_cache, mock_fused_infer_attention_score,
            mock_paged_attention, mock_get_forward_context):
        """Test forward pass in DecodeOnly state when seq)len_mismatch"""
        query = torch.randn(10, 8, 64)
        key = torch.randn(10, 8, 64)
        value = torch.randn(10, 8, 64)
        kv_cache = torch.empty(2, 5, 128, 8, 64)
        output = torch.empty_like(query)

        metadata = self.attn_metadata
        metadata.attn_state = AscendAttentionState.DecodeOnly
        metadata.seq_lens = torch.tensor([10])  # len == 1 != query.size(0)==10
        metadata.block_tables = torch.zeros(1, 5, dtype=torch.long)
        metadata.num_actual_tokens = 10
        metadata.slot_mapping = torch.zeros(10, dtype=torch.long)
        layer = self.layer_no_quant
        metadata.num_decodes = 10
        metadata.num_prefills = 0
        metadata.actual_seq_lengths_q = [10]

        mock_get_forward_context.return_value = MagicMock(capturing=False)

        mock_fused_infer_attention_score.return_value = (torch.ones(10, 8, 64),
                                                         torch.ones(10, 8, 64))

        output = self.impl_swa.forward(layer, query, key, value, kv_cache,
                                       metadata, output)

        mock_paged_attention.assert_not_called()
        mock_fused_infer_attention_score.assert_called_once()

        assert output.shape == (10, 8, 64)
