# 上游 issue #1 备份：Codex 自动化测试反馈监控

> 备份文件, 用于 fork 仓库保留与原作者的协作历史.

> 来源: [xj-zhang2018/R-KV-vllm-ascend#1](https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1)
> 备份时间: 2026-06-09 06:31:09 UTC
> 原作者: @xj-zhang2018

## 元信息

- 标题: Codex 自动化测试反馈监控
- 作者: @xj-zhang2018
- 创建时间: 2026-06-05 02:14:28 UTC
- 最后更新: 2026-06-08 11:03:52 UTC
- 关闭时间: ?
- 状态: `open`
- 评论数 (issue metadata): 66
- HTML: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1

## Issue 正文

这个 Issue 用于接收真实环境中的自动化测试反馈。

请在评论中提供：
- 失败现象或测试输出
- 复现步骤
- 期望行为
- 相关环境信息

Codex 将通过本地 30 秒心跳监控这个 Issue 的最新回复。遇到可执行的代码问题时，会在本地修改代码、运行合适的验证、提交并推送到远端分支，然后在本 Issue 回复本次处理结果和后续操作方式。

## 评论时间线

本页共拉取到 **66 条** 评论 (按 id 升序, 即时间从早到晚).

### 评论 #1 — @xj-zhang2018 at 2026-06-05 02:15:50 UTC
- Comment id: `4627539816`
- Created: 2026-06-05 02:15:50 UTC
- Updated: 2026-06-05 02:15:50 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4627539816
- Author association: `OWNER`

监控已启动。

请直接在本 Issue 追加真实环境反馈，建议包含失败输出、复现步骤、期望行为和环境信息。Codex 的 30 秒心跳会检查新回复；如果反馈可执行，我会修改代码、运行可行验证、推送到远端 `codex/issue-1-feedback` 分支，并在这里回复处理摘要、验证结果和下一步操作方式。

如果信息不足，我会在这里回复需要补充的内容。

---

### 评论 #2 — @xj-zhang2018 at 2026-06-05 02:20:18 UTC
- Comment id: `4627558144`
- Created: 2026-06-05 02:20:18 UTC
- Updated: 2026-06-05 02:20:18 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4627558144
- Author association: `OWNER`

当前版本代码你修改了那些文件，请列举出修改的文件名和文件路径

---

### 评论 #3 — @xj-zhang2018 at 2026-06-05 02:21:00 UTC
- Comment id: `4627561078`
- Created: 2026-06-05 02:21:00 UTC
- Updated: 2026-06-05 02:21:00 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4627561078
- Author association: `OWNER`

目前没有修改任何仓库代码文件。

确认结果：
- 当前分支：`main`
- `git status --short --branch` 输出：`## main...origin/main`
- 代码修改文件：无
- 已提交/推送的代码变更：无

本轮只完成了自动化监控环境的搭建：创建了本 Issue、发布启动说明，并在本地维护 `.tmp/gh-issue-comment-monitor/xj-zhang2018-R-KV-vllm-ascend-1.json` 作为 Issue 回复 checkpoint。该 checkpoint 不是代码功能修改。

后续如果 Issue 中出现可执行的失败日志或需求反馈，我会在处理完成后回复具体修改的文件路径、验证结果、远端分支和 commit。

---

### 评论 #4 — @xj-zhang2018 at 2026-06-05 02:23:28 UTC
- Comment id: `4627571414`
- Created: 2026-06-05 02:23:28 UTC
- Updated: 2026-06-05 02:23:28 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4627571414
- Author association: `OWNER`

已完成第一版 vLLM-Ascend 适配，核心改动都在 `other_code/vllm-ascend-releases-v0.18.0` 下：

- 新增 Ascend 专用 R-KV 压缩器：[rkv.py](/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py:91)
- 在 Ascend attention 中接入每层 KV 压缩和 query window 缓存：[attention_v1.py](/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py:954)
- 在 runner 中维护“有效 KV 长度”，保持 RoPE/input position 使用原始长度，slot mapping 和 attention seq_len 使用压缩后长度：[model_runner_v1.py](/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/worker/model_runner_v1.py:410)
- 增加环境变量开关：[envs.py](/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py:113)

启用方式示例：

``​`bash
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=1024
export VLLM_ASCEND_RKV_BUFFER=128
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_KERNEL_SIZE=7
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
``​`

建议启动 vllm-ascend 时使用 eager 路径，例如加 `--enforce-eager`。当前第一版为稳健起见只启用普通 v1 DecodeOnly 场景：非 speculative、非 CP、非 DBO、非 ACL graph、非 MLA、单 KV-cache group。暂未做 block manager 旧块释放，所以主要收益是后续 attention 的有效 KV 长度下降带来的推理计算加速，不是显存块容量回收。

验证情况：已通过 `python3 -m py_compile` 语法检查。本地 Python 环境没有安装 `torch`，所以 CPU smoke test 和 Ascend 实机推理测试没有在这台环境里跑成。

---

### 评论 #5 — @xj-zhang2018 at 2026-06-05 02:24:10 UTC
- Comment id: `4627574900`
- Created: 2026-06-05 02:24:10 UTC
- Updated: 2026-06-05 02:24:10 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4627574900
- Author association: `OWNER`

收到这条第一版适配说明。当前评论里没有新的失败日志、复现步骤或明确的代码修改请求，因此本次心跳没有修改代码，也没有提交/推送新的 commit。

建议下一步操作：
1. 在安装了 `torch`、vLLM/vllm-ascend 依赖和 Ascend 运行环境的机器上启动真实推理验证。
2. 按评论中的环境变量启用 R-KV，并建议加 `--enforce-eager`。
3. 优先覆盖普通 v1 DecodeOnly 场景；暂时避开 speculative、CP、DBO、ACL graph、MLA、多 KV-cache group。
4. 如果出现失败，请在本 Issue 追加完整命令、环境变量、报错栈、模型/输入长度、是否开启 eager、以及期望行为。收到可复现反馈后，我会按监控流程修改代码、验证、推送远端分支，并在这里回复改动文件、commit 和后续操作。

---

### 评论 #6 — @xj-zhang2018 at 2026-06-05 02:25:40 UTC
- Comment id: `4627581207`
- Created: 2026-06-05 02:25:40 UTC
- Updated: 2026-06-05 02:25:40 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4627581207
- Author association: `OWNER`

当前版你的修改列表如下
other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py
other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py
other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/utils.py
/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py
/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/worker/model_runner_v1.py

---

### 评论 #7 — @xj-zhang2018 at 2026-06-05 02:26:35 UTC
- Comment id: `4627585212`
- Created: 2026-06-05 02:26:35 UTC
- Updated: 2026-06-05 02:26:35 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4627585212
- Author association: `OWNER`

收到这份当前版本修改文件列表，我已确认这些路径在仓库中都存在：

- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/utils.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/worker/model_runner_v1.py`

当前评论只是补充修改清单，没有新的失败日志、复现步骤或明确代码修改请求。本次心跳未修改代码，当前工作区仍为干净状态：`## main...origin/main`。

如需我继续处理，请追加具体测试失败、报错栈、复现命令或期望调整点。

---

### 评论 #8 — @xj-zhang2018 at 2026-06-05 02:28:10 UTC
- Comment id: `4627591601`
- Created: 2026-06-05 02:28:10 UTC
- Updated: 2026-06-05 02:28:10 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4627591601
- Author association: `OWNER`

当前版本vllm-ascend我应该如何拉起推理服务，让她生效r-kv算法

---

### 评论 #9 — @xj-zhang2018 at 2026-06-05 02:29:16 UTC
- Comment id: `4627596032`
- Created: 2026-06-05 02:29:16 UTC
- Updated: 2026-06-05 02:29:16 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4627596032
- Author association: `OWNER`

当前版本要让 R-KV 生效，关键是：启动 vLLM-Ascend 的 v1 eager DecodeOnly 路径，并在启动前设置 `VLLM_ASCEND_RKV_ENABLE=1` 和正数 `VLLM_ASCEND_RKV_BUDGET`。

可以先按下面方式拉起服务：

``​`bash
cd /path/to/vllm-ascend-releases-v0.18.0

# 如当前环境尚未安装本仓库版本，先安装/更新
pip install -e .

# 建议显式使用 v1 engine；较新 vllm-ascend 版本通常默认 v1，但显式设置便于排查
export VLLM_USE_V1=1

# 启用 R-KV
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=1024
export VLLM_ASCEND_RKV_BUFFER=128
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_KERNEL_SIZE=7
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last

# 用普通 decoder-only 模型先验证，例如 Qwen 类模型
vllm serve /path/to/model \
  --served-model-name rkv-test \
  --host 0.0.0.0 \
  --port 8000 \
  --enforce-eager \
  --max-model-len 4096 \
  --max-num-seqs 8
``​`

请求示例：

``​`bash
curl http://127.0.0.1:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "rkv-test",
    "prompt": "这里放一段长 prompt，长度最好超过 budget + buffer 后再观察 R-KV 压缩是否触发。",
    "max_tokens": 64,
    "temperature": 0
  }'
``​`

注意条件：
- R-KV 当前只在 v1 `DecodeOnly` attention 路径生效。prefill 阶段不会压缩，进入 decode 后且有效 KV 长度达到 `budget + buffer` 才会触发。
- `VLLM_ASCEND_RKV_BUDGET` 必须大于 0；设为 1024 时，默认 buffer 128，通常 seq_len 到 1152 左右以后才会尝试压缩。
- 第一版建议先用普通 decoder-only dense 模型验证，例如 Qwen；先避开 speculative、CP、DBO、ACL graph、MLA、encoder-decoder、sliding-window、pooling、多 KV-cache group 等场景。
- 建议保留 `--enforce-eager`，因为代码里 runtime guard 会避开 graph/capturing 路径。
- 这版主要降低后续 attention 使用的有效 KV 长度；暂未释放 block manager 旧块，所以不要预期显存块容量立刻回收。

本次是使用方式答复，没有修改代码。如果按上述方式启动后出现报错，请继续贴完整启动命令、环境变量、模型名、prompt 长度和报错栈，我会继续按反馈修改代码。

---

### 评论 #10 — @sunao2000123 at 2026-06-05 06:19:19 UTC
- Comment id: `4628785975`
- Created: 2026-06-05 06:19:19 UTC
- Updated: 2026-06-05 06:19:19 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4628785975
- Author association: `NONE`

我跑了你第一版的代码，但是报错了。这是我的拉起方式“export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=1024
export VLLM_ASCEND_RKV_BUFFER=128
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_KERNEL_SIZE=7
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last


vllm serve /softwarePlatform/z00872399/Qwen/Qwen3-32B \
        --max-model-len 45000 \
        --served-model-name Qwen3-32B \
        --tensor-parallel-size 4 \
        --pipeline-parallel-size 2 \
        --gpu-memory-utilization 0.9 \
        --block-size 128 \
        --distributed-executor-backend mp \
        --trust-remote-code \
        --port 8000 \
        --enforce-eager \”

这是vllm ascend的报错日志：“(Worker pid=1944) INFO 06-05 06:06:07 [cpu_binding.py:381] NPU5: main=[26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45]  acl=[46]  release=[[47]]                                                                                            
(Worker pid=1942) INFO 06-05 06:06:08 [cpu_binding.py:403] [migrate] NPU:3 -> NUMA [5]                                                                                                                                                                   
(Worker pid=1944) INFO 06-05 06:06:08 [cpu_binding.py:403] [migrate] NPU:5 -> NUMA [1]                                                                                                                                                                   
(Worker pid=1941) INFO 06-05 06:06:08 [cpu_binding.py:329] [cpu_bind_mode] mode=topo_affinity rank=2 visible_npus=[0, 1, 2, 3, 4, 5, 6, 7]                                                                                                               
(Worker pid=1941) INFO 06-05 06:06:08 [cpu_binding.py:376] The CPU allocation plan is as follows:                                                                                                                                                        
(Worker pid=1941) INFO 06-05 06:06:08 [cpu_binding.py:381] NPU2: main=[98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117]  acl=[118]  release=[[119]]                                                                        
(Worker pid=1941) INFO 06-05 06:06:08 [cpu_binding.py:403] [migrate] NPU:2 -> NUMA [4]                                                                                                                                                                   
(Worker pid=1944) INFO 06-05 06:06:13 [cpu_binding.py:497] NPU5(PCI 0000:02:00.0): sq_send_trigger_irq IRQ_ID=1856 -> CPU24, cq_update_irq IRQ_ID=1857 -> CPU25                                                                                          
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852] WorkerProc failed to start.                                                                                                                                                           
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852] Traceback (most recent call last):                                                                                                                                                    
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 821, in worker_main                                                                                        
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     worker = WorkerProc(*args, **kwargs)                                                                                                                                              
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                                              
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/tracing/otel.py", line 178, in sync_wrapper                                                                                                         
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     return func(*args, **kwargs)                                                                                                                                                      
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]            ^^^^^^^^^^^^^^^^^^^^^                                                                                                                                                      
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/patch/platform/patch_multiproc_executor.py", line 200, in __init__                                                                    
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     self.worker.init_device()                                                                                                                                                         
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/v1/worker/worker_base.py", line 312, in init_device                                                                                                 
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     self.worker.init_device()  # type: ignore                                                                                                                                         
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     ^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                                                         
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/worker.py", line 324, in init_device                                                                                           
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     self.model_runner = NPUModelRunner(self.vllm_config, self.device)                                                                                                                 
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                 
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/model_runner_v1.py", line 419, in __init__                                                                                     
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     and len(self.kv_cache_config.kv_cache_groups) == 1                                                                                                                                
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852]             ^^^^^^^^^^^^^^^^^^^^                                                                                                                                                      
(Worker pid=1944) ERROR 06-05 06:06:13 [multiproc_executor.py:852] AttributeError: 'NPUModelRunner' object has no attribute 'kv_cache_config'                                                                                                            
(Worker pid=1945) INFO 06-05 06:06:13 [cpu_binding.py:497] NPU6(PCI 0000:41:00.0): sq_send_trigger_irq IRQ_ID=2113 -> CPU48, cq_update_irq IRQ_ID=2114 -> CPU49                                                                                          
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852] WorkerProc failed to start.                                                                                                                                                           
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852] Traceback (most recent call last):                                                                                                                                                    
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 821, in worker_main                                                                                        
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     worker = WorkerProc(*args, **kwargs)                                                                                                                                              
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                                              
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/tracing/otel.py", line 178, in sync_wrapper                                                                                                         
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     return func(*args, **kwargs)                                                                                                                                                      
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]            ^^^^^^^^^^^^^^^^^^^^^                                                                                                                                                      
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/patch/platform/patch_multiproc_executor.py", line 200, in __init__                                                                    
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     self.worker.init_device()                                                                                                                                                         
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/v1/worker/worker_base.py", line 312, in init_device                                                                                                 
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     self.worker.init_device()  # type: ignore                                                                                                                                         
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     ^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                                                         
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/worker.py", line 324, in init_device                                                                                           
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]     self.model_runner = NPUModelRunner(self.vllm_config, self.device)                                                                                                                 
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                 
(Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/model_runner_v1.py", line 419, in __init__   (Worker pid=1945) ERROR 06-05 06:06:13 [multiproc_executor.py:852] AttributeError: 'NPUModelRunner' object has no attribute 'kv_cache_config'
(Worker pid=1943) INFO 06-05 06:06:14 [cpu_binding.py:497] NPU4(PCI 0000:01:00.0): sq_send_trigger_irq IRQ_ID=1600 -> CPU0, cq_update_irq IRQ_ID=1601 -> CPU1
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852] WorkerProc failed to start.
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852] Traceback (most recent call last):
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 821, in worker_main
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]     worker = WorkerProc(*args, **kwargs)
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/tracing/otel.py", line 178, in sync_wrapper
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]     return func(*args, **kwargs)
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]            ^^^^^^^^^^^^^^^^^^^^^
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/patch/platform/patch_multiproc_executor.py", line 200, in __init__
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]     self.worker.init_device()
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/v1/worker/worker_base.py", line 312, in init_device
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]     self.worker.init_device()  # type: ignore
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]     ^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/worker.py", line 324, in init_device
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]     self.model_runner = NPUModelRunner(self.vllm_config, self.device)
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/model_runner_v1.py", line 419, in __init__
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]     and len(self.kv_cache_config.kv_cache_groups) == 1
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852]             ^^^^^^^^^^^^^^^^^^^^
(Worker pid=1943) ERROR 06-05 06:06:14 [multiproc_executor.py:852] AttributeError: 'NPUModelRunner' object has no attribute 'kv_cache_config'
(Worker pid=1939) INFO 06-05 06:06:15 [cpu_binding.py:497] NPU0(PCI 0000:c1:00.0): sq_send_trigger_irq IRQ_ID=3138 -> CPU144, cq_update_irq IRQ_ID=3139 -> CPU145
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852] WorkerProc failed to start.
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852] Traceback (most recent call last):
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 821, in worker_main
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]     worker = WorkerProc(*args, **kwargs)
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/tracing/otel.py", line 178, in sync_wrapper
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]     return func(*args, **kwargs)
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]            ^^^^^^^^^^^^^^^^^^^^^
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/patch/platform/patch_multiproc_executor.py", line 200, in __init__
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]     self.worker.init_device()
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]   File "/vllm-workspace/vllm/vllm/v1/worker/worker_base.py", line 312, in init_device
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]     self.worker.init_device()  # type: ignore
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]     ^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/worker.py", line 324, in init_device
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]     self.model_runner = NPUModelRunner(self.vllm_config, self.device)
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/model_runner_v1.py", line 419, in __init__
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]     and len(self.kv_cache_config.kv_cache_groups) == 1
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852]             ^^^^^^^^^^^^^^^^^^^^
(Worker pid=1939) ERROR 06-05 06:06:15 [multiproc_executor.py:852] AttributeError: 'NPUModelRunner' object has no attribute 'kv_cache_config'
(Worker pid=1940) INFO 06-05 06:06:15 [cpu_binding.py:497] NPU1(PCI 0000:c2:00.0): sq_send_trigger_irq IRQ_ID=3394 -> CPU168, cq_update_irq IRQ_ID=3395 -> CPU169(EngineCore pid=1925) ERROR 06-05 06:06:21 [core.py:1099] Exception: WorkerProc initialization failed due to an exception in a background process. See stack trace for root cause.
(EngineCore pid=1925) Process EngineCore:
(EngineCore pid=1925) Traceback (most recent call last):
(EngineCore pid=1925)   File "/usr/local/python3.11.14/lib/python3.11/multiprocessing/process.py", line 314, in _bootstrap
(EngineCore pid=1925)     self.run()
(EngineCore pid=1925)   File "/usr/local/python3.11.14/lib/python3.11/multiprocessing/process.py", line 108, in run
(EngineCore pid=1925)     self._target(*self._args, **self._kwargs)
(EngineCore pid=1925)   File "/vllm-workspace/vllm/vllm/v1/engine/core.py", line 1103, in run_engine_core
(EngineCore pid=1925)     raise e
(EngineCore pid=1925)   File "/vllm-workspace/vllm/vllm/v1/engine/core.py", line 1073, in run_engine_core
(EngineCore pid=1925)     engine_core = EngineCoreProc(*args, engine_index=dp_rank, **kwargs)
(EngineCore pid=1925)                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=1925)   File "/vllm-workspace/vllm/vllm/tracing/otel.py", line 178, in sync_wrapper
(EngineCore pid=1925)     return func(*args, **kwargs)
(EngineCore pid=1925)            ^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=1925)   File "/vllm-workspace/vllm/vllm/v1/engine/core.py", line 839, in __init__
(EngineCore pid=1925)     super().__init__(
(EngineCore pid=1925)   File "/vllm-workspace/vllm/vllm/v1/engine/core.py", line 112, in __init__
(EngineCore pid=1925)     self.model_executor = executor_class(vllm_config)
(EngineCore pid=1925)                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=1925)   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 101, in __init__
(EngineCore pid=1925)     super().__init__(vllm_config)
(EngineCore pid=1925)   File "/vllm-workspace/vllm/vllm/tracing/otel.py", line 178, in sync_wrapper
(EngineCore pid=1925)     return func(*args, **kwargs)
(EngineCore pid=1925)            ^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=1925)   File "/vllm-workspace/vllm/vllm/v1/executor/abstract.py", line 103, in __init__
(EngineCore pid=1925)     self._init_executor()
(EngineCore pid=1925)   File "/vllm-workspace/vllm-ascend/vllm_ascend/patch/platform/patch_multiproc_executor.py", line 104, in _init_executor
(EngineCore pid=1925)     self.workers = AscendWorkerProc.wait_for_ready(unready_workers)
(EngineCore pid=1925)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=1925)   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 731, in wait_for_ready
(EngineCore pid=1925)     raise e from None
(EngineCore pid=1925) Exception: WorkerProc initialization failed due to an exception in a background process. See stack trace for root cause.
(APIServer pid=1905) Traceback (most recent call last):
(APIServer pid=1905)   File "/usr/local/python3.11.14/bin/vllm", line 6, in <module>
(APIServer pid=1905)     sys.exit(main())
(APIServer pid=1905)              ^^^^^^
(APIServer pid=1905)   File "/vllm-workspace/vllm/vllm/entrypoints/cli/main.py", line 75, in main
(APIServer pid=1905)     args.dispatch_function(args)
(APIServer pid=1905)   File "/vllm-workspace/vllm/vllm/entrypoints/cli/serve.py", line 118, in cmd
(APIServer pid=1905)     uvloop.run(run_server(args))
(APIServer pid=1905)   File "/usr/local/python3.11.14/lib/python3.11/site-packages/uvloop/__init__.py", line 92, in run
(APIServer pid=1905)     return runner.run(wrapper())
(APIServer pid=1905)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1905)   File "/usr/local/python3.11.14/lib/python3.11/asyncio/runners.py", line 118, in run
(APIServer pid=1905)     return self._loop.run_until_complete(task)
(APIServer pid=1905)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1905)   File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
(APIServer pid=1905)   File "/usr/local/python3.11.14/lib/python3.11/site-packages/uvloop/__init__.py", line 48, in wrapper”

