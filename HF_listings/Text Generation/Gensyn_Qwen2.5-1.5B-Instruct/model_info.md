# Gensyn/Qwen2.5-1.5B-Instruct

## Model Information

- **Model ID**: Gensyn/Qwen2.5-1.5B-Instruct
- **Author**: Gensyn
- **Last Updated**: 2025-04-04 02:34:03+00:00
- **Repository**: https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct

## Tags

transformers, safetensors, qwen2, text-generation, chat, rl-swarm, gensyn, conversational, en, base_model:Qwen/Qwen2.5-1.5B, base_model:finetune:Qwen/Qwen2.5-1.5B, license:apache-2.0, autotrain_compatible, text-generation-inference, endpoints_compatible, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/.gitattributes](https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/.gitattributes)
- **LICENSE** (None bytes)
  - Download: [https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/LICENSE](https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/LICENSE)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/README.md](https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/config.json](https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/config.json)
- **generation_config.json** (None bytes)
  - Download: [https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/generation_config.json](https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/generation_config.json)
- **merges.txt** (None bytes)
  - Download: [https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/merges.txt](https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/merges.txt)
- **model.safetensors** (None bytes)
  - Download: [https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/model.safetensors](https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/model.safetensors)
- **tokenizer.json** (None bytes)
  - Download: [https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/tokenizer.json](https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/tokenizer.json)
- **tokenizer_config.json** (None bytes)
  - Download: [https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/tokenizer_config.json](https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/tokenizer_config.json)
- **vocab.json** (None bytes)
  - Download: [https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/vocab.json](https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/resolve/main/vocab.json)


## External Links

- [github.com](https://github.com/gensyn-ai/paper-rl-swarm/blob/main/latest.pdf)
- [github.com](https://github.com/gensyn-ai/rl-swarm)
- [huggingface.co](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct)
- [qwen.readthedocs.io](https://qwen.readthedocs.io/en/latest/)
- [www.gensyn.ai](https://www.gensyn.ai/articles/rl-swarm)
- [www.gensyn.ai](https://www.gensyn.ai/testnet)


## README.md

```markdown
---
license: apache-2.0
license_link: https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct/blob/main/LICENSE
language:
- en
pipeline_tag: text-generation
base_model: Qwen/Qwen2.5-1.5B
tags:
- chat
- rl-swarm
- gensyn
library_name: transformers
---

# Qwen2.5-1.5B-Instruct

## Introduction

This model is intended for use in the [Gensyn RL Swarm](https://www.gensyn.ai/articles/rl-swarm), to finetune locally using peer-to-peer reinforcement learning post-training.

Once finetuned, the model can be used as normal in any workflow, for details on how to do this please refer to the [original model documentation](https://qwen.readthedocs.io/en/latest/).

For more details on the original model, please refer to the original repository [here](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct).

This repo contains an **unmodified version** of the instruction-tuned 1.5B Qwen2.5 model, which has the following features:
- Type: Causal Language Models
- Training Stage: Pretraining & Post-training
- Architecture: transformers with RoPE, SwiGLU, RMSNorm, Attention QKV bias and tied word embeddings
- Number of Parameters: 1.54B
- Number of Paramaters (Non-Embedding): 1.31B
- Number of Layers: 28
- Number of Attention Heads (GQA): 12 for Q and 2 for KV
- Context Length: Full 32,768 tokens and generation 8192 tokens

## Requirements

This model is intended for use in the [Gensyn RL Swarm](https://www.gensyn.ai/articles/rl-swarm) system, for details on model requirements when using outside of a swarm, refer to the original Qwen repo [here](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct).

## Quickstart

To deploy this model into a swarm and/or participate in the Gensyn Testnet, follow the instructions in the [RL Swarm repository](https://github.com/gensyn-ai/rl-swarm), read about the [testnet](https://www.gensyn.ai/testnet), read the [RL Swarm overview](https://www.gensyn.ai/articles/rl-swarm), and/or read the [RL Swarm technical report](https://github.com/gensyn-ai/paper-rl-swarm/blob/main/latest.pdf).

```


---

*Generated on 2025-06-21 15:06:19*
*Source: https://huggingface.co/Gensyn/Qwen2.5-1.5B-Instruct*
