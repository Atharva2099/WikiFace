# PKU-Alignment/beaver-7b-v1.0-cost

## Model Information

- **Model ID**: PKU-Alignment/beaver-7b-v1.0-cost
- **Author**: PKU-Alignment
- **Last Updated**: 2024-04-20 18:03:39+00:00
- **Repository**: https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost

## Tags

safe-rlhf, safetensors, llama, reinforcement-learning-from-human-feedback, reinforcement-learning, beaver, safety, ai-safety, deepspeed, rlhf, alpaca, en, dataset:PKU-Alignment/PKU-SafeRLHF, arxiv:2302.13971, arxiv:2307.04657, arxiv:2310.12773, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/.gitattributes](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/.gitattributes)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/README.md](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/config.json](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/config.json)
- **model-00001-of-00007.safetensors** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00001-of-00007.safetensors](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00001-of-00007.safetensors)
- **model-00002-of-00007.safetensors** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00002-of-00007.safetensors](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00002-of-00007.safetensors)
- **model-00003-of-00007.safetensors** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00003-of-00007.safetensors](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00003-of-00007.safetensors)
- **model-00004-of-00007.safetensors** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00004-of-00007.safetensors](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00004-of-00007.safetensors)
- **model-00005-of-00007.safetensors** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00005-of-00007.safetensors](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00005-of-00007.safetensors)
- **model-00006-of-00007.safetensors** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00006-of-00007.safetensors](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00006-of-00007.safetensors)
- **model-00007-of-00007.safetensors** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00007-of-00007.safetensors](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model-00007-of-00007.safetensors)
- **model.safetensors.index.json** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model.safetensors.index.json](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/model.safetensors.index.json)
- **special_tokens_map.json** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/special_tokens_map.json](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/special_tokens_map.json)
- **tokenizer.json** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/tokenizer.json](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/tokenizer.json)
- **tokenizer_config.json** (None bytes)
  - Download: [https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/tokenizer_config.json](https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost/resolve/main/tokenizer_config.json)


## External Links

- [arxiv.org](https://arxiv.org/abs/2302.13971)
- [github.com](https://github.com/PKU-Alignment)
- [github.com](https://github.com/tatsu-lab/stanford_alpaca)
- [huggingface.co](https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF)


## README.md

```markdown
---
datasets:
  - PKU-Alignment/PKU-SafeRLHF
language:
  - en
tags:
  - reinforcement-learning-from-human-feedback
  - reinforcement-learning
  - beaver
  - safety
  - llama
  - ai-safety
  - deepspeed
  - rlhf
  - alpaca
library_name: safe-rlhf
---

# 🦫 Beaver's Cost Model

## Model Details

The Beaver cost model is a preference model trained using the [PKU-SafeRLHF](https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF) dataset.
It can play a role in the safe RLHF algorithm, helping the Beaver model become more safe and harmless.

- **Developed by:** the [PKU-Alignment](https://github.com/PKU-Alignment) Team.
- **Model Type:** An auto-regressive language model based on the transformer architecture.
- **License:** Non-commercial license.
- **Fine-tuned from model:** [LLaMA](https://arxiv.org/abs/2302.13971), [Alpaca](https://github.com/tatsu-lab/stanford_alpaca).

## Model Sources

- **Repository:** <https://github.com/PKU-Alignment/safe-rlhf>
- **Beaver:** <https://huggingface.co/PKU-Alignment/beaver-7b-v1.0>
- **Dataset:** <https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF>
- **Reward Model:** <https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-reward>
- **Cost Model:** <https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost>
- **Dataset Paper:** <https://arxiv.org/abs/2307.04657>
- **Paper:** <https://arxiv.org/abs/2310.12773>

## How to Use the Cost Model

```python
import torch
from transformers import AutoTokenizer
from safe_rlhf.models import AutoModelForScore

model = AutoModelForScore.from_pretrained('PKU-Alignment/beaver-7b-v1.0-cost', torch_dtype=torch.bfloat16, device_map='auto')
tokenizer = AutoTokenizer.from_pretrained('PKU-Alignment/beaver-7b-v1.0-cost')

input = 'BEGINNING OF CONVERSATION: USER: hello ASSISTANT:Hello! How can I help you today?'

input_ids = tokenizer(input, return_tensors='pt')
output = model(**input_ids)
print(output)

# ScoreModelOutput(
#     scores=tensor([[[ -9.4375],
#          [ -2.5156],
#          [ -2.6562],
#          [ -2.3594],
#          [ -1.9375],
#          [ -2.5781],
#          [ -1.4766],
#          [ -1.9922],
#          [ -2.6562],
#          [ -3.8125],
#          [ -2.9844],
#          [ -4.1875],
#          [ -3.5938],
#          [ -4.6562],
#          [ -4.0000],
#          [ -3.3438],
#          [ -4.5625],
#          [ -4.8438],
#          [ -5.1875],
#          [ -8.0000],
#          [ -8.4375],
#          [-10.5000],
#          [-10.5000],
#          [ -8.8750],
#          [-10.1250],
#          [-10.2500],
#          [-11.5625],
#          [-10.7500]]], grad_fn=<ToCopyBackward0>),
#     end_scores=tensor([[-10.7500]], grad_fn=<ToCopyBackward0>),
#     last_hidden_state=tensor([[[ 2.2812, -0.4219, -0.2832,  ...,  0.2715,  0.4277,  1.1875],
#          [-0.3730, -0.2158,  1.2891,  ..., -1.3281,  0.6016,  0.7773],
#          [ 0.2285, -1.2422,  1.0625,  ..., -1.3438,  1.1875,  1.1016],
#          ...,
#          [-0.8828, -2.6250,  0.9180,  ..., -0.2773,  1.7500,  0.7695],
#          [ 2.0781, -4.1250, -0.1069,  ..., -0.8008,  0.4844,  0.4102],
#          [ 2.9688, -1.6250,  1.1250,  ...,  0.3223,  0.0439, -2.3281]]],
#        dtype=torch.bfloat16, grad_fn=<ToCopyBackward0>),
#     end_last_hidden_state=tensor([[ 2.9688, -1.6250,  1.1250,  ...,  0.3223,  0.0439, -2.3281]],
#        dtype=torch.bfloat16, grad_fn=<ToCopyBackward0>),
#     end_index=tensor([27])
# )
```

```


---

*Generated on 2025-06-21 15:07:54*
*Source: https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost*