怎么改

---

### 评论 #11 — @xj-zhang2018 at 2026-06-05 06:23:54 UTC
- Comment id: `4628808018`
- Created: 2026-06-05 06:23:54 UTC
- Updated: 2026-06-05 06:23:54 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4628808018
- Author association: `OWNER`

已定位并修复这个启动报错。

原因是第一版在 `NPUModelRunner.__init__` 里判断 R-KV 是否可用时访问了 `self.kv_cache_config.kv_cache_groups`，但 `kv_cache_config` 要到 `initialize_kv_cache()` 阶段才会初始化，所以 worker 启动时会直接抛：

``​`text
AttributeError: 'NPUModelRunner' object has no attribute 'kv_cache_config'
``​`

处理方式：
- 移除了 `__init__` 阶段对 `self.kv_cache_config` 的访问。
- 在 `initialize_kv_cache()` 中 KV cache groups 完成整理后，再检查 R-KV 当前是否只面对单个 KV cache group。
- 如果不是单个 KV cache group，现在会打印 warning 并自动关闭 R-KV，而不是启动崩溃。

验证：

``​`bash
python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/worker/model_runner_v1.py
``​`

已通过。

远端分支：`codex/issue-1-feedback`
提交：`32a8a548ed309eb823bcba77ff385fb7e53c0fc1`

你可以这样拉取测试：

``​`bash
git fetch origin codex/issue-1-feedback
git checkout codex/issue-1-feedback
``​`

然后用你上面同样的环境变量和 `vllm serve` 命令重试。如果之后日志里出现 “R-KV is disabled because it only supports a single KV cache group” 这类 warning，说明这次拓扑/模型布局下生成了多个 KV cache group，当前 R-KV 会安全跳过；那就需要下一步扩展多 KV cache group 支持。


---

### 评论 #12 — @sunao2000123 at 2026-06-05 06:25:24 UTC
- Comment id: `4628815599`
- Created: 2026-06-05 06:25:24 UTC
- Updated: 2026-06-05 06:25:24 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4628815599
- Author association: `NONE`

所以，当前版本代码你修改了那些文件，请列举出修改的文件名和文件路径

---

### 评论 #13 — @xj-zhang2018 at 2026-06-05 06:26:31 UTC
- Comment id: `4628821829`
- Created: 2026-06-05 06:26:31 UTC
- Updated: 2026-06-05 06:26:31 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4628821829
- Author association: `OWNER`

当前这个修复提交只修改了 1 个文件：

| 文件名 | 仓库内路径 |
| --- | --- |
| `model_runner_v1.py` | `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/worker/model_runner_v1.py` |

对应提交：`32a8a548ed309eb823bcba77ff385fb7e53c0fc1`

这次没有改 `attention_v1.py`、`envs.py` 或其他文件。主要改动点是在 `model_runner_v1.py` 中把 R-KV 对 `kv_cache_groups` 的检查从 `NPUModelRunner.__init__` 阶段移到 `initialize_kv_cache()` 阶段，避免启动时 `kv_cache_config` 尚未初始化导致 AttributeError。


---

### 评论 #14 — @xj-zhang2018 at 2026-06-05 06:31:35 UTC
- Comment id: `4628850632`
- Created: 2026-06-05 06:31:35 UTC
- Updated: 2026-06-05 06:31:35 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4628850632
- Author association: `OWNER`

以后修改代码不需要创建新的分支了，保持当前分支不要变了，在这个分支继续演进下去就行了。codex/issue-1-feedback

---

### 评论 #15 — @xj-zhang2018 at 2026-06-05 06:38:29 UTC
- Comment id: `4628890636`
- Created: 2026-06-05 06:38:29 UTC
- Updated: 2026-06-05 06:38:29 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4628890636
- Author association: `OWNER`

收到，后续代码修改会保持并复用当前 `codex/issue-1-feedback` 分支继续演进，不再新建新的工作分支；提交后仍会 push 到 origin 并在这里同步 commit 和验证结果。

---

### 评论 #16 — @sunao2000123 at 2026-06-05 06:58:06 UTC
- Comment id: `4629001955`
- Created: 2026-06-05 06:58:06 UTC
- Updated: 2026-06-05 06:58:06 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4629001955
- Author association: `NONE`

基于你的版本，我已经成功拉起了，但vllm会显示“(APIServer pid=4839) WARNING 06-05 06:53:11 [envs.py:1717] Unknown vLLM environment variable detected: VLLM_ASCEND_RKV_BUDGET
(APIServer pid=4839) WARNING 06-05 06:53:11 [envs.py:1717] Unknown vLLM environment variable detected: VLLM_ASCEND_RKV_WINDOW_SIZE
(APIServer pid=4839) WARNING 06-05 06:53:11 [envs.py:1717] Unknown vLLM environment variable detected: VLLM_ASCEND_RKV_RETAIN_RATIO
(APIServer pid=4839) WARNING 06-05 06:53:11 [envs.py:1717] Unknown vLLM environment variable detected: VLLM_ASCEND_RKV_RETAIN_DIRECTION
(APIServer pid=4839) WARNING 06-05 06:53:11 [envs.py:1717] Unknown vLLM environment variable detected: VLLM_ASCEND_RKV_KERNEL_SIZE
(APIServer pid=4839) WARNING 06-05 06:53:11 [envs.py:1717] Unknown vLLM environment variable detected: VLLM_ASCEND_RKV_BUFFER
(APIServer pid=4839) WARNING 06-05 06:53:11 [envs.py:1717] Unknown vLLM environment variable detected: VLLM_ASCEND_RKV_MIX_LAMBDA”
我在怀疑vllmascend在拉起的时候走进rkv的核心代码了吗，为什么是Unknown vLLM environment variable detected

---

### 评论 #17 — @xj-zhang2018 at 2026-06-05 07:05:06 UTC
- Comment id: `4629043046`
- Created: 2026-06-05 07:05:06 UTC
- Updated: 2026-06-05 07:05:06 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4629043046
- Author association: `OWNER`

已处理这个环境变量告警问题。

判断结果：R-KV 代码路径是否启用，仍然由 vllm-ascend 里的 `VLLM_ASCEND_RKV_ENABLE` 和 `VLLM_ASCEND_RKV_BUDGET` 控制；这次看到的 `Unknown vLLM environment variable detected` 是 vLLM 核心的环境变量检查器不认识新增的 R-KV 变量，并不代表 vllm-ascend 一定没有读取到这些变量。不过这个 warning 会造成误导，所以我做了修复。

处理内容：
- 新增 `vllm_ascend/patch/platform/patch_envs.py`，在 vllm-ascend platform patch 阶段把 `vllm_ascend.envs.env_variables` 注册到 `vllm.envs.env_variables`。
- 使用 `setdefault` 注册，避免覆盖 vLLM 自己已经存在的变量定义。
- 在 platform patch 入口优先加载这个 env registry bridge。
- 补了一个不依赖真实 vLLM 安装的测试，验证 Ascend/R-KV 变量会进入 vLLM registry，且已有变量不会被覆盖。

验证结果：
- `python3 -m py_compile .../patch_envs.py .../patch/platform/__init__.py .../patch/__init__.py .../tests/ut/test_envs.py` 通过。
- 隔离脚本用 fake `vllm.envs` 验证通过：29 个 vllm-ascend 环境变量都能注册进去，且不会覆盖已有项。
- 本地尝试运行 `python3 -m unittest tests.ut.test_envs.TestEnvVariables.test_env_vars_registered_to_vllm` 时，环境缺少 `pytest`，测试框架未能启动；不是新增逻辑失败。

远端分支：`codex/issue-1-feedback`
提交：`943f851e Register Ascend env vars with vLLM`

你可以拉取该分支后再次启动。如果仍看到 R-KV 变量的 unknown warning，请贴一下最新完整启动命令、环境变量和启动日志；如果 warning 消失但怀疑 R-KV 没实际生效，我再继续帮你加更明确的 R-KV 启用日志或检查执行路径。


---

### 评论 #18 — @sunao2000123 at 2026-06-05 08:10:05 UTC
- Comment id: `4629489815`
- Created: 2026-06-05 08:10:05 UTC
- Updated: 2026-06-05 08:10:05 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4629489815
- Author association: `NONE`

我跑出来了，现在相同的拉起方式“export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=1024
export VLLM_ASCEND_RKV_BUFFER=128
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_KERNEL_SIZE=7
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last


vllm serve /softwarePlatform/z00872399/Qwen/Qwen3-32B \
        --max-model-len 45000 \
        --served-model-name Qwen3-32B \
        --tensor-parallel-size 4 \
        --pipeline-parallel-size 2 \
        --gpu-memory-utilization 0.9 \
        --block-size 128 \
        --distributed-executor-backend mp \
        --trust-remote-code \
        --port 8000 \
”，这张表是我用你的vllmascend rkv的方式的性能
 E2EL                     │ total   │ 66403.1 ms     │ 66321.1 ms      │ 66490.3 ms    │ 66415.7 ms     │ 66445.7 ms     │ 66468.4 ms     │ 66488.1 ms      │ 10  │                                                                                     
├──────────────────────────┼─────────┼────────────────┼─────────────────┼───────────────┼────────────────┼────────────────┼────────────────┼─────────────────┼─────┤                                                                                     
│ TTFT                     │ total   │ 306.3 ms       │ 126.8 ms        │ 448.4 ms      │ 311.3 ms       │ 338.4 ms       │ 444.5 ms       │ 448.0 ms        │ 10  │                                                                                     
├──────────────────────────┼─────────┼────────────────┼─────────────────┼───────────────┼────────────────┼────────────────┼────────────────┼─────────────────┼─────┤                                                                                     
│ TPOT                     │ total   │ 64.6 ms        │ 64.5 ms         │ 64.7 ms       │ 64.6 ms        │ 64.7 ms        │ 64.7 ms        │ 64.7 ms         │ 10  │  


这张表是相同的拉起方式，把rkv关掉的性能。也就是基线base
═════════════════════════╪═════════╪═════════════════╪═════════════════╪═════════════════╪═════════════════╪═════════════════╪═════════════════╪═════════════════╪═════╡
│ E2EL                     │ total   │ 60977.2 ms      │ 60440.5 ms      │ 61448.9 ms      │ 61043.6 ms      │ 61155.5 ms      │ 61355.6 ms      │ 61439.6 ms      │ 10  │
├──────────────────────────┼─────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────┤
│ TTFT                     │ total   │ 7347.1 ms       │ 197.8 ms        │ 14324.2 ms      │ 7492.8 ms       │ 10784.0 ms      │ 12997.4 ms      │ 14191.5 ms      │ 10  │
├──────────────────────────┼─────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────┤
│ TPOT                     │ total   │ 52.4 ms         │ 46.1 ms         │ 58.9 ms         │ 52.4 ms         │ 55.7 ms         │ 57.6 ms         │ 58.8 ms         │ 10  │
├──────────────────────────┼─────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────┤

你看base的ttft和tpot比rkv快，你自己改一改，看看哪里出问题了，然后以后修改代码的时候一定要把完整的你修改过的文件路径发给我 我好double check

---

### 评论 #19 — @xj-zhang2018 at 2026-06-05 08:19:27 UTC
- Comment id: `4629550710`
- Created: 2026-06-05 08:19:27 UTC
- Updated: 2026-06-05 08:19:27 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4629550710
- Author association: `OWNER`

已根据这组性能反馈在 `codex/issue-1-feedback` 上继续改了一版：`7758be717fa8e81f80a1703e7f832fde03ec79cb`。

我先校对了一下表格：这组数据里 RKV 的 TTFT 平均值是 `306.3 ms`，关闭 RKV 的 base 是 `7347.1 ms`，所以 TTFT 平均值其实是 RKV 更快；当前主要问题是 RKV 的 TPOT (`64.6 ms`) 和 E2EL (`66403.1 ms`) 比 base (`52.4 ms` / `60977.2 ms`) 慢。

这次修改内容：
- 只在当前 batch 确认为 `DecodeOnly` 且 RKV runtime 可用时，才传递/消费 `rkv_req_ids`，避免 prefill / chunked prefill 的每层 attention 进入 RKV query-cache 路径。
- RKV 压缩现在会等到攒满 `VLLM_ASCEND_RKV_WINDOW_SIZE` 个 decode query 后再触发，避免长 prompt 的首个 decode token 用过短观察窗口触发整段 KV gather/update/write。
- 增加了对应单测，覆盖“非 decode 不更新 query cache”和“未满 window 不压缩”。

验证结果：
- 通过：`python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/worker/model_runner_v1.py other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`
- 通过：`git diff --check`
- 受阻：本机当前 Python 环境没有 `torch`，所以新增的 targeted unittest 在导入阶段失败：`ModuleNotFoundError: No module named 'torch'`，不是测试断言失败。

