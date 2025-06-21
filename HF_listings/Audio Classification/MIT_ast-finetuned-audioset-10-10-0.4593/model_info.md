# MIT/ast-finetuned-audioset-10-10-0.4593

## Model Information

- **Model ID**: MIT/ast-finetuned-audioset-10-10-0.4593
- **Author**: MIT
- **Last Updated**: 2023-09-06 14:49:15+00:00
- **Repository**: https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593

## Tags

transformers, pytorch, safetensors, audio-spectrogram-transformer, audio-classification, arxiv:2104.01778, license:bsd-3-clause, endpoints_compatible, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/.gitattributes](https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/.gitattributes)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/README.md](https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/config.json](https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/config.json)
- **model.safetensors** (None bytes)
  - Download: [https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/model.safetensors](https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/model.safetensors)
- **preprocessor_config.json** (None bytes)
  - Download: [https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/preprocessor_config.json](https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/preprocessor_config.json)
- **pytorch_model.bin** (None bytes)
  - Download: [https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/pytorch_model.bin](https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/resolve/main/pytorch_model.bin)


## External Links

- [arxiv.org](https://arxiv.org/abs/2104.01778)
- [github.com](https://github.com/YuanGongND/ast)
- [huggingface.co](https://huggingface.co/docs/transformers/main/en/model_doc/audio-spectrogram-transformer#transformers.ASTForAudioClassification.forward.example)
- [huggingface.co](https://huggingface.co/docs/transformers/model_doc/vit)


## README.md

```markdown
---
license: bsd-3-clause
tags:
- audio-classification
---

# Audio Spectrogram Transformer (fine-tuned on AudioSet) 

Audio Spectrogram Transformer (AST) model fine-tuned on AudioSet. It was introduced in the paper [AST: Audio Spectrogram Transformer](https://arxiv.org/abs/2104.01778) by Gong et al. and first released in [this repository](https://github.com/YuanGongND/ast). 

Disclaimer: The team releasing Audio Spectrogram Transformer did not write a model card for this model so this model card has been written by the Hugging Face team.

## Model description

The Audio Spectrogram Transformer is equivalent to [ViT](https://huggingface.co/docs/transformers/model_doc/vit), but applied on audio. Audio is first turned into an image (as a spectrogram), after which a Vision Transformer is applied. The model gets state-of-the-art results on several audio classification benchmarks.

## Usage

You can use the raw model for classifying audio into one of the AudioSet classes. See the [documentation](https://huggingface.co/docs/transformers/main/en/model_doc/audio-spectrogram-transformer#transformers.ASTForAudioClassification.forward.example) for more info.
```


---

*Generated on 2025-06-21 15:07:36*
*Source: https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593*
