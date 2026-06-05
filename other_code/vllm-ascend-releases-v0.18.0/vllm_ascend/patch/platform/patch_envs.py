# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the vLLM project

import vllm.envs as vllm_envs

from vllm_ascend import envs as ascend_envs


for name, getter in ascend_envs.env_variables.items():
    vllm_envs.env_variables.setdefault(name, getter)