完整修改文件路径：
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/worker/model_runner_v1.py`
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`

远端分支：`origin/codex/issue-1-feedback`

可以拉取这个分支后用同一套启动参数再跑一次性能表，重点看 TPOT/E2EL 是否回落。


---

### 评论 #20 — @sunao2000123 at 2026-06-05 09:24:33 UTC
- Comment id: `4630049343`
- Created: 2026-06-05 09:24:33 UTC
- Updated: 2026-06-05 09:24:33 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4630049343
- Author association: `NONE`

你现在这个性能很奇怪，我拉起一次你的vllm，然后测了两次aisbench。在同次的拉起vllm rkv中。第一次
的性能： E2E：61115.7 TTFT:  7425.9 TPOT：52.5
我第二次用相同的aisbench的性能测试：E2E：47622.8 TTFT:  247.3 TPOT：46.3
你看这个就是bug理论上说 第一次和第二次的aisbench在相同的vllm拉起里面，e2e和ttft都应该大差不差。但你第一次的ttft是7425.第二次是247.明显是有bug，ttft怎么可能就247

---

### 评论 #21 — @xj-zhang2018 at 2026-06-05 09:34:59 UTC
- Comment id: `4630120421`
- Created: 2026-06-05 09:34:59 UTC
- Updated: 2026-06-05 09:34:59 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4630120421
- Author association: `OWNER`

已处理这条 TTFT 第二次异常偏低的反馈。

判断：这个现象很像同一 vLLM 进程内第二次 aisbench 命中了 prefix cache。R-KV 会原地压缩/改写 KV cache block，和 prefix caching 复用相同 prompt 的 KV block 不兼容，所以第二轮 TTFT 可能被不真实地拉低到几百 ms。理论上 RKV 下连续两轮相同压测不应该出现第一次 TTFT 7425 ms、第二次 TTFT 247 ms 这种差异。

本次修复：
- 当 `VLLM_ASCEND_RKV_ENABLE=True` 且 `VLLM_ASCEND_RKV_BUDGET > 0` 时，在 Ascend platform config 兼容性检查阶段自动关闭 prefix caching，并打印 warning，避免复用被 RKV 原地改写过的 KV blocks。
- 对 RKV 的 per-request 状态补了 reset：新调度请求、finished 请求、preempted 请求都会清理 `rkv_effective_kv_lens`，并把 req_id 传到 attention 层清理 query window cache。
- attention 层在 decode 前会丢弃这些 reset req_id 的 `rkv_query_cache`，避免同一 vLLM 进程里 req_id 被重用时继承旧窗口。
- 增加了对应单测覆盖 prefix cache 禁用、req_id 重用清理、finished/preempted/new request 的 RKV 状态重置。

验证：
- 通过：`python3 -m py_compile` 覆盖本次修改的源码和测试文件。
- 通过：`git diff --check`。
- 受本机环境限制未跑通：`python3 -m unittest tests.ut.attention.test_attention_v1 tests.ut.worker.test_model_runner_v1 tests.ut.test_platform`，失败原因是本地缺少 `torch` 和 `pytest`；单独导入完整工程也缺少 `vllm`。

已推送：
- 分支：`codex/issue-1-feedback`
- commit：`4e032c3b Fix RKV prefix-cache reuse`

修改文件：
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/platform.py`
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/worker/model_runner_v1.py`
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/utils.py`
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/tests/ut/worker/test_model_runner_v1.py`
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_platform.py`

请拉取 `codex/issue-1-feedback` 后，在同一次 vLLM 拉起里再连续跑两次相同 aisbench。RKV 开启时 prefix cache 会自动关闭，预期两轮 TTFT/E2E 应该回到同量级；如果仍有大幅差异，请继续贴完整启动参数和两轮 aisbench 命令。

---

### 评论 #22 — @sunao2000123 at 2026-06-06 02:40:10 UTC
- Comment id: `4637090747`
- Created: 2026-06-06 02:40:10 UTC
- Updated: 2026-06-06 02:40:10 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637090747
- Author association: `NONE`

基线性能： E2E：60977    TTFT:  7347.2   TPOT：52.1  
你自己写的最新rkv性能：E2E：88883.1067    TTFT:   8779.3       TPOT：76.4  
请迭代你的rkv版本，你的rkv比基线慢很多。最终效果是要比基线快很多。


---

### 评论 #23 — @xj-zhang2018 at 2026-06-06 02:54:51 UTC
- Comment id: `4637138126`
- Created: 2026-06-06 02:54:51 UTC
- Updated: 2026-06-06 02:54:51 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637138126
- Author association: `OWNER`

已根据这条性能反馈继续迭代 R-KV：`af6ff31e` 已推送到 `codex/issue-1-feedback`。

本次主要降低 R-KV 在常态 decode 下的额外开销：
- R-KV helper 只在 `DecodeOnly` 路径进入，避免 prefill/TTFT 路径每层做无效 R-KV 判定。
- query window cache 只在接近下一次压缩阈值时开始维护，也就是 `budget + buffer - window_size + 1` 之后才缓存。
- 当请求还远离压缩阈值时会清理旧 query cache，压缩成功后也立即清理该请求的 cache，避免后续 decode 一直承担 `torch.cat`/缓存维护成本。
- 补了对应单测覆盖：低于阈值不缓存、接近阈值才缓存、压缩后清理 query cache。

验证结果：
- `git diff --check` 通过。
- `python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py` 通过。
- `python3 -m unittest tests.ut.attention.test_attention_v1` 在当前本地环境无法执行，导入阶段缺少 `torch`：`ModuleNotFoundError: No module named 'torch'`。

请基于最新 `codex/issue-1-feedback` 重新跑 E2E/TTFT/TPOT。如果仍然慢于基线，请把最新三项指标和测试配置继续贴上来，我会继续针对实测瓶颈迭代。


---

### 评论 #24 — @sunao2000123 at 2026-06-06 02:56:17 UTC
- Comment id: `4637141882`
- Created: 2026-06-06 02:56:17 UTC
- Updated: 2026-06-06 02:56:17 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637141882
- Author association: `NONE`

你修改代码的时候一定要把完整的你修改过的文件路径发给我 我好double check

---

### 评论 #25 — @xj-zhang2018 at 2026-06-06 02:56:48 UTC
- Comment id: `4637143058`
- Created: 2026-06-06 02:56:48 UTC
- Updated: 2026-06-06 02:56:48 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637143058
- Author association: `OWNER`

收到，后续每次修改代码我都会在 Issue 回复里附上完整文件路径，方便你 double check。

本次 `af6ff31e` 修改过的文件完整路径是：
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`


---

### 评论 #26 — @sunao2000123 at 2026-06-06 03:14:36 UTC
- Comment id: `4637195501`
- Created: 2026-06-06 03:14:36 UTC
- Updated: 2026-06-06 03:14:36 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637195501
- Author association: `NONE`

基线性能： E2E：60977    TTFT:  7347.2   TPOT：52.1  
最新rkv性能：E2E：62589.4 TTFT:   8915.3 TPOT：52.5

你现在的性能几乎和基线持平，但还是很不应该的，因为你开启了rkv，看到会比基线要快很多。你现在第一一定要确保rkv的核心算法要使能，第二一定要确保开启rkv后要比base快很多

---

### 评论 #27 — @xj-zhang2018 at 2026-06-06 03:20:35 UTC
- Comment id: `4637211453`
- Created: 2026-06-06 03:20:35 UTC
- Updated: 2026-06-06 03:20:35 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637211453
- Author association: `OWNER`

已根据这轮性能反馈继续处理，重点是确保 RKV 核心压缩逻辑更早真正使能。

处理摘要：
- 修正 `_maybe_compress_rkv()` 的触发条件：当序列长度达到 RKV 触发阈值后，只要当前请求已经缓存到至少 1 个 decode query，就立即调用 `RKVCompressor.update_kv()`，不再等待满 `window_size=8` 个 query。
- 之前的等待窗口会导致长 prefill 后 decode 阶段延迟 8 步才进入核心压缩，短输出场景甚至可能看不到压缩收益；现在会在第一个可压缩 decode step 就压缩 KV，让后续 decode 更早使用压缩后的有效 KV 长度。
- 更新了对应单测，覆盖“只有 1 个可用 query 时也会执行 gather/update/write”的路径，避免之后又退回到等待整窗。

验证结果：
- `git diff --check`：通过
- `python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`：通过
- `python3 -m unittest tests.ut.attention.test_attention_v1`：当前本地环境缺少 `torch`，导入阶段阻塞：`ModuleNotFoundError: No module named 'torch'`

远端分支：`codex/issue-1-feedback`
提交：`6a1d7ea03c7244dbf0dddbd028888e6a72788124`

完整修改文件路径：
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`

请基于最新 `codex/issue-1-feedback` 重新跑一次 E2E / TTFT / TPOT。如果开启 RKV 后仍然没有明显快于 base，请把新指标和运行参数继续贴上来，我会继续沿着“核心压缩是否命中 + 有效 KV 长度是否传入 decode kernel”这条链路查。


---

### 评论 #28 — @sunao2000123 at 2026-06-06 03:31:08 UTC
- Comment id: `4637234486`
- Created: 2026-06-06 03:31:08 UTC
- Updated: 2026-06-06 03:31:08 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637234486
- Author association: `NONE`

基线性能： E2E：62676.8    TTFT:  8883.5 TPOT：52.6
你的最新rkv性能：E2E：62589.4 TTFT:   8915.3 TPOT：52.5

这两个几乎一样了啊，但这肯定是不可能的，我觉得不应该把你要看的方向关注在这一块“修正 _maybe_compress_rkv() 的触发条件：当序列长度达到 RKV 触发阈值后，只要当前请求已经缓存到至少 1 个 decode query，就立即调用 RKVCompressor.update_kv()，不再等待满 window_size=8 个 query。” 因为我的输入是10k的长度，看到会触发压缩。检验你自己好好仔细排查一下。一个好的使能的rkv 不可能tpot跟base是一样的

---

### 评论 #29 — @xj-zhang2018 at 2026-06-06 03:41:36 UTC
- Comment id: `4637256208`
- Created: 2026-06-06 03:41:36 UTC
- Updated: 2026-06-06 03:41:36 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637256208
- Author association: `OWNER`

收到，这个反馈是对的：10k 输入下本来就会很快达到触发长度，所以继续只盯 `_maybe_compress_rkv()` 的触发阈值不是关键方向。

我重新顺着实际生效链路查了一遍，找到更像根因的问题：`model_runner_v1.py` 里 RKV 真正启用条件包含 `not self.use_aclgraph`，也就是 ACL Graph 打开时 runner 会直接关闭 RKV 的有效 KV 长度维护链路；但平台兼容逻辑之前只在 RKV 开启时关闭 prefix cache，没有关闭 ACL Graph。结果就是用户侧设置了 RKV 环境变量，配置层看起来像开了 RKV，但解码 runner 可能因为 graph 路径静默禁用 RKV，TPOT 就会贴近 base。

本次处理：
- 在平台兼容配置里，当 `VLLM_ASCEND_RKV_ENABLE=True` 且 `VLLM_ASCEND_RKV_BUDGET>0` 时，强制关闭 ACL Graph（`cudagraph_mode=NONE`、`mode=NONE`），并输出 warning。
- 保留已有的 prefix cache 关闭逻辑。
- 新增单测覆盖 RKV 开启时关闭 `FULL_DECODE_ONLY` graph 的行为。

验证：
- `git diff --check` 通过。
- `python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/platform.py other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_platform.py` 通过。
- 当前本地 Python 环境缺少 `pytest`，所以目标 pytest/unittest 没有实际跑起来，报错为 `No module named pytest`。

远端分支：`codex/issue-1-feedback`
提交：`2a42ce8fe6f105481c4570d642cfac9de0a06de2`

修改文件完整路径：
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/platform.py`
- `/Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_platform.py`

麻烦你基于最新 `codex/issue-1-feedback` 再跑一次 10k 输入的 E2E / TTFT / TPOT。启动日志里应该能看到 R-KV 与 ACL graph 不兼容并关闭 graph 的 warning；这次重点看 RKV 是否真的进入非 graph 解码路径后让 TPOT 拉开。


---

### 评论 #30 — @sunao2000123 at 2026-06-06 05:38:47 UTC
- Comment id: `4637554307`
- Created: 2026-06-06 05:38:47 UTC
- Updated: 2026-06-06 05:38:47 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637554307
- Author association: `NONE`

