# google/t5-v1_1-xxl

## Model Information

- **Model ID**: google/t5-v1_1-xxl
- **Author**: google
- **Last Updated**: 2023-01-24 16:52:41+00:00
- **Repository**: https://huggingface.co/google/t5-v1_1-xxl

## Tags

transformers, pytorch, tf, t5, text2text-generation, en, dataset:c4, arxiv:2002.05202, arxiv:1910.10683, license:apache-2.0, autotrain_compatible, text-generation-inference, endpoints_compatible, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/google/t5-v1_1-xxl/resolve/main/.gitattributes](https://huggingface.co/google/t5-v1_1-xxl/resolve/main/.gitattributes)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/google/t5-v1_1-xxl/resolve/main/README.md](https://huggingface.co/google/t5-v1_1-xxl/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/google/t5-v1_1-xxl/resolve/main/config.json](https://huggingface.co/google/t5-v1_1-xxl/resolve/main/config.json)
- **generation_config.json** (None bytes)
  - Download: [https://huggingface.co/google/t5-v1_1-xxl/resolve/main/generation_config.json](https://huggingface.co/google/t5-v1_1-xxl/resolve/main/generation_config.json)
- **pytorch_model.bin** (None bytes)
  - Download: [https://huggingface.co/google/t5-v1_1-xxl/resolve/main/pytorch_model.bin](https://huggingface.co/google/t5-v1_1-xxl/resolve/main/pytorch_model.bin)
- **special_tokens_map.json** (None bytes)
  - Download: [https://huggingface.co/google/t5-v1_1-xxl/resolve/main/special_tokens_map.json](https://huggingface.co/google/t5-v1_1-xxl/resolve/main/special_tokens_map.json)
- **spiece.model** (None bytes)
  - Download: [https://huggingface.co/google/t5-v1_1-xxl/resolve/main/spiece.model](https://huggingface.co/google/t5-v1_1-xxl/resolve/main/spiece.model)
- **tf_model.h5** (None bytes)
  - Download: [https://huggingface.co/google/t5-v1_1-xxl/resolve/main/tf_model.h5](https://huggingface.co/google/t5-v1_1-xxl/resolve/main/tf_model.h5)
- **tokenizer_config.json** (None bytes)
  - Download: [https://huggingface.co/google/t5-v1_1-xxl/resolve/main/tokenizer_config.json](https://huggingface.co/google/t5-v1_1-xxl/resolve/main/tokenizer_config.json)


## External Links

- [ai.googleblog.com](https://ai.googleblog.com/2020/02/exploring-transfer-learning-with-t5.html)
- [arxiv.org](https://arxiv.org/abs/2002.05202)
- [arxiv.org](https://arxiv.org/pdf/1910.10683.pdf)
- [camo.githubusercontent.com](https://camo.githubusercontent.com/623b4dea0b653f2ad3f36c71ebfe749a677ac0a1/68747470733a2f2f6d69726f2e6d656469756d2e636f6d2f6d61782f343030362f312a44304a31674e51663876727255704b657944387750412e706e67)
- [github.com](https://github.com/google-research/text-to-text-transfer-transformer/blob/master/released_checkpoints.md#t511)
- [huggingface.co](https://huggingface.co/datasets/c4)
- [huggingface.co](https://huggingface.co/models?search=t5-v1_1)


## README.md

```markdown
---
language: en
datasets:
- c4

license: apache-2.0
---

[Google's T5](https://ai.googleblog.com/2020/02/exploring-transfer-learning-with-t5.html) Version 1.1


## Version 1.1

[T5 Version 1.1](https://github.com/google-research/text-to-text-transfer-transformer/blob/master/released_checkpoints.md#t511) includes the following improvements compared to the original T5 model- GEGLU activation in feed-forward hidden layer, rather than ReLU - see [here](https://arxiv.org/abs/2002.05202).

- Dropout was turned off in pre-training (quality win). Dropout should be re-enabled during fine-tuning.

- Pre-trained on C4 only without mixing in the downstream tasks.

- no parameter sharing between embedding and classifier layer

- "xl" and "xxl" replace "3B" and "11B". The model shapes are a bit different - larger `d_model` and smaller `num_heads` and `d_ff`.

**Note**: T5 Version 1.1 was only pre-trained on C4 excluding any supervised training. Therefore, this model has to be fine-tuned before it is useable on a downstream task.
Pretraining Dataset: [C4](https://huggingface.co/datasets/c4)

Other Community Checkpoints: [here](https://huggingface.co/models?search=t5-v1_1)

Paper: [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/pdf/1910.10683.pdf)

Authors: *Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, Peter J. Liu* 


## Abstract

Transfer learning, where a model is first pre-trained on a data-rich task before being fine-tuned on a downstream task, has emerged as a powerful technique in natural language processing (NLP). The effectiveness of transfer learning has given rise to a diversity of approaches, methodology, and practice. In this paper, we explore the landscape of transfer learning techniques for NLP by introducing a unified framework that converts every language problem into a text-to-text format. Our systematic study compares pre-training objectives, architectures, unlabeled datasets, transfer approaches, and other factors on dozens of language understanding tasks. By combining the insights from our exploration with scale and our new “Colossal Clean Crawled Corpus”, we achieve state-of-the-art results on many benchmarks covering summarization, question answering, text classification, and more. To facilitate future work on transfer learning for NLP, we release our dataset, pre-trained models, and code.

![model image](https://camo.githubusercontent.com/623b4dea0b653f2ad3f36c71ebfe749a677ac0a1/68747470733a2f2f6d69726f2e6d656469756d2e636f6d2f6d61782f343030362f312a44304a31674e51663876727255704b657944387750412e706e67)
 
```


---

*Generated on 2025-06-21 15:06:26*
*Source: https://huggingface.co/google/t5-v1_1-xxl*