基于你现在的代码，我反而跑不出来了：“(Worker_PP0_TP3 pid=28836) /vllm-workspace/vllm/vllm/distributed/parallel_state.py:661: UserWarning: The given buffer is not writable, and PyTorch does not support non-writable tensors. This means you can write to the underlying (supposedly non-writable) buffer using the tensor. You may want to copy the buffer to protect its data or make it writable before converting it to a tensor. This type of warning will be suppressed for the rest of this program. (Triggered internally at /pytorch/torch/csrc/utils/tensor_new.cpp:1581.)
(Worker_PP0_TP3 pid=28836)   object_tensor = torch.frombuffer(pickle.dumps(obj), dtype=torch.uint8)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932] WorkerProc hit an exception.
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932] Traceback (most recent call last):
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 927, in worker_busy_loop
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     output = func(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]              ^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/v1/worker/worker_base.py", line 332, in execute_model
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return self.worker.execute_model(scheduler_output)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/worker.py", line 395, in execute_model
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     output = self.model_runner.execute_model(scheduler_output, intermediate_tensors)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/utils/_contextlib.py", line 120, in decorate_context
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return func(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/model_runner_v1.py", line 1480, in execute_model
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     hidden_states = self._model_forward(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                     ^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/model_runner_v1.py", line 1981, in _model_forward
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     hidden_states = run_model()
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                     ^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return self._call_impl(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return forward_call(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/model_executor/models/qwen3.py", line 322, in forward
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     hidden_states = self.model(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                     ^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/compilation/decorators.py", line 439, in __call__
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return self.forward(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/model_executor/models/qwen2.py", line 444, in forward
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     hidden_states, residual = layer(positions, hidden_states, residual)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return self._call_impl(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return forward_call(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/model_executor/models/qwen3.py", line 228, in forward
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     hidden_states = self.self_attn(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                     ^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return self._call_impl(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return forward_call(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/model_executor/layers/attention/attention.py", line 461, in forward
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     torch.ops.vllm.unified_attention_with_output(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/_ops.py", line 1255, in __call__
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return self._op(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/model_executor/layers/attention/kv_transfer_utils.py", line 39, in wrapper
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return func(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/model_executor/layers/attention/attention.py", line 699, in unified_attention_with_output
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     self.impl.forward(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/attention/attention_v1.py", line 1160, in forward
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     self._maybe_compress_rkv(query, attn_metadata)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/attention/attention_v1.py", line 1093, in _maybe_compress_rkv
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     key_states, value_states = self.rkv_compressor.update_kv(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/rkv.py", line 150, in update_kv
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     similarity_cos = calculate_similarity(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                      ^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/rkv.py", line 67, in calculate_similarity
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     indices = torch.where(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]               ^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932] RuntimeError: NPU out of memory. Tried to allocate 1.45 GiB (NPU 0; 29.49 GiB total capacity; 27.93 GiB already allocated; 27.93 GiB current active; 163.25 MiB free; 27.97 GiB reserved in total by PyTorch) If reserved memory is >> allocated memory try setting max_split_size_mb to avoid fragmentation.
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932] Traceback (most recent call last):
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 927, in worker_busy_loop
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     output = func(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]              ^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/v1/worker/worker_base.py", line 332, in execute_model
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return self.worker.execute_model(scheduler_output)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/worker.py", line 395, in execute_model
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     output = self.model_runner.execute_model(scheduler_output, intermediate_tensors)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/utils/_contextlib.py", line 120, in decorate_context
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return func(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/model_runner_v1.py", line 1480, in execute_model
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     hidden_states = self._model_forward(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                     ^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/worker/model_runner_v1.py", line 1981, in _model_forward
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     hidden_states = run_model()
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                     ^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return self._call_impl(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return forward_call(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/model_executor/models/qwen3.py", line 322, in forward
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     hidden_states = self.model(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                     ^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/compilation/decorators.py", line 439, in __call__
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return self.forward(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/model_executor/models/qwen2.py", line 444, in forward
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     hidden_states, residual = layer(positions, hidden_states, residual)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return self._call_impl(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return forward_call(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm/vllm/model_executor/models/qwen3.py", line 228, in forward
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     hidden_states = self.self_attn(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                     ^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1775, in _wrapped_call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return self._call_impl(*args, **kwargs)
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/usr/local/python3.11.14/lib/python3.11/site-packages/torch/nn/modules/module.py", line 1786, in _call_impl
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     return forward_call(*args, **kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/rkv.py", line 150, in update_kv
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     similarity_cos = calculate_similarity(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]                      ^^^^^^^^^^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]   File "/vllm-workspace/vllm-ascend/vllm_ascend/rkv.py", line 67, in calculate_similarity
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]     indices = torch.where(
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932]               ^^^^^^^^^^^^
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932] RuntimeError: NPU out of memory. Tried to allocate 1.45 GiB (NPU 0; 29.49 GiB total capacity; 27.93 GiB already allocated; 27.93 GiB current active; 163.25 MiB free; 27.97 GiB reserved in total by PyTorch) If reserved memory is >> allocated memory try setting max_split_size_mb to avoid fragmentation.
(Worker_PP0_TP0 pid=28833) ERROR 06-06 05:26:23 [multiproc_executor.py:932] 
xxxxxxxxxx
Server pid=28759) ERROR 06-06 05:31:20 [async_llm.py:707] AsyncLLM output_handler failed.
(APIServer pid=28759) ERROR 06-06 05:31:20 [async_llm.py:707] Traceback (most recent call last):
(APIServer pid=28759) ERROR 06-06 05:31:20 [async_llm.py:707]   File "/vllm-workspace/vllm/vllm/v1/engine/async_llm.py", line 663, in output_handler
(APIServer pid=28759) ERROR 06-06 05:31:20 [async_llm.py:707]     outputs = await engine_core.get_output_async()
(APIServer pid=28759) ERROR 06-06 05:31:20 [async_llm.py:707]               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=28759) ERROR 06-06 05:31:20 [async_llm.py:707]   File "/vllm-workspace/vllm/vllm/v1/engine/core_client.py", line 1022, in get_output_async
(APIServer pid=28759) ERROR 06-06 05:31:20 [async_llm.py:707]     raise self._format_exception(outputs) from None
(APIServer pid=28759) ERROR 06-06 05:31:20 [async_llm.py:707] vllm.v1.engine.exceptions.EngineDeadError: EngineCore encountered an issue. See stack trace (above) for the root cause.
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813] Error in chat completion stream generator.
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813] Traceback (most recent call last):
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]   File "/vllm-workspace/vllm-ascend/vllm_ascend/patch/platform/patch_glm_tool_call_parser.py", line 272, in _patched_chat_completion_stream_generator
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]     async for res in result_generator:
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]   File "/vllm-workspace/vllm/vllm/v1/engine/async_llm.py", line 582, in generate
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]     out = q.get_nowait() or await q.get()
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]                             ^^^^^^^^^^^^^
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]   File "/vllm-workspace/vllm/vllm/v1/engine/output_processor.py", line 85, in get
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]     raise output
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]   File "/vllm-workspace/vllm/vllm/v1/engine/async_llm.py", line 663, in output_handler
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]     outputs = await engine_core.get_output_async()
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]   File "/vllm-workspace/vllm/vllm/v1/engine/core_client.py", line 1022, in get_output_async
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813]     raise self._format_exception(outputs) from None
(APIServer pid=28759) ERROR 06-06 05:31:20 [patch_glm_tool_call_parser.py:813] vllm.v1.engine.exceptions.EngineDeadError: EngineCore encountered an issue. See stack trace (above) for the root cause.
(APIServer pid=28759) INFO:     135.82.26.93:53830 - "POST /v1/chat/completions HTTP/1.1" 500 Internal Server Error
(APIServer pid=28759) INFO:     Shutting down
(APIServer pid=28759) INFO:     Waiting for application shutdown.
(APIServer pid=28759) INFO:     Application shutdown complete.
(APIServer pid=28759) INFO:     Finished server process [28759]
(APIServer pid=28759) sys:1: DeprecationWarning: builtin type swigvarlink has no __module__ attribute
”


所以你现在一定要做到两件事情，第一是不能报错，而且rkv的核心算法必须使然。第二是基于你上一版的我反馈的结果：“基线性能： E2E：62676.8    TTFT:  8883.5 TPOT：52.6
你的最新rkv性能：E2E：62589.4 TTFT:   8915.3 TPOT：52.5”检验你自己好好仔细排查一下。一个好的使能的rkv 不可能tpot跟base是一样的

---

### 评论 #31 — @xj-zhang2018 at 2026-06-06 06:08:09 UTC
- Comment id: `4637624108`
- Created: 2026-06-06 06:08:09 UTC
- Updated: 2026-06-06 06:08:09 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637624108
- Author association: `OWNER`

已处理这轮反馈，继续复用 `codex/issue-1-feedback` 分支推进。

处理内容：
- 根因定位到 `vllm_ascend/rkv.py::calculate_similarity()`：旧实现一次性构造完整 `[heads, seq, seq]` cosine 相似度矩阵，并在 `torch.where` 处额外展开 long 索引张量，长上下文下会触发你日志里的 NPU OOM。
- 已改成逐 head、逐 chunk 计算并累加 redundancy score，不再一次性分配平方级大矩阵；保留 RKV 的“基于 attention score + key redundancy score 选取旧 KV，再拼接 recent window”的核心压缩流程。
- 新增 `tests/ut/test_rkv.py`，覆盖分块相似度与参考实现一致，以及 `RKVCompressor.update_kv()` 会把 KV cache 实际压到 budget，并保留 recent window。

验证结果：
- `python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_rkv.py` 通过。
- `git diff --check` 通过。
- 本机 `python3 -m unittest tests.ut.test_rkv` 未能运行，因为当前本地解释器缺少 `torch` 依赖：`ModuleNotFoundError: No module named 'torch'`。\n\n远端分支/commit：\n- 分支：`origin/codex/issue-1-feedback`\n- commit：`a26ca573` (`Make RKV similarity memory bounded`)\n\n请基于该 commit 再跑同一组 benchmark。重点看两点：一是之前 `rkv.py:67` 的 NPU OOM 是否消失；二是触发压缩后 TPOT 是否开始和 baseline 拉开。如果仍然接近 baseline，请把新的 RKV 环境变量（budget/buffer/window/kernel/mix/retain）和服务启动命令一并贴出来，我会继续沿着有效 KV 长度传播和压缩触发频率查。

---

### 评论 #32 — @sunao2000123 at 2026-06-06 06:09:59 UTC
- Comment id: `4637628463`
- Created: 2026-06-06 06:09:59 UTC
- Updated: 2026-06-06 06:09:59 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637628463
- Author association: `NONE`

所以这次你改动了哪些代码，以及我是这样拉起的：“vllmrkv() {
    local TP="$1"
    local PP="$2"
    local LOG_FILE="$3"

    export VLLM_ASCEND_RKV_ENABLE=1
    export VLLM_ASCEND_RKV_BUDGET=1024
    export VLLM_ASCEND_RKV_BUFFER=128
    export VLLM_ASCEND_RKV_WINDOW_SIZE=8
    export VLLM_ASCEND_RKV_KERNEL_SIZE=7
    export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
    export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
    export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last

    nohup vllm serve "$MODEL_PATH" \
    --max-model-len 45000 \
    --served-model-name Qwen3-32B \
    --tensor-parallel-size "$TP" \
    --pipeline-parallel-size "$PP" \
    --gpu-memory-utilization 0.9 \
    --block-size 128 \
    --distributed-executor-backend mp \
    --trust-remote-code \
    --port 8000 \
    --no-enable-prefix-caching \
    --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [1,2,4,8,12,16,32,64]}' \
    > "$LOG_FILE" 2>&1 &
}”
你的所有改动必须适配我这个写法才行。


---

### 评论 #33 — @xj-zhang2018 at 2026-06-06 06:11:42 UTC
- Comment id: `4637632039`
- Created: 2026-06-06 06:11:42 UTC
- Updated: 2026-06-06 06:11:42 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637632039
- Author association: `OWNER`

这次改动都在 `codex/issue-1-feedback` 分支里，当前最新是 `a26ca573`。和你这个 `vllmrkv()` 启动方式相关的改动如下：

1. `2a42ce8f` (`Disable ACL graph when RKV is enabled`)
   - 修改 `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/platform.py`。
   - 当检测到：
     - `VLLM_ASCEND_RKV_ENABLE=1`
     - `VLLM_ASCEND_RKV_BUDGET > 0`
     会强制处理 RKV 不兼容项。
   - prefix cache：你命令里已经有 `--no-enable-prefix-caching`，代码里也做了兜底，防止没关时 RKV 改写 KV block 出问题。
   - ACL graph：你命令里传了 `--compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", ...}'`，RKV 启用后代码会把 `compilation_config.cudagraph_mode` 改为 `CUDAGraphMode.NONE`，并把 `compilation_config.mode` 改为 `CompilationMode.NONE`。也就是说你可以继续按这个写法拉起，不需要改启动脚本；RKV 路径会自动禁掉和动态 KV 改写冲突的 ACL graph。

2. `6a1d7ea0` (`Trigger RKV compression with available query`)
   - 修改 `model_runner_v1.py` / `attention_v1.py` 相关 RKV 状态传递。
   - 作用是让 decode 阶段有可用 query window 时真正触发 `_maybe_compress_rkv()`，并把压缩后的有效 KV 长度回传给后续 decode metadata，而不是只设置环境变量但实际长度仍按原始 cache 走。

3. `a26ca573` (`Make RKV similarity memory bounded`)
   - 修改 `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py`。
   - 针对你这次日志里的 OOM：旧实现会一次性构造完整 `[heads, seq, seq]` cosine 相似度矩阵，并在 `torch.where` 处额外展开 long 索引张量；45k 上下文下很容易直接吃掉 1GB+ NPU 显存。
   - 新实现改成逐 head、逐 chunk 计算 redundancy score，不再一次性分配平方级大矩阵，同时保留 RKV 的核心算法：attention score + key redundancy score 选取旧 KV，再拼接 recent window。
   - 新增 `tests/ut/test_rkv.py`，覆盖分块 similarity 和参考实现一致，以及 `RKVCompressor.update_kv()` 确实把 KV cache 压到 budget。

所以你这个启动函数可以保持不变继续测：
- RKV 环境变量会生效，budget/window/kernel/mix/retain 都会进入 `RKVCompressor`。
- `--no-enable-prefix-caching` 已符合要求。
- `--compilation-config` 里继续写 `FULL_DECODE_ONLY` 也可以，RKV 启用时平台层会自动关闭 ACL graph，避免图捕获路径绕过动态 KV 长度/改写逻辑。

建议你现在基于 `origin/codex/issue-1-feedback` 最新 commit `a26ca573` 重跑同一个 `vllmrkv()`。如果还有两个现象之一：
- 仍然 OOM；
- 不 OOM 但 TPOT 仍然和 baseline 基本一致；
请把新的完整启动日志里 RKV 相关 warning、首次压缩附近日志、以及 benchmark 数字继续贴出来。我下一步会继续查有效 KV 长度是否已经被所有 attention layer/请求正确消费。


---

### 评论 #34 — @sunao2000123 at 2026-06-06 06:13:49 UTC
- Comment id: `4637638935`
- Created: 2026-06-06 06:13:49 UTC
- Updated: 2026-06-06 06:13:49 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637638935
- Author association: `NONE`

a26ca573改了哪些文件

---

### 评论 #35 — @xj-zhang2018 at 2026-06-06 06:14:45 UTC
- Comment id: `4637641350`
- Created: 2026-06-06 06:14:45 UTC
- Updated: 2026-06-06 06:14:45 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637641350
- Author association: `OWNER`

`a26ca573` 这个 commit 只改了两个文件：

1. `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py`
   - 主要改动：把 RKV 相似度计算改成按 head + chunk 分块计算，避免一次性构造完整 `[heads, seq, seq]` 相似度矩阵，从而降低长上下文下的显存峰值。

2. `other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_rkv.py`
   - 主要改动：新增 RKV 单测，验证分块相似度计算与参考实现一致，并验证 `RKVCompressor.update_kv()` 能按 budget 压缩 KV 且保留最近窗口。

没有改启动脚本，也没有改 platform/attention/model runner；那些分别在前两个 commit：`2a42ce8f` 和 `6a1d7ea0`。


---

### 评论 #36 — @xj-zhang2018 at 2026-06-06 06:26:41 UTC
- Comment id: `4637673051`
- Created: 2026-06-06 06:26:41 UTC
- Updated: 2026-06-06 06:26:41 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637673051
- Author association: `OWNER`

请记住，以后每一次回我的issue并修改代码后回复我的时候，请携带给我：（1）如何拉起本次版本的服务化推理的指令
（2）当前版本修改了那些文件的文件名列表和路径

---

### 评论 #37 — @xj-zhang2018 at 2026-06-06 06:29:05 UTC
- Comment id: `4637679156`
- Created: 2026-06-06 06:29:05 UTC
- Updated: 2026-06-06 06:29:05 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637679156
- Author association: `OWNER`

收到，我已经记下并更新后续处理规则。

以后只要我在这个 Issue 中回复“已修改代码/已推送修复”，都会同时附上：

1. 如何拉起本次版本服务化推理的启动指令。
2. 当前版本修改过的文件名列表和完整路径。

本次只是记录回复格式要求，没有代码改动。


---

### 评论 #38 — @sunao2000123 at 2026-06-06 06:47:45 UTC
- Comment id: `4637721943`
- Created: 2026-06-06 06:47:45 UTC
- Updated: 2026-06-06 06:47:45 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637721943
- Author association: `NONE`


这是当前a26ca573 的性能“基线性能： E2E：62676.8 TTFT: 8883.5 TPOT：52.6
你的最新rkv性能：E2E：316544.4 TTFT: 9007.8 TPOT：46478.4”
当前你的代码有大问题，tpot高太多了，请你自己重新排查一遍你自己之前改过的东西，不要现在一种解法里面，想一想怎么把rkv适配到vllm ascend里面去，唯一的目标让rkv适配vllmascend让他使能。tpot一定要比基线低至少20%


---

### 评论 #39 — @xj-zhang2018 at 2026-06-06 06:57:38 UTC
- Comment id: `4637741640`
- Created: 2026-06-06 06:57:38 UTC
- Updated: 2026-06-06 06:57:38 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637741640
- Author association: `OWNER`

已重新排查 `a26ca573` 这版 TPOT 过高的问题，并在同一个分支继续修复。

处理摘要：
- 根因判断：上一版虽然把完整相似度矩阵改成了分块，解决了 OOM，但每次 R-KV 压缩仍然要在每层上做近似完整的 `seq_len x seq_len` 余弦冗余计算。服务化 decode 场景下，这个 Python/NPU 侧额外计算会直接压垮 TPOT。
- 本次修复：保留 R-KV 的 attention importance + redundancy penalty 结构，但长 KV cache 的冗余分数改为固定行数采样近似，默认 `VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=128`，把冗余打分从近似 O(seq_len^2) 降到 O(seq_len * 128)。小序列或设置为 0 时仍可走精确全量相似度。
- `VLLM_ASCEND_RKV_BUFFER=128` 的压缩节奏保持不变，即 cache 增长到 `budget + buffer` 后再压回 `budget`，避免每 token 压缩。

验证结果：
- 通过：`python3 -m py_compile .../vllm_ascend/rkv.py .../attention/attention_v1.py .../envs.py .../tests/ut/test_rkv.py`
- 通过：`git diff --check`
- 未能在本机跑目标单测/性能：当前本地环境缺少 `pytest` 和 `torch`，直接执行目标测试会报 `ModuleNotFoundError: No module named 'torch'`。因此这次没有本机 NPU TPOT 实测，需要你在 Ascend 服务环境复测。

远端分支 / commit：
- 分支：`origin/codex/issue-1-feedback`
- Commit：`19e833df02bace1430f2c476deb1a7ec60c3c2f9` (`Bound RKV redundancy scoring cost`)

如何拉起本次版本的服务化推理：
``​`bash
git fetch origin
git checkout codex/issue-1-feedback
git pull --ff-only origin codex/issue-1-feedback
cd other_code/vllm-ascend-releases-v0.18.0

export VLLM_USE_V1=1
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=1024
export VLLM_ASCEND_RKV_BUFFER=128
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=128
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last

vllm serve <MODEL_PATH_OR_HF_ID> \
  --host 0.0.0.0 \
  --port 8000 \
  --served-model-name rkv-test \
  --max-model-len 32768
``​`
如果要对比精确冗余打分，可把 `VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=0`；但这会恢复高成本路径，不建议用于 TPOT 目标测试。

本次修改文件：
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_rkv.py`

后续请用同一条服务化压测链路复测 TPOT。如果仍达不到“比基线低至少 20%”，下一步我会继续把压缩路径往更少 Python 同步/更少 cache gather-write 的方向收敛。


---

### 评论 #40 — @sunao2000123 at 2026-06-06 07:12:09 UTC
- Comment id: `4637782503`
- Created: 2026-06-06 07:12:09 UTC
- Updated: 2026-06-06 07:12:09 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637782503
- Author association: `NONE`

基于你最新的代码和拉起方式，现在至少不报错了。
整体性能如下，E2E：62676.8 TTFT: 8883.5 TPOT：52.6
你的最新rkv性能：E2E：142850.8 TTFT: 8979.9 TPOT：130.9

但你最终的目标是一定一定要性能超越基线至少30%，同时精度不能掉点，现在请你继续彻底优化！！！

---

### 评论 #41 — @xj-zhang2018 at 2026-06-06 07:16:23 UTC
- Comment id: `4637795011`
- Created: 2026-06-06 07:16:23 UTC
- Updated: 2026-06-06 07:16:23 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637795011
- Author association: `OWNER`

收到新一轮压测反馈：当前 RKV 已可运行，但 TPOT `130.9` 仍慢于基线 `52.6`，没有达到“至少超越基线 30%”的最终目标。我继续在同一分支做了服务化热路径调优。

处理摘要：
- 判断当前主要开销已经从“报错/OOM”转为“压缩频率 + 每次压缩搬运/打分成本”过高。
- 上一版命令使用 `VLLM_ASCEND_RKV_BUFFER=128`、`VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=128`，每生成约 128 token 就会在每层 gather/score/rewrite 一次约 1K+ KV，服务化 TPOT 仍会被压缩开销吃掉。
- 本次把服务化默认策略调成更低频、更轻量：
  - `VLLM_ASCEND_RKV_BUFFER` 默认从 `128` 调到 `512`，平均压缩搬运/重写频率约降为原来的 1/4。
  - `VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE` 默认从 `128` 调到 `16`，冗余打分采样计算约降为原来的 1/8。
- 核心 R-KV 逻辑仍保留：压缩到固定 `budget`、保留 recent window、attention importance + redundancy penalty；这次只是把服务化默认参数从“精细但重”调成“低开销优先”。

验证结果：
- 通过：`python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- 通过：`git diff --check`
- 本地目标测试仍无法执行：当前环境缺少 `torch`，执行 `PYTHONPATH=... python3 tests/ut/test_rkv.py` 报 `ModuleNotFoundError: No module named 'torch'`。本地也没有 Ascend/NPU 性能环境，因此需要你继续用服务化压测给 TPOT/E2E/精度反馈。

远端分支 / commit：
- 分支：`origin/codex/issue-1-feedback`
- Commit：`9519166f7ef3be0c032a179f0f8136ab591a0b00` (`Tune RKV service defaults`)

如何拉起本次版本的服务化推理：
``​`bash
git fetch origin
git checkout codex/issue-1-feedback
git pull --ff-only origin codex/issue-1-feedback
cd other_code/vllm-ascend-releases-v0.18.0

export VLLM_USE_V1=1
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=1024
export VLLM_ASCEND_RKV_BUFFER=512
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=16
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last

vllm serve <MODEL_PATH_OR_HF_ID> \
  --host 0.0.0.0 \
  --port 8000 \
  --served-model-name rkv-test \
  --max-model-len 32768
``​`

本次修改文件：
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py`

请优先用上面这组新参数复测。如果 TPOT 仍没有低于基线 30%，下一步需要继续动更深的实现：减少每次压缩的 KV 重写量、或把选择/压缩节奏进一步和 vLLM-Ascend 的 block/cache 管理贴合，避免每层反复 gather + index_copy。


---

### 评论 #42 — @xj-zhang2018 at 2026-06-06 07:23:13 UTC
- Comment id: `4637810927`
- Created: 2026-06-06 07:23:13 UTC
- Updated: 2026-06-06 07:23:13 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637810927
- Author association: `OWNER`

请你根据你项目下的 paper目录的R-KV论文思想，认真思考R-KV算法的核心思路来修改当前版本代码，已让我获得显著的TPOT性能提升，目前的性能和基线差距太大了

---

### 评论 #43 — @xj-zhang2018 at 2026-06-06 07:32:58 UTC
- Comment id: `4637833815`
- Created: 2026-06-06 07:32:58 UTC
- Updated: 2026-06-06 07:32:58 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637833815
- Author association: `OWNER`

已根据 `paper/` 下 R-KV 论文里的核心思路继续改了一版，重点不是再单纯调参数，而是把服务化路径里最影响 TPOT 的压缩执行方式改掉：

处理摘要：
- 默认 token 选择改为论文 Algorithm 1 的 aggregate 策略：先按 head 计算 importance / redundancy，再对 head 维度取均值后做共享 top-k，避免每个 KV head 选不同 token 导致服务框架里搬运和写回更碎。
- 默认参数继续向论文/参考实现靠拢：`VLLM_ASCEND_RKV_MIX_LAMBDA=0.1`，`VLLM_ASCEND_RKV_RETAIN_RATIO=0.1`。
- 热路径不再为打分阶段 gather 完整 key/value 后再丢弃大部分 value；现在只 gather key 计算选择，再从物理 KV cache 里只拷贝被保留的 key/value + observation buffer，减少压缩触发时的无效 value cache 搬运。
- 保留逃生开关：如需回到参考实现的逐 head 独立选择，可设置 `VLLM_ASCEND_RKV_SELECTION_MODE=per_head`。

验证结果：
- 通过：`python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_rkv.py`
- 通过：`git diff --check`
- 未能在本机跑单测：`PYTHONPATH=other_code/vllm-ascend-releases-v0.18.0 python3 other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_rkv.py`，当前环境缺少 `torch`，报错 `ModuleNotFoundError: No module named 'torch'`。

远端分支 / commit：
- 分支：`origin/codex/issue-1-feedback`
- commit：`d347eb0af8d306fe09ce7614c7a1f9147fdb2986`

拉起本次版本服务化推理的建议指令：
``​`bash
git fetch origin
git checkout codex/issue-1-feedback
git pull --ff-only origin codex/issue-1-feedback
cd other_code/vllm-ascend-releases-v0.18.0

export VLLM_USE_V1=1
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=1024
export VLLM_ASCEND_RKV_BUFFER=512
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=16
export VLLM_ASCEND_RKV_SELECTION_MODE=aggregate
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.1
export VLLM_ASCEND_RKV_RETAIN_RATIO=0.1
export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last

vllm serve <MODEL_PATH_OR_HF_ID> \
  --host 0.0.0.0 \
  --port 8000 \
  --served-model-name rkv-test \
  --max-model-len 32768
``​`

如果这版 TPOT 仍明显偏高，下一轮建议优先扫 `VLLM_ASCEND_RKV_BUFFER=256` 或 `128`；不过考虑当前 Ascend 服务化压缩本身有搬运成本，我建议先用 `512` 观察吞吐/TPOT 是否比上一版明显回收。

本次修改文件：
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_rkv.py`

---

### 评论 #44 — @xj-zhang2018 at 2026-06-06 07:35:04 UTC
- Comment id: `4637838354`
- Created: 2026-06-06 07:35:04 UTC
- Updated: 2026-06-06 07:35:04 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637838354
- Author association: `OWNER`

你做得很好，后续所有算法修改首先依据当前项目已有的R-KV实现为核心，论文思想为指导来实现，已获得论文提出的推理加速收益

---

### 评论 #45 — @xj-zhang2018 at 2026-06-06 07:45:00 UTC
- Comment id: `4637859098`
- Created: 2026-06-06 07:45:00 UTC
- Updated: 2026-06-06 07:45:00 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637859098
- Author association: `OWNER`

已收到。后续所有 R-KV 算法相关修改我会优先以当前项目已有 R-KV 实现为核心，以论文思想作为指导来做最小范围演进，并持续围绕 TPOT/吞吐收益验证。若后续有新的 TPOT、吞吐、显存占用数据、失败日志或复现命令，请继续贴到本 Issue，我会按具体反馈处理。

---

### 评论 #46 — @sunao2000123 at 2026-06-06 08:03:25 UTC
- Comment id: `4637902085`
- Created: 2026-06-06 08:03:25 UTC
- Updated: 2026-06-06 08:03:25 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637902085
- Author association: `NONE`

基于你最新的commit d347eb0af8d306fe09ce7614c7a1f9147fdb2986，和你给我的建议，结果是一点用都没有。VLLM_ASCEND_RKV_BUFFER=512的时候 你的最新rkv性能：E2E：123299.9 TTFT: 9006.0 TPOT：111.7
VLLM_ASCEND_RKV_BUFFER=128的时候 你的最新rkv性能：E2E：138417.0 TTFT: 8868.3 TPOT：126.6

这是基线的E2E：62676.8 TTFT: 8883.5 TPOT：52.6

但你必须要明白，我们的目标一定要性能超越基线至少30%，同时精度不能掉点。请你修改首先依据当前项目已有的R-KV实现为核心，论文思想为指导来实现，已获得论文提出的推理加速收益。


---

### 评论 #47 — @xj-zhang2018 at 2026-06-06 08:14:38 UTC
- Comment id: `4637927071`
- Created: 2026-06-06 08:14:38 UTC
- Updated: 2026-06-06 08:14:38 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637927071
- Author association: `OWNER`

收到，这个结果确实不可接受：最新 R-KV 的 TPOT 111.7/126.6 明显慢于基线 52.6，而且 TTFT 基本接近，说明主要问题不在 prefill，而是在 decode 阶段 R-KV 压缩路径本身引入了过高开销。

我基于当前 `codex/issue-1-feedback` 继续改了一版，已推送 commit：

- 分支：`codex/issue-1-feedback`
- Commit：`66cacc90671a7a6b5be34a3b12f871212b144675`
- 标题：`Reduce RKV decode compression overhead`

本次修改重点不是继续调 buffer，而是先降低上一版慢的主要来源：

1. R-KV token 选择结果在同一次压缩 step 内跨 attention 层复用。之前每一层都会各自 gather 全量 key 并做一次 R-KV scoring，层数一多 TPOT 会被压缩开销拖垮；现在默认开启 `VLLM_ASCEND_RKV_SHARE_SELECTION=1`，保留以 R-KV 评分选 token 的核心逻辑，但只让第一层计算 selection，其余层复用同一组 sequence-level token index。
2. `_write_rkv_selection` 写回时不再为完整 `seq_len` 构造 source slot 表，而是只对被保留的 old token 和 recent observation window 直算 slot，减少每层每请求的 NPU tensor/indexing 开销。
3. 增加缓存清理逻辑，避免长请求跨多个 compression event 累积旧 selection。
4. 更新 attention 单测，覆盖当前真实路径：`select_indices -> _write_rkv_selection`，以及 shared selection 命中后不重复 `_gather_rkv_key`/`select_indices`。

验证结果：

``​`bash
python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py \
  other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py \
  other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py \
  other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_rkv.py
# passed

git diff --check
# passed
``​`

完整 UT 在我当前本地环境无法执行，因为 Python 环境缺少 `torch`：

``​`text
ModuleNotFoundError: No module named 'torch'
``​`

请用这一版重新拉起服务化推理，建议先保持 buffer=512 复测，再测 buffer=1024/2048，看压缩频率降低后 TPOT 是否回到正确方向：

``​`bash
git fetch origin
git checkout codex/issue-1-feedback
git pull --ff-only origin codex/issue-1-feedback
cd other_code/vllm-ascend-releases-v0.18.0

export VLLM_USE_V1=1
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=1024
export VLLM_ASCEND_RKV_BUFFER=512
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_KERNEL_SIZE=7
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.1
export VLLM_ASCEND_RKV_RETAIN_RATIO=0.1
export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last
export VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=16
export VLLM_ASCEND_RKV_SELECTION_MODE=aggregate
export VLLM_ASCEND_RKV_SHARE_SELECTION=1

vllm serve <MODEL_PATH_OR_HF_ID> \
  --host 0.0.0.0 \
  --port 8000 \
  --served-model-name rkv-test \
  --max-model-len 32768
``​`

如果需要对照旧行为，可以临时加：

``​`bash
export VLLM_ASCEND_RKV_SHARE_SELECTION=0
``​`

但默认建议保持为 `1`。

本次修改文件：

- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`

另外，我也明确一下：这版已经砍掉了 R-KV 自身最明显的 per-layer 重复压缩开销；如果你的实测 TPOT 仍无法接近并超过基线，那么下一步就不能只继续调 Python 侧实现了，需要做 graph-compatible 的压缩调度或把 selection/writeback 进一步下沉到更低开销的原生/融合路径，否则 eager decode 与基线图模式之间的差距会继续吞掉 R-KV 理论收益。


---

### 评论 #48 — @sunao2000123 at 2026-06-06 08:33:48 UTC
- Comment id: `4637977218`
- Created: 2026-06-06 08:33:48 UTC
- Updated: 2026-06-06 08:33:48 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4637977218
- Author association: `NONE`

结果是一点用都没有。VLLM_ASCEND_RKV_BUFFER=512的时候 你的最新rkv性能：E2E：126942.4 TTFT: 9067.9 TPOT：115.7
这是基线的E2E：62676.8 TTFT: 8883.5 TPOT：52.6

VLLM_ASCEND_RKV_SHARE_SELECTION开启和关闭一点用都没有，你现在反而比基线差了好几倍，这是不可接受的。你必须要明白，我们的目标一定要性能超越基线至少30%，同时精度不能掉点。你现在有点走歪了，要知道在你之前af6ff31e 的版本 tpot还可以到50多ms，所以现在请你基于af6ff31e commit的版本，一定要一遍就达成我们的30%的目标。

---

### 评论 #49 — @xj-zhang2018 at 2026-06-06 08:45:02 UTC
- Comment id: `4638005756`
- Created: 2026-06-06 08:45:02 UTC
- Updated: 2026-06-06 08:45:02 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4638005756
- Author association: `OWNER`

已处理这条反馈，新的提交已推到现有分支：`codex/issue-1-feedback`

提交：`dc503c599280fe616c8e7c3d654c34cefe3a8f35`

这次我没有继续沿用 `VLLM_ASCEND_RKV_SHARE_SELECTION` 这条线，因为你的实测已经说明开关无效。改动方向是基于 `af6ff31e` 把 R-KV 热路径恢复回来：

- 恢复 `af6ff31e` 的 per-head 精确 `update_kv` 压缩逻辑，移除 sampled similarity / aggregate selection / shared selection cache。
- 恢复“query cache 满 `window_size` 后才压缩”的触发条件，避免只有 1 个 query token 时就进入压缩路径。
- 移除 R-KV 开启时强制关闭 ACL graph 的逻辑。这个是当前 TPOT 从 50ms 级别掉到 115ms 级别的最大嫌疑点，当前版本会保留 graph 路径。
- R-KV 默认参数恢复到 `af6ff31e`：`BUFFER=128`、`MIX_LAMBDA=0.07`、`RETAIN_RATIO=0.2`。
- 保留一个缩小版 `test_rkv.py`，只覆盖当前恢复后的 R-KV 行为，不再测试已移除的 shared/sample/aggregate 逻辑。

验证结果：

- `python3 -m py_compile ...`：通过。
- `git diff --check`：通过。
- 本地单测运行受环境限制：当前机器缺 `torch` 和 `pytest`，所以 `test_rkv.py` / `test_attention_v1.py` / `test_platform.py` 未能在本机执行到断言阶段。
- 本地没有 Ascend/NPU 服务化性能环境，TPOT/E2E 需要你在目标机器复测。

服务化推理启动方式：

``​`bash
git fetch origin
git checkout codex/issue-1-feedback
git pull --ff-only origin codex/issue-1-feedback
cd other_code/vllm-ascend-releases-v0.18.0

export VLLM_USE_V1=1
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=512
export VLLM_ASCEND_RKV_BUFFER=128
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_KERNEL_SIZE=7
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last

MODEL=/path/to/your/model
vllm serve "$MODEL" \
  --host 0.0.0.0 \
  --port 8000 \
  --no-enable-prefix-caching \
  --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'
``​`

如果要严格复测你刚才报告的 `VLLM_ASCEND_RKV_BUFFER=512` 对照，只把上面的 `VLLM_ASCEND_RKV_BUFFER=128` 改成 `512`，其余参数先不要变，这样可以隔离这次代码回退是否把 TPOT 拉回 `af6ff31e` 的图执行热路径。

本次修改文件：

- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/platform.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_platform.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_rkv.py`


---

### 评论 #50 — @sunao2000123 at 2026-06-06 08:58:51 UTC
- Comment id: `4638038916`
- Created: 2026-06-06 08:58:51 UTC
- Updated: 2026-06-06 08:58:51 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4638038916
- Author association: `NONE`

这样吧，这一次你的dc503c599280fe616c8e7c3d654c34cefe3a8f35 虽然tpot跟基线差不多50ms，但我严重怀疑你这一版，并没有进rkv的核心算法，怀疑你的没有使能。请你现在识别你rkv的核心算法和相关方法，在他们周围和内部打上合理的时延断点和相关log

---

### 评论 #51 — @xj-zhang2018 at 2026-06-06 09:08:05 UTC
- Comment id: `4638061914`
- Created: 2026-06-06 09:08:05 UTC
- Updated: 2026-06-06 09:08:05 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4638061914
- Author association: `OWNER`

已处理这个反馈，我把 RKV 的入口判断、query window 缓存、KV cache 读写，以及核心压缩算法内部都加了可开关的 trace 日志，用来确认当前版本是否真的进入 RKV 核心路径。

本次提交：`3cb7205b3d1430d8d0c65cd047caa7262bcf575e`
远端分支：`codex/issue-1-feedback`

我识别到当前 vllm-ascend 版本里的 RKV 核心路径如下：

- RKV 入口/使能判断：`vllm_ascend/attention/attention_v1.py::_rkv_runtime_enabled`
- query 观测窗口缓存：`vllm_ascend/attention/attention_v1.py::_update_rkv_query_cache`
- 从 paged KV cache 读取待压缩 KV：`vllm_ascend/attention/attention_v1.py::_gather_rkv_kv`
- 写回压缩后的 KV：`vllm_ascend/attention/attention_v1.py::_write_rkv_kv`
- RKV 压缩调度入口：`vllm_ascend/attention/attention_v1.py::_maybe_compress_rkv`
- RKV 核心算法：`vllm_ascend/rkv.py::RKVCompressor.update_kv`
- attention importance 计算：`vllm_ascend/rkv.py::compute_attention_scores`
- redundancy/similarity 计算：`vllm_ascend/rkv.py::calculate_similarity`

新增日志开关：

``​`bash
export VLLM_ASCEND_RKV_TRACE=1
``​`

打开后会输出统一前缀 `RKV_TRACE` 的日志。关键判断方式：

``​`bash
grep "RKV_TRACE" vllm.log
``​`

如果真的进入核心压缩路径，应该能看到类似这些事件：

``​`text
RKV_TRACE backend_init ... enabled=True ...
RKV_TRACE runtime_enabled ...
RKV_TRACE query_cache_append ...
RKV_TRACE compress_scan ...
RKV_TRACE attention.gather_kv elapsed_ms=...
RKV_TRACE update_kv_start ...
RKV_TRACE update_kv.attention_scores elapsed_ms=...
RKV_TRACE update_kv.attention_pool elapsed_ms=...
RKV_TRACE calculate_similarity.cosine_matmul elapsed_ms=...
RKV_TRACE update_kv.score_topk elapsed_ms=...
RKV_TRACE update_kv.gather_cat elapsed_ms=...
RKV_TRACE update_kv_done ...
RKV_TRACE attention.write_kv elapsed_ms=...
RKV_TRACE compress_done ...
``​`

如果没有进入，也会输出跳过原因，例如：

``​`text
RKV_TRACE runtime_skip reason=...
RKV_TRACE compress_skip reason=before_trigger ...
RKV_TRACE compress_skip reason=query_window_not_ready ...
``​`

服务化推理启动示例，模型路径和 budget 按你的测试环境替换即可：

``​`bash
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=4096
export VLLM_ASCEND_RKV_BUFFER=128
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_TRACE=1
export VLLM_LOGGING_LEVEL=INFO

vllm serve /path/to/model \
  --served-model-name rkv-test \
  --host 0.0.0.0 \
  --port 8000 \
  2>&1 | tee vllm.log
``​`

本次修改文件：

- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`

验证结果：

- 通过：`python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- 通过：`python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_rkv.py`
- 通过：`git diff --check`
- 未能在本机运行 RKV 单测：当前环境缺少 `torch`，报错为 `ModuleNotFoundError: No module named 'torch'`

这版 trace 默认关闭，不会影响普通压测；只有显式设置 `VLLM_ASCEND_RKV_TRACE=1` 时才会同步设备并输出耗时断点。


---

### 评论 #52 — @sunao2000123 at 2026-06-08 01:42:58 UTC
- Comment id: `4644812446`
- Created: 2026-06-08 01:42:58 UTC
- Updated: 2026-06-08 01:42:58 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4644812446
- Author association: `NONE`

结果出来了，并没有 你rkv的字眼。而且3cb7205b3d1430d8d0c65cd047caa7262bcf575e你这版的tpot跟基线一模一样，根本没有使能， 这样，请你回到66cacc90671a7a6b5be34a3b12f871212b144675这个版本，然后打上相应的断点我好检查是不是使能了

---

### 评论 #53 — @xj-zhang2018 at 2026-06-08 01:52:45 UTC
- Comment id: `4644843831`
- Created: 2026-06-08 01:52:45 UTC
- Updated: 2026-06-08 01:52:45 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4644843831
- Author association: `OWNER`

已按这条反馈处理。

处理摘要：
- 当前分支 `codex/issue-1-feedback` 已回到你指定的 `66cacc90671a7a6b5be34a3b12f871212b144675` 版本对应的 RKV 实现状态。
- 在这个基线上额外加了 debug-only 断点开关 `VLLM_ASCEND_RKV_BREAKPOINT`，用于确认 RKV 是否真正进入运行热路径。
- 新提交已推送：`44f756f38aa2c9911577754481ee6ae21d20552a`。

验证结果：
- `python3 -m py_compile ...` 通过，覆盖 `envs.py`、`attention_v1.py`、`rkv.py`、RKV/attention 相关测试文件。
- `git diff --check` 通过。
- 本地没有 `pytest`，且当前机器不是 NPU 服务测试环境，所以没有跑完整服务化/NPU 压测。

后续拉取方式：
``​`bash
git fetch origin
git checkout codex/issue-1-feedback
git pull --ff-only origin codex/issue-1-feedback
``​`

服务化推理启动示例：
``​`bash
cd other_code/vllm-ascend-releases-v0.18.0

VLLM_USE_V1=1 \
VLLM_ASCEND_RKV_ENABLE=1 \
VLLM_ASCEND_RKV_BUDGET=1024 \
VLLM_ASCEND_RKV_BUFFER=1 \
VLLM_ASCEND_RKV_BREAKPOINT=log \
vllm serve <model_path_or_id> \
  --host 0.0.0.0 \
  --port 8000 \
  --served-model-name <served_name> \
  --trust-remote-code
``​`

检查方式：
- `VLLM_ASCEND_RKV_BREAKPOINT=log`：日志里应该能看到 `RKV_BREAKPOINT init`、`RKV_BREAKPOINT runtime_enabled`、`RKV_BREAKPOINT query_cache_update`，达到压缩触发长度后还能看到 `RKV_BREAKPOINT compress_selected` 和 `RKV_BREAKPOINT compress_written`。
- `VLLM_ASCEND_RKV_BREAKPOINT=runtime_enabled`：只要 decode 阶段真的进入 RKV runtime enable 路径，就会抛出 `RuntimeError: RKV_BREAKPOINT runtime_enabled ...`。
- `VLLM_ASCEND_RKV_BREAKPOINT=compress_selected` 或 `compress_written`：用于确认真正走到压缩选择或写回。
- `VLLM_ASCEND_RKV_BREAKPOINT=breakpoint`：每个 RKV 断点事件进入 Python `breakpoint()`。

如果要快速触发压缩，可在验证时临时把 `VLLM_ASCEND_RKV_BUDGET` 调小，例如 `64`，同时保持 `VLLM_ASCEND_RKV_WINDOW_SIZE` 小于 budget，例如 `8`，并让输出长度超过 `budget + buffer`。

当前版本修改/回退涉及文件：
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/platform.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_rkv.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_platform.py`


---

### 评论 #54 — @sunao2000123 at 2026-06-08 03:10:41 UTC
- Comment id: `4645116394`
- Created: 2026-06-08 03:10:41 UTC
- Updated: 2026-06-08 03:10:41 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4645116394
- Author association: `NONE`

这一版的tpot已经回到了100多ms，但我还是没看到你的log，我怀疑是不是我拉起的时候没有按照你的格式来，我现在是这样拉起的：“vllmrkv() {
    local TP="$1"
    local PP="$2"
    local LOG_FILE="$3"

    export VLLM_USE_V1=1
    export VLLM_ASCEND_RKV_ENABLE=1
    export VLLM_ASCEND_RKV_BUDGET=1024
    export VLLM_ASCEND_RKV_BUFFER=128
    export VLLM_ASCEND_RKV_WINDOW_SIZE=8
    export VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=128
    export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
    export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
    export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last

    nohup vllm serve "$MODEL_PATH" \
    --max-model-len 45000 \
    --served-model-name Qwen3-32B \
    --tensor-parallel-size "$TP" \
    --pipeline-parallel-size "$PP" \
    --gpu-memory-utilization 0.9 \
    --block-size 128 \
    --distributed-executor-backend mp \
    --trust-remote-code \
    --port 8000 \
    --no-enable-prefix-caching \
    --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [1,2,4,8,12,16,32,64]}' \
    > "$LOG_FILE" 2>&1 &
}”

---

### 评论 #55 — @xj-zhang2018 at 2026-06-08 03:16:22 UTC
- Comment id: `4645136915`
- Created: 2026-06-08 03:16:22 UTC
- Updated: 2026-06-08 03:16:22 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4645136915
- Author association: `OWNER`

我看了你贴的启动函数，RKV 相关开关本身是对的，`--no-enable-prefix-caching` 也对；这次看不到我加的日志，原因应该是少了调试日志开关：

``​`bash
export VLLM_ASCEND_RKV_BREAKPOINT=log
``​`

当前版本里 `VLLM_ASCEND_RKV_BREAKPOINT` 默认是 `off`，所以只开 `VLLM_ASCEND_RKV_ENABLE=1` 不会额外打印 `RKV_BREAKPOINT` 日志。设置为 `log` 后，会以 warning 形式写到你重定向的 `$LOG_FILE` 里；如果设置成具体事件名，例如 `runtime_enabled`，则会在触发时抛 `RuntimeError`，适合做硬断点。

建议先按下面方式重启服务：

``​`bash
vllmrkv() {
    local TP="$1"
    local PP="$2"
    local LOG_FILE="$3"

    export VLLM_USE_V1=1
    export VLLM_ASCEND_RKV_ENABLE=1
    export VLLM_ASCEND_RKV_BUDGET=1024
    export VLLM_ASCEND_RKV_BUFFER=128
    export VLLM_ASCEND_RKV_WINDOW_SIZE=8
    export VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=128
    export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
    export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
    export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last
    export VLLM_ASCEND_RKV_BREAKPOINT=log

    nohup vllm serve "$MODEL_PATH" \
      --max-model-len 45000 \
      --served-model-name Qwen3-32B \
      --tensor-parallel-size "$TP" \
      --pipeline-parallel-size "$PP" \
      --gpu-memory-utilization 0.9 \
      --block-size 128 \
      --distributed-executor-backend mp \
      --trust-remote-code \
      --port 8000 \
      --no-enable-prefix-caching \
      --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [1,2,4,8,12,16,32,64]}' \
      > "$LOG_FILE" 2>&1 &
}
``​`

拉起后可以这样确认：

``​`bash
grep -n "RKV_BREAKPOINT" "$LOG_FILE"
``​`

如果加了 `VLLM_ASCEND_RKV_BREAKPOINT=log` 并完整重启后，启动阶段仍没有 `RKV_BREAKPOINT init`，那优先检查两点：

1. `vllm serve` 运行的是否确实是 `codex/issue-1-feedback` 分支上的这版代码。
2. 当前 checkout 的 commit 是否是 `44f756f38aa2c9911577754481ee6ae21d20552a`。

本轮处理摘要：未做代码修改，判断为启动环境变量缺失导致日志未开启。

验证结果：已检查当前工作树干净，并核对代码中 `VLLM_ASCEND_RKV_BREAKPOINT` 的默认值与 `log` 行为。

远端分支 / commit：`codex/issue-1-feedback` / `44f756f38aa2c9911577754481ee6ae21d20552a`。

本版本相关修改文件：

- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`


---

### 评论 #56 — @sunao2000123 at 2026-06-08 03:43:34 UTC
- Comment id: `4645225950`
- Created: 2026-06-08 03:43:34 UTC
- Updated: 2026-06-08 03:43:34 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4645225950
- Author association: `NONE`

“RKV_BREAKPOINT init、RKV_BREAKPOINT runtime_enabled、RKV_BREAKPOINT query_cache_update，RKV_BREAKPOINT compress_selected 和 RKV_BREAKPOINT compress_written。现在能看到这些指标。
当前性能是E2E：138504 TTFT: 9057TPOT：126
这是基线的E2E：62676.8 TTFT: 8883.5 TPOT：52.6

但你必须要明白，我们的目标一定要性能超越基线至少30%，同时精度不能掉点。请你修改首先依据当前项目已有的R-KV实现为核心，论文思想为指导来实现，已获得论文提出的推理加速收益。现在请你排查一下是不是进到核心rkv的算法里面 就会慢，打一下相应的时延断点，然后请你现在继续优化性能

---

### 评论 #57 — @xj-zhang2018 at 2026-06-08 03:53:48 UTC
- Comment id: `4645269136`
- Created: 2026-06-08 03:53:48 UTC
- Updated: 2026-06-08 03:53:48 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4645269136
- Author association: `OWNER`

已处理这条反馈，提交并推送到既有分支：`codex/issue-1-feedback`。

处理摘要：
- 增加 R-KV 核心路径的毫秒级 timing 断点，用于判断慢点是在 `gather_key`、`select_indices`、attention score、similarity、top-k 还是 KV 写回。
- 新增 `VLLM_ASCEND_RKV_BREAKPOINT=timing` 模式：只输出 `RKV_BREAKPOINT timing_*`，不会像 `log` 一样每层每步输出 `runtime_enabled/query_cache_update/compress_*`，避免 debug 日志本身把 TPOT 拉高。
- decode forward 中 RKV runtime enable 判定从每层两次降为一次，减少开启调试时的重复日志/重复判定开销。
- 保留现有 R-KV 论文核心实现：attention importance + redundancy similarity + aggregate token selection + 跨层共享 selection + 原地 KV selection 写回。

远端版本：
- branch: `codex/issue-1-feedback`
- commit: `5898eef2590b143614c1479e2e0426822f1b7cac`
- GitHub: https://github.com/xj-zhang2018/R-KV-vllm-ascend/commit/5898eef2590b143614c1479e2e0426822f1b7cac

验证结果：
- 通过：`python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`
- 通过：`git diff --check`
- 未能在本机完整跑单测：当前机器缺 `pytest`，并且 `unittest` 导入时缺 `torch`。需要在 Ascend/vLLM 运行环境中补跑 RKV 相关 UT/E2E。

服务化推理启动方式：

1. 用 timing 模式排查核心慢点，注意这个模式会同步设备计时，只用于诊断，不用于真实性能口径：

``​`bash
cd /Users/zhangxiangjun/我的项目/R-KV/R-KV-main/other_code/vllm-ascend-releases-v0.18.0
export PYTHONPATH=$PWD:${PYTHONPATH}
export VLLM_USE_V1=1
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=1024
export VLLM_ASCEND_RKV_BUFFER=512
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_KERNEL_SIZE=7
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.1
export VLLM_ASCEND_RKV_RETAIN_RATIO=0.1
export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last
export VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=16
export VLLM_ASCEND_RKV_SELECTION_MODE=aggregate
export VLLM_ASCEND_RKV_SHARE_SELECTION=1
export VLLM_ASCEND_RKV_BREAKPOINT=timing

vllm serve "$MODEL_PATH" \
  --host 0.0.0.0 \
  --port 8000 \
  --tensor-parallel-size "$TP_SIZE" \
  --trust-remote-code
``​`

启动后重点 grep：

``​`bash
grep 'RKV_BREAKPOINT timing_' rkv_server.log
``​`

会看到这些核心耗时点：`timing_gather_key`、`timing_select_indices`、`timing_attention_scores`、`timing_attention_pool`、`timing_similarity_sampled` 或 `timing_similarity_full`、`timing_similarity`、`timing_score_topk`、`timing_write_selection`、`timing_compress_request`、`timing_select_cache_hit`。

2. 跑真实性能对比时关闭断点日志：

``​`bash
export VLLM_ASCEND_RKV_BREAKPOINT=off
# 其余 RKV 参数保持与上面一致，再启动同一个 vllm serve 命令
``​`

后续建议：
- 请分别贴两组结果：`VLLM_ASCEND_RKV_BREAKPOINT=timing` 的 `RKV_BREAKPOINT timing_*` 日志，以及 `VLLM_ASCEND_RKV_BREAKPOINT=off` 的 E2E/TTFT/TPOT。
- 当前这组 `BREAKPOINT=log` 下的 TPOT 可能包含大量 warning 日志开销，不能直接作为最终性能口径；最终是否达到“超越基线至少 30% 且精度不掉点”，需要用 `off` 模式重新测。

本次修改文件：
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`


---

### 评论 #58 — @sunao2000123 at 2026-06-08 06:51:43 UTC
- Comment id: `4646145058`
- Created: 2026-06-08 06:51:43 UTC
- Updated: 2026-06-08 06:51:43 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4646145058
- Author association: `NONE`

当前TPOT125ms,基线52.6。我截取了一部分的性能指标，首先分析一下RKV有没有起作用，再进一步根据这些时延进行优化，最终的目标是超过baseline百分之三十
RKV_BREAKPOINT timing_select_cache_hit req_id=chatcmpl-874d521c05ed1300-9fe030e2 seq_len=640 elapsed_ms=0.000
(Worker_PP1_TP1 pid=56134) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.165 req_id=chatcmpl-bf5d8118c1ec5927-867ead20 seq_len=640 selected_tokens=504 observation=8
(Worker_PP1_TP0 pid=56133) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.161 req_id=chatcmpl-bf5d8118c1ec5927-867ead20 seq_len=640 selected_tokens=504 observation=8
(Worker_PP1_TP3 pid=56136) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.165 req_id=chatcmpl-874d521c05ed1300-9fe030e2 seq_len=640 selected_tokens=504 observation=8
(Worker_PP1_TP1 pid=56134) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.579 req_id=chatcmpl-bf5d8118c1ec5927-867ead20 seq_len=640
(Worker_PP1_TP0 pid=56133) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.579 req_id=chatcmpl-bf5d8118c1ec5927-867ead20 seq_len=640
(Worker_PP1_TP3 pid=56136) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.610 req_id=chatcmpl-874d521c05ed1300-9fe030e2 seq_len=640
(Worker_PP1_TP3 pid=56136) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_select_cache_hit req_id=chatcmpl-bf5d8118c1ec5927-867ead20 seq_len=640 elapsed_ms=0.000
(Worker_PP1_TP2 pid=56135) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.197 req_id=chatcmpl-874d521c05ed1300-9fe030e2 seq_len=640 selected_tokens=504 observation=8
(Worker_PP1_TP2 pid=56135) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.630 req_id=chatcmpl-874d521c05ed1300-9fe030e2 seq_len=640
(Worker_PP1_TP2 pid=56135) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_select_cache_hit req_id=chatcmpl-bf5d8118c1ec5927-867ead20 seq_len=640 elapsed_ms=0.000
(Worker_PP1_TP3 pid=56136) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.159 req_id=chatcmpl-bf5d8118c1ec5927-867ead20 seq_len=640 selected_tokens=504 observation=8
(Worker_PP1_TP3 pid=56136) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.590 req_id=chatcmpl-bf5d8118c1ec5927-867ead20 seq_len=640
(Worker_PP1_TP2 pid=56135) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.190 req_id=chatcmpl-bf5d8118c1ec5927-867ead20 seq_len=640 selected_tokens=504 observation=8
(Worker_PP1_TP2 pid=56135) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.619 req_id=chatcmpl-bf5d8118c1ec5927-867ead20 seq_len=640
(Worker_PP1_TP0 pid=56133) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_select_cache_hit req_id=chatcmpl-ab0d8344305b412e-be605cf9 seq_len=640 elapsed_ms=0.000
(Worker_PP1_TP1 pid=56134) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_select_cache_hit req_id=chatcmpl-ab0d8344305b412e-be605cf9 seq_len=640 elapsed_ms=0.000
(Worker_PP1_TP3 pid=56136) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_select_cache_hit req_id=chatcmpl-ab0d8344305b412e-be605cf9 seq_len=640 elapsed_ms=0.000
(Worker_PP1_TP1 pid=56134) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.134 req_id=chatcmpl-ab0d8344305b412e-be605cf9 seq_len=640 selected_tokens=504 observation=8
(Worker_PP1_TP0 pid=56133) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.165 req_id=chatcmpl-ab0d8344305b412e-be605cf9 seq_len=640 selected_tokens=504 observation=8
(Worker_PP1_TP1 pid=56134) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.584 req_id=chatcmpl-ab0d8344305b412e-be605cf9 seq_len=640
(Worker_PP1_TP0 pid=56133) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.635 req_id=chatcmpl-ab0d8344305b412e-be605cf9 seq_len=640
(Worker_PP1_TP1 pid=56134) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_select_cache_hit req_id=chatcmpl-b2646543803942b7-9598e0ea seq_len=640 elapsed_ms=0.000
(Worker_PP1_TP0 pid=56133) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_select_cache_hit req_id=chatcmpl-b2646543803942b7-9598e0ea seq_len=640 elapsed_ms=0.000
(Worker_PP1_TP2 pid=56135) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_select_cache_hit req_id=chatcmpl-ab0d8344305b412e-be605cf9 seq_len=640 elapsed_ms=0.000
(Worker_PP1_TP3 pid=56136) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.183 req_id=chatcmpl-ab0d8344305b412e-be605cf9 seq_len=640 selected_tokens=504 observation=8
(Worker_PP1_TP3 pid=56136) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.653 req_id=chatcmpl-ab0d8344305b412e-be605cf9 seq_len=640
(Worker_PP1_TP3 pid=56136) WARNING 06-08 06:35:12 [attention_v1.py:99] RKV_BREAKPOINT timing_select_cache_hit req_id=chatcmpl-b2646543803942b7-9598e0ea seq_len=640 elapsed_ms=0.000

---

### 评论 #59 — @xj-zhang2018 at 2026-06-08 06:58:09 UTC
- Comment id: `4646182808`
- Created: 2026-06-08 06:58:09 UTC
- Updated: 2026-06-08 06:58:09 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4646182808
- Author association: `OWNER`

已处理这轮性能反馈，提交到了现有分支 `codex/issue-1-feedback`。

处理摘要：
- 从你给的日志看，RKV 已经在起作用：`seq_len=640` 时选择了 `selected_tokens=504`，并保留 `observation=8`，实际写回长度约为 `512`。
- 但这个配置下 KV 长度只从 640 降到 512，下降约 20%。如果当前 baseline TPOT 是 52.6ms，要做到再快 30%，仅靠这个压缩比例理论上不够，还需要更低 budget、更多长上下文收益，或继续降低压缩/写 cache 开销。
- 本次代码把 RKV 压缩从 attention 之后前移到本层 decode attention 之前，并且只在当前层 attention 调用期间临时使用压缩后的有效 KV 长度。这样触发压缩的那个 token 不再先按 640 跑完 attention 后才压缩到 512，下一层也不会因为 metadata 被永久改写而跳过自己的压缩。
- 新增 `RKV_BREAKPOINT timing_effective_len`，在 `VLLM_ASCEND_RKV_BREAKPOINT=timing` 时能看到本层 attention 实际使用的 `original_seq_lens` 和 `effective_seq_lens`，用于确认压缩长度是否真正进入 kernel 入参。

验证结果：
- 通过：`python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`
- 通过：`git diff --check`
- 未能在本机完整跑单测：`python3 -m pytest ...` 失败，因为本机没有 `pytest`；`python3 -m unittest discover ...` 失败，因为本机没有 `torch`。

远端分支 / commit：
- 分支：`codex/issue-1-feedback`
- commit：`efe594b637e43159febdd6a9d6997685b165a2a3`
- 链接：https://github.com/xj-zhang2018/R-KV-vllm-ascend/commit/efe594b637e43159febdd6a9d6997685b165a2a3

如何拉起本次版本的服务化推理：
``​`bash
git fetch origin codex/issue-1-feedback
git checkout codex/issue-1-feedback
git pull --ff-only origin codex/issue-1-feedback

export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=512
export VLLM_ASCEND_RKV_BUFFER=128
export VLLM_ASCEND_RKV_BREAKPOINT=timing
# 其他 vLLM/NPU/模型参数沿用你当前的服务启动函数或 vllm serve 命令
# 真实 TPOT 性能测试时请改为：export VLLM_ASCEND_RKV_BREAKPOINT=off
``​`

建议下一轮验证：
1. 先用 `VLLM_ASCEND_RKV_BREAKPOINT=timing` 跑一小轮，确认出现 `timing_effective_len original_seq_lens=[640] effective_seq_lens=[512]` 或类似日志。
2. 再用 `VLLM_ASCEND_RKV_BREAKPOINT=off` 跑 TPOT，避免同步计时日志影响性能。
3. 如果 TPOT 仍明显高于 baseline，请继续贴 `timing_effective_len`、`timing_compress_request` 和最终 TPOT。下一步我建议直接做 budget/ratio 约束，例如把有效 KV 长度压到触发长度的 70% 以下，才有机会接近“比 baseline 快 30%”这个目标。

本次修改文件：
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`


---

### 评论 #60 — @sunao2000123 at 2026-06-08 07:30:17 UTC
- Comment id: `4646379262`
- Created: 2026-06-08 07:30:17 UTC
- Updated: 2026-06-08 07:30:17 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4646379262
- Author association: `NONE`

这是关闭time模式的结果。
E2E 125858.8 TTFT 8992.9 TPOT114.2
基线的E2E：62676.8 TTFT: 8883.5 TPOT：52.6
timing_effective_len、timing_compress_request没有改变。
现在分析一下问题出在哪里，并进一步进行优化，最终目标超越基线至少 30% 且精度不掉点。

---

### 评论 #61 — @xj-zhang2018 at 2026-06-08 07:38:50 UTC
- Comment id: `4646432363`
- Created: 2026-06-08 07:38:50 UTC
- Updated: 2026-06-08 07:38:50 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4646432363
- Author association: `OWNER`

处理了这条性能反馈，已推送到远端分支 `codex/issue-1-feedback`。

### 处理摘要

这次主要针对“关闭 timing 后 RKV 仍明显慢于基线，且 `timing_effective_len` / `timing_compress_request` 没有改善”的最可疑链路做修复：RKV 压缩后，runner 需要把压缩后的 effective KV length 持久化到下一步 decode，否则后续 token 仍可能按原始 seq_len 触发压缩，导致 `compress_request` 近似每步发生，TPOT 被压缩/搬移开销打穿。

已有代码只取第一个带 `rkv_compressed_lens` 的 attention metadata。多层/多 attention group 场景下，如果不同层或 group 上报不一致，runner 可能错过部分请求的压缩结果。这次改为遍历所有 layer metadata，并按 request 合并最小的正向压缩长度，再写回 `rkv_effective_kv_lens`。这样下一步 decode 的 `rkv_seq_lens` 和 slot mapping 会更稳地使用压缩后的长度，避免重复按长上下文压缩。

同时需要注意：如果继续使用 `budget=512, buffer=128`，effective length 会在约 513 到 640 之间运行。这个配置更偏保精度，理论上不一定能达到“比基线快 30%”的目标。下面给了一个更偏性能的复测配置，建议先用小样本验证精度不掉点，再扩大压测。

### 验证结果

- `python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/worker/model_runner_v1.py other_code/vllm-ascend-releases-v0.18.0/tests/ut/worker/test_model_runner_v1.py`：通过
- `git diff --check`：通过
- `PYTHONPATH=. python3 -m unittest tests.ut.worker.test_model_runner_v1`：本地环境缺少 `torch`，导入阶段失败，未能执行断言
- 当前机器没有 Ascend/NPU 服务化压测环境，因此 E2E/TPOT 和精度回归需要在目标机器复测

### 远端版本

- 分支：`codex/issue-1-feedback`
- commit：`37ca68b2719194c3cb4a0ca38c44c92b1bc8e737`

### 如何拉取本次版本

``​`bash
git fetch origin
git checkout codex/issue-1-feedback
git pull --ff-only origin codex/issue-1-feedback
``​`

### 服务化推理启动建议

先用偏性能配置复测，目标是确认 `compress_request` 不再每步触发，并观察 TPOT 是否显著低于基线：

``​`bash
cd other_code/vllm-ascend-releases-v0.18.0
export VLLM_USE_V1=1
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=384
export VLLM_ASCEND_RKV_BUFFER=64
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_KERNEL_SIZE=7
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.1
export VLLM_ASCEND_RKV_RETAIN_RATIO=0.1
export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last
export VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=8
export VLLM_ASCEND_RKV_SELECTION_MODE=aggregate
export VLLM_ASCEND_RKV_SHARE_SELECTION=1
export VLLM_ASCEND_RKV_BREAKPOINT=off

vllm serve <MODEL_PATH> \
  --served-model-name <MODEL_NAME> \
  --max-model-len <MAX_MODEL_LEN> \
  --enforce-eager
``​`

如果这个配置精度掉点，把 `VLLM_ASCEND_RKV_BUDGET` 逐步调回 `512`；如果精度稳定但速度仍不够，再尝试 `VLLM_ASCEND_RKV_BUDGET=256`、`VLLM_ASCEND_RKV_BUFFER=64`。建议只在少量请求上临时把 `VLLM_ASCEND_RKV_BREAKPOINT=log` 打开确认链路：第一次压缩后，下一步的 effective seq len 应该接近 `budget + 1`，而不是原始长上下文长度。

### 本次修改文件

- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/worker/model_runner_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/worker/test_model_runner_v1.py`

后续复测请回传这两组信息：RKV 配置环境变量、`VLLM_ASCEND_RKV_BREAKPOINT=log` 下连续 3 到 5 个 token 的 `runtime_enabled / timing_effective_len / timing_compress_request` 片段，以及同一批请求的 E2E/TTFT/TPOT/精度结果。


---

### 评论 #62 — @sunao2000123 at 2026-06-08 08:05:36 UTC
- Comment id: `4646607249`
- Created: 2026-06-08 08:05:36 UTC
- Updated: 2026-06-08 08:05:36 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4646607249
- Author association: `NONE`

这是开启timing的结果：E2E 132084,TTFT 8937.4， TPOT 120.4
这是off的结果：E2E 128876.1,TTFT 9129.1， TPOT 117.1
这是基线的E2E：62676.8 TTFT: 8883.5 TPOT：52.6
本次启动参数：
export VLLM_USE_V1=1
    export VLLM_ASCEND_RKV_ENABLE=1
    export VLLM_ASCEND_RKV_BUDGET=256
    export VLLM_ASCEND_RKV_BUFFER=128
    export VLLM_ASCEND_RKV_WINDOW_SIZE=8
    export VLLM_ASCEND_RKV_KERNEL_SIZE=7
    export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
    export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
    export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last
    export VLLM_ASCEND_RKV_BREAKPOINT=log
    export VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=16
    export VLLM_ASCEND_RKV_SELECTION_MODE=aggregate
    export VLLM_ASCEND_RKV_SHARE_SELECTION=1
    export VLLM_ASCEND_RKV_BREAKPOINT=off
只改了budget，但是没有什么特别大的影响。
这是grep -n "RKV_BREAKPOINT"的结果。分析可能存在的问题，并进一步优化。
(Worker_PP1_TP0 pid=60111) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_similarity elapsed_ms=6.746 kv_cache_len=10015 observation=1
(Worker_PP1_TP2 pid=60113) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_attention_scores elapsed_ms=0.239 kv_cache_len=9562 observation=1
(Worker_PP1_TP3 pid=60114) WARNING 06-08 07:45:24 [attention_v1.py:99] RKV_BREAKPOINT timing_gather_key elapsed_ms=0.277 req_id=chatcmpl-955e81e13c9756de-9641404e seq_len=9562
(Worker_PP1_TP0 pid=60111) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_score_topk elapsed_ms=0.289 keep_old=255 mix_lambda=0.07 selection_mode=aggregate
(Worker_PP1_TP1 pid=60112) WARNING 06-08 07:45:24 [attention_v1.py:99] RKV_BREAKPOINT timing_gather_key elapsed_ms=0.279 req_id=chatcmpl-955e81e13c9756de-9641404e seq_len=9562
(Worker_PP1_TP0 pid=60111) WARNING 06-08 07:45:24 [attention_v1.py:99] RKV_BREAKPOINT timing_select_indices elapsed_ms=8.658 req_id=chatcmpl-81f1b619ec351ef6-b51cf7ab seq_len=10015
(Worker_PP1_TP2 pid=60113) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_attention_pool elapsed_ms=0.405 observation=1 kernel_size=7
(Worker_PP1_TP3 pid=60114) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_attention_scores elapsed_ms=0.244 kv_cache_len=9562 observation=1
(Worker_PP1_TP1 pid=60112) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_attention_scores elapsed_ms=0.249 kv_cache_len=9562 observation=1
(Worker_PP1_TP3 pid=60114) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_attention_pool elapsed_ms=0.428 observation=1 kernel_size=7
(Worker_PP1_TP1 pid=60112) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_attention_pool elapsed_ms=0.426 observation=1 kernel_size=7
(Worker_PP1_TP0 pid=60111) WARNING 06-08 07:45:24 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.277 req_id=chatcmpl-81f1b619ec351ef6-b51cf7ab seq_len=10015 selected_tokens=255 observation=1
(Worker_PP1_TP0 pid=60111) WARNING 06-08 07:45:24 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=11.179 req_id=chatcmpl-81f1b619ec351ef6-b51cf7ab seq_len=10015
(Worker_PP1_TP0 pid=60111) WARNING 06-08 07:45:24 [attention_v1.py:99] RKV_BREAKPOINT timing_gather_key elapsed_ms=0.303 req_id=chatcmpl-955e81e13c9756de-9641404e seq_len=9562
(Worker_PP1_TP0 pid=60111) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_attention_scores elapsed_ms=0.242 kv_cache_len=9562 observation=1
(Worker_PP1_TP0 pid=60111) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_attention_pool elapsed_ms=0.419 observation=1 kernel_size=7
(Worker_PP1_TP2 pid=60113) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_similarity_sampled elapsed_ms=5.747 num_heads=2 seq_len=9562 sample_count=16
(Worker_PP1_TP2 pid=60113) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_similarity elapsed_ms=6.316 kv_cache_len=9562 observation=1
(Worker_PP1_TP2 pid=60113) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_score_topk elapsed_ms=0.260 keep_old=255 mix_lambda=0.07 selection_mode=aggregate
(Worker_PP1_TP3 pid=60114) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_similarity_sampled elapsed_ms=5.769 num_heads=2 seq_len=9562 sample_count=16
(Worker_PP1_TP1 pid=60112) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_similarity_sampled elapsed_ms=5.695 num_heads=2 seq_len=9562 sample_count=16
(Worker_PP1_TP2 pid=60113) WARNING 06-08 07:45:24 [attention_v1.py:99] RKV_BREAKPOINT timing_select_indices elapsed_ms=8.137 req_id=chatcmpl-955e81e13c9756de-9641404e seq_len=9562
(Worker_PP1_TP3 pid=60114) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_similarity elapsed_ms=6.354 kv_cache_len=9562 observation=1
(Worker_PP1_TP1 pid=60112) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_similarity elapsed_ms=6.288 kv_cache_len=9562 observation=1
(Worker_PP1_TP3 pid=60114) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_score_topk elapsed_ms=0.272 keep_old=255 mix_lambda=0.07 selection_mode=aggregate
(Worker_PP1_TP1 pid=60112) WARNING 06-08 07:45:24 [rkv.py:61] RKV_BREAKPOINT timing_score_topk elapsed_ms=0.278 keep_old=255 mix_lambda=0.07 selection_mode=aggregate
(Worker_PP1_TP3 pid=60114) WARNING 06-08 07:45:24 [attention_v1.py:99] RKV_BREAKPOINT timing_select_indices elapsed_ms=8.256 req_id=chatcmpl-955e81e13c9756de-9641404e seq_len=9562
(Worker_PP1_TP1 pid=60112) WARNING 06-08 07:45:24 [attention_v1.py:99] RKV_BREAKPOINT timing_select_indices elapsed_ms=8.226 req_id=chatcmpl-955e81e13c9756de-9641404e seq_len=9562
(Worker_PP1_TP2 pid=60113) WARNING 06-08 07:45:24 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.129 req_id=chatcmpl-955e81e13c9756de-9641404e seq_len=9562 selected_tokens=255 observation=1
(Worker_PP1_TP2 pid=60113) WARNING 06-08 07:45:24 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=10.321 req_id=chatcmpl-955e81e13c9756de-9641404e seq_len=9562

---

### 评论 #63 — @xj-zhang2018 at 2026-06-08 08:19:05 UTC
- Comment id: `4646704151`
- Created: 2026-06-08 08:19:05 UTC
- Updated: 2026-06-08 08:19:05 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4646704151
- Author association: `OWNER`

已处理这轮反馈（comment `4646607249`），提交已推送到远端分支：`codex/issue-1-feedback`，commit：`518b37d9 Optimize RKV compression diagnostics`。

处理摘要：
- 你贴的日志里 `seq_len=9k/10k` 出现在 `compress_request` 阶段，这本身可能是首次长 prompt decode 后第一次压缩，不能单独证明下一轮 attention 没吃到压缩长度；但缺少 runner 侧状态日志，之前确实很难判断。
- 发现 `observation=1` 的根因是 prefill 阶段没有 query cache，长 prompt 后第一步 decode 只有 1 个 query 就触发了压缩。现在默认路径会等待 query window 收满后再做首次压缩，避免用单 token 观测直接压缩 10k 上下文。
- 增加了 runner 侧状态日志：`timing_state_effective_before` / `timing_state_effective_update`，用于确认压缩后的 effective KV len 是否被下一轮 decode 采用。
- 增加了 `VLLM_ASCEND_RKV_SELECTION_MODE=attention_only`，跳过 redundancy similarity，仅按 attention 重要性选 token。这个模式主要用于服务化测速/定位 similarity 开销瓶颈；默认 `aggregate` 仍保留 R-KV 的 attention + redundancy 逻辑。

验证结果：
- 已通过：`python3 -m py_compile` 覆盖本次修改的 R-KV/attention/runner/env/tests 文件。
- 已通过：`git diff --check`。
- 未能在本机完整跑 unittest：当前 Python 环境缺少 `torch`，`python3 -m unittest tests.ut.test_rkv tests.ut.attention.test_attention_v1 tests.ut.worker.test_model_runner_v1` 在 import 阶段报 `ModuleNotFoundError: No module named 'torch'`。

建议下一轮服务化推理启动方式（注意不要同时设置 `BREAKPOINT=log` 和后面的 `BREAKPOINT=off`，后者会覆盖前者）：

``​`bash
git fetch origin
git checkout codex/issue-1-feedback
git pull --ff-only origin codex/issue-1-feedback
cd other_code/vllm-ascend-releases-v0.18.0
export PYTHONPATH=$PWD:${PYTHONPATH}

export VLLM_USE_V1=1
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=256
export VLLM_ASCEND_RKV_BUFFER=128
export VLLM_ASCEND_RKV_WINDOW_SIZE=8
export VLLM_ASCEND_RKV_KERNEL_SIZE=7
export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last
export VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=16
export VLLM_ASCEND_RKV_SELECTION_MODE=aggregate
export VLLM_ASCEND_RKV_SHARE_SELECTION=1
export VLLM_ASCEND_RKV_BREAKPOINT=timing

vllm serve <MODEL_PATH_OR_ID> --tensor-parallel-size <TP> --max-model-len <MAX_MODEL_LEN> --enforce-eager
``​`

测速定位 similarity 开销时，只改这一项再跑一组：

``​`bash
export VLLM_ASCEND_RKV_SELECTION_MODE=attention_only
``​`

建议 grep 这些日志：

``​`bash
grep -E "RKV_BREAKPOINT (timing_compress_wait_query_window|timing_compress_request|timing_select_indices|timing_similarity|timing_state_effective_before|timing_state_effective_update|timing_effective_len)" <server_log>
``​`

预期现象：
- 首次达到触发阈值后，前几步可能看到 `timing_compress_wait_query_window cached_tokens=<8 required_tokens=8`。
- 压缩写入后应看到 `timing_state_effective_update ... compressed_len=256 next_len=256`。
- 下一步 decode 前应看到 `timing_state_effective_before ... original_len=100xx effective_len=256/257/...`。
- 如果 update 后下一步 before 仍是 `effective_len=100xx`，说明状态传播仍有问题；如果 effective len 已经是 256 左右但 TPOT 仍接近 full length，则下一步应继续查 Ascend paged attention 是否实际使用了 patched `seq_lens`。

本次修改文件：
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/rkv.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/worker/model_runner_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/envs.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/test_rkv.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`


---

### 评论 #64 — @sunao2000123 at 2026-06-08 08:47:22 UTC
- Comment id: `4646903498`
- Created: 2026-06-08 08:47:22 UTC
- Updated: 2026-06-08 08:47:22 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4646903498
- Author association: `NONE`

结果： E2EL 131529.1 TTFT 9094.3  TPOT 119.7
注意到elapsed_ms全部等于=0.000，并且没有effctive_len等字眼。请你分析原因并进一步优化。
 RKV_BREAKPOINT timing_state_effective_update elapsed_ms=0.000 req_id=chatcmpl-8a73e89d197ff5e0-a8b45b06 previous_len=319 scheduled_tokens=1 compressed_len=0 next_len=320
(Worker_PP1_TP3 pid=63680) WARNING 06-08 08:29:05 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_update elapsed_ms=0.000 req_id=chatcmpl-b591cf66f48807d7-8b9fb5d7 previous_len=318 scheduled_tokens=1 compressed_len=0 next_len=319
(Worker_PP0_TP2 pid=63675) WARNING 06-08 08:29:05 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_update elapsed_ms=0.000 req_id=chatcmpl-b35c81f1b11f9c0f-966186e0 previous_len=319 scheduled_tokens=1 compressed_len=0 next_len=320

(Worker_PP1_TP2 pid=63679) WARNING 06-08 08:29:05 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_before elapsed_ms=0.000 req_id=chatcmpl-a18fe3c93004458f-806d4d81 original_len=9937 effective_len=319
(Worker_PP1_TP2 pid=63679) WARNING 06-08 08:29:05 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_before elapsed_ms=0.000 req_id=chatcmpl-bec69cb687d86077-82f8ebe0 original_len=10085 effective_len=319
(Worker_PP1_TP2 pid=63679) WARNING 06-08 08:29:05 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_before elapsed_ms=0.000 req_id=chatcmpl-9a1ba9082e001815-9d2f3b22 original_len=9632 effective_len=319


(Worker_PP1_TP0 pid=63677) WARNING 06-08 08:29:05 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_update elapsed_ms=0.000 req_id=chatcmpl-bec69cb687d86077-82f8ebe0 previous_len=319 scheduled_tokens=1 compressed_len=0 next_len=320
(Worker_PP1_TP0 pid=63677) WARNING 06-08 08:29:05 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_update elapsed_ms=0.000 req_id=chatcmpl-9a1ba9082e001815-9d2f3b22 previous_len=319 scheduled_tokens=1 compressed_len=0 next_len=320
(Worker_PP1_TP0 pid=63677) WARNING 06-08 08:29:05 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_update elapsed_ms=0.000 req_id=chatcmpl-b591cf66f48807d7-8b9fb5d7 previous_len=319 scheduled_tokens=1 compressed_len=0 next_len=320


(Worker_PP1_TP2 pid=63679) WARNING 06-08 08:29:05 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_update elapsed_ms=0.000 req_id=chatcmpl-8a73e89d197ff5e0-a8b45b06 previous_len=319 scheduled_tokens=1 compressed_len=0 next_len=320
(Worker_PP1_TP2 pid=63679) WARNING 06-08 08:29:05 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_update elapsed_ms=0.000 req_id=chatcmpl-b35c81f1b11f9c0f-966186e0 previous_len=319 scheduled_tokens=1 compressed_len=0 next_len=320
(Worker_PP1_TP2 pid=63679) WARNING 06-08 08:29:05 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_update elapsed_ms=0.000 req_id=chatcmpl-b1e5dd26ba6cac42-bd8ca83b previous_len=319 scheduled_tokens=1 compressed_len=0 next_len=320

---

### 评论 #65 — @xj-zhang2018 at 2026-06-08 08:54:09 UTC
- Comment id: `4646951681`
- Created: 2026-06-08 08:54:09 UTC
- Updated: 2026-06-08 08:54:09 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4646951681
- Author association: `OWNER`

已处理这轮反馈，提交已推送到现有分支 `codex/issue-1-feedback`。

处理摘要：
- 先说明日志含义：`timing_state_effective_update elapsed_ms=0.000` / `timing_state_effective_before elapsed_ms=0.000` 是我前一版加的状态标记日志，不是实际耗时采样；真实耗时日志会来自 `timing_compress_request`、`timing_attention_forward` 等需要同步计时的事件。
- 你贴出的日志里其实已经有有效长度字段，例如 `original_len=9937 effective_len=319`、`original_len=10085 effective_len=319`，说明 runner 侧的有效 KV 长度传播已经生效。
- 这次继续优化 paged attention 输入：当 R-KV 生效并把 `seq_lens` 降到有效长度后，同步裁剪传给 `_npu_paged_attention` 的 `block_tables` 列数，避免 NPU PA 调用仍携带原始 9k/10k token 对应的长 block table 形状。
- 新增诊断日志 `RKV_BREAKPOINT timing_block_table_trim elapsed_ms=0.000 original_blocks=... effective_blocks=... max_context_len=... block_size=...`。例如 `effective_len≈319`、`block_size=128` 时，`effective_blocks` 应该是 3；如果原来 `original_blocks` 是 80 左右，这条日志能直接确认 block table 已被裁剪。

验证结果：
- `python3 -m py_compile other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`：通过。
- `git diff --check`：通过。
- `python3 -m unittest tests.ut.attention.test_attention_v1`：本机环境缺少 `torch`，导入阶段失败，未能执行真实单测；已补充对应单测用例。

远端版本：
- 分支：`codex/issue-1-feedback`
- commit：`47168f5e Trim RKV paged attention block tables`

服务化推理拉起建议：
``​`bash
cd other_code/vllm-ascend-releases-v0.18.0
export VLLM_USE_V1=1
export VLLM_ASCEND_RKV_ENABLE=1
export VLLM_ASCEND_RKV_BUDGET=256
export VLLM_ASCEND_RKV_BUFFER=64
export VLLM_ASCEND_RKV_SELECTION_MODE=attention_only
export VLLM_ASCEND_RKV_BREAKPOINT=timing
# 注意不要在后面再 export VLLM_ASCEND_RKV_BREAKPOINT=off，否则会覆盖 timing/log。
python -m vllm.entrypoints.openai.api_server \
  --model <MODEL_PATH> \
  --served-model-name <SERVED_MODEL_NAME> \
  --host 0.0.0.0 \
  --port 8000 \
  --tensor-parallel-size <TP> \
  --pipeline-parallel-size <PP> \
  --max-model-len <MAX_MODEL_LEN>
``​`

下一轮请重点看这几类日志：
- `timing_state_effective_before original_len=... effective_len=...`
- `timing_effective_len original_seq_lens=... effective_seq_lens=...`
- `timing_block_table_trim original_blocks=... effective_blocks=...`
- `timing_attention_forward elapsed_ms=...`

如果 `effective_len` 和 `effective_blocks` 都已经降下来但 TPOT 仍然接近 120ms，那么下一个主要瓶颈大概率不是有效长度传播，而是当前 R-KV 为了动态改写 KV cache 仍禁用了 ACL graph，导致 decode 走 eager/非图路径的固定开销偏高；后续我会基于这轮新日志继续评估是否能做“压缩完成后恢复图路径”或 PA workspace 缓存级优化。

本次修改文件：
- `other_code/vllm-ascend-releases-v0.18.0/vllm_ascend/attention/attention_v1.py`
- `other_code/vllm-ascend-releases-v0.18.0/tests/ut/attention/test_attention_v1.py`


---

### 评论 #66 — @sunao2000123 at 2026-06-08 11:03:52 UTC
- Comment id: `4648232820`
- Created: 2026-06-08 11:03:52 UTC
- Updated: 2026-06-08 11:03:52 UTC
- URL: https://github.com/xj-zhang2018/R-KV-vllm-ascend/issues/1#issuecomment-4648232820
- Author association: `NONE`

 各项性能均几乎没有提升。启动方式如下
export VLLM_USE_V1=1
    export VLLM_ASCEND_RKV_ENABLE=1
    export VLLM_ASCEND_RKV_BUDGET=256
    export VLLM_ASCEND_RKV_BUFFER=64
    export VLLM_ASCEND_RKV_WINDOW_SIZE=8
    export VLLM_ASCEND_RKV_KERNEL_SIZE=7
    export VLLM_ASCEND_RKV_MIX_LAMBDA=0.07
    export VLLM_ASCEND_RKV_RETAIN_RATIO=0.2
    export VLLM_ASCEND_RKV_RETAIN_DIRECTION=last
    export VLLM_ASCEND_RKV_SIMILARITY_SAMPLE_SIZE=16
    export VLLM_ASCEND_RKV_SELECTION_MODE=aggregate
    export VLLM_ASCEND_RKV_SHARE_SELECTION=1
    export VLLM_ASCEND_RKV_BREAKPOINT=timing
没有timing_block_table_trim original_blocks以及timing_attention_forward elapsed_ms。进一步排查问题，并进行优化。
(Worker_PP0_TP2 pid=65929) WARNING 06-08 10:50:10 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_before elapsed_ms=0.000 req_id=chatcmpl-99b68732419cdca4-a8469d21 original_len=10202 effective_len=294
(Worker_PP1_TP3 pid=65934) WARNING 06-08 10:50:10 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_before elapsed_ms=0.000 req_id=chatcmpl-8979d2b679536d60-b03a6f20 original_len=9761 effective_len=293
(Worker_PP0_TP1 pid=65928) WARNING 06-08 10:50:10 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_before elapsed_ms=0.000 req_id=chatcmpl-99b68732419cdca4-a8469d21 original_len=10202 effective_len=294
(Worker_PP0_TP0 pid=65927) WARNING 06-08 10:50:10 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_before elapsed_ms=0.000 req_id=chatcmpl-a8d61889448d314a-a04d6183 original_len=9344 effective_len=294
(Worker_PP0_TP2 pid=65929) WARNING 06-08 10:50:10 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_before elapsed_ms=0.000 req_id=chatcmpl-bade0b41645fe37f-9c97f7ee original_len=10571 effective_len=294
(Worker_PP1_TP3 pid=65934) WARNING 06-08 10:50:10 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effective_before elapsed_ms=0.000 req_id=chatcmpl-a54c2687a0f519fe-b59862c8 original_len=10303 effective_len=293
(Worker_PP0_TP1 pid=65928) WARNING 06-08 10:50:10 [model_runner_v1.py:189] RKV_BREAKPOINT timing_state_effectiv^C

112297:(Worker_PP0_TP1 pid=65928) WARNING 06-08 10:50:05 [attention_v1.py:99] RKV_BREAKPOINT timing_effective_len elapsed_ms=0.000 original_seq_lens=[320, 320, 320, 320, 320, 320, 320, 320, 320, 320] effective_seq_lens=[256, 256, 256, 256, 256, 256, 256, 256, 256, 256]
112298-(Worker_PP0_TP2 pid=65929) WARNING 06-08 10:50:05 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.162 req_id=chatcmpl-a8d61889448d314a-a04d6183 seq_len=320 selected_tokens=248 observation=8
112299-(Worker_PP0_TP2 pid=65929) WARNING 06-08 10:50:05 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.636 req_id=chatcmpl-a8d61889448d314a-a04d6183 seq_len=320
112300-(Worker_PP0_TP3 pid=65930) WARNING 06-08 10:50:05 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.206 req_id=chatcmpl-bade0b41645fe37f-9c97f7ee seq_len=320 selected_tokens=248 observation=8
112301:(Worker_PP0_TP2 pid=65929) WARNING 06-08 10:50:05 [attention_v1.py:99] RKV_BREAKPOINT timing_effective_len elapsed_ms=0.000 original_seq_lens=[320, 320, 320, 320, 320, 320, 320, 320, 320, 320] effective_seq_lens=[256, 256, 256, 256, 256, 256, 256, 256, 256, 256]
112302-(Worker_PP0_TP3 pid=65930) WARNING 06-08 10:50:05 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.662 req_id=chatcmpl-bade0b41645fe37f-9c97f7ee seq_len=320
112303-(Worker_PP0_TP3 pid=65930) WARNING 06-08 10:50:05 [attention_v1.py:99] RKV_BREAKPOINT timing_select_cache_hit req_id=chatcmpl-a8d61889448d314a-a04d6183 seq_len=320 elapsed_ms=0.000
112304-(Worker_PP0_TP3 pid=65930) WARNING 06-08 10:50:05 [attention_v1.py:99] RKV_BREAKPOINT timing_write_selection elapsed_ms=1.190 req_id=chatcmpl-a8d61889448d314a-a04d6183 seq_len=320 selected_tokens=248 observation=8
112305-(Worker_PP0_TP3 pid=65930) WARNING 06-08 10:50:05 [attention_v1.py:99] RKV_BREAKPOINT timing_compress_request elapsed_ms=1.638 req_id=chatcmpl-a8d61889448d314a-a04d6183 seq_len=320

---

## 统计

- 备份评论数: **66**
- 参与的 GitHub 用户: @sunao2000123, @xj-zhang2018
- 时间跨度: 2026-06-05T02:15:50Z → 2026-06-08T11:03:52Z

---

_End of backup. This file is auto-generated. Do not edit by hand._
