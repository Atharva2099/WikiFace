# sshleifer/distilbart-cnn-12-6

## Model Information

- **Model ID**: sshleifer/distilbart-cnn-12-6
- **Author**: sshleifer
- **Last Updated**: 2021-06-14 07:51:12+00:00
- **Repository**: https://huggingface.co/sshleifer/distilbart-cnn-12-6

## Tags

transformers, pytorch, jax, rust, bart, text2text-generation, summarization, en, dataset:cnn_dailymail, dataset:xsum, license:apache-2.0, autotrain_compatible, endpoints_compatible, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/.gitattributes](https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/.gitattributes)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/README.md](https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/config.json](https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/config.json)
- **flax_model.msgpack** (None bytes)
  - Download: [https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/flax_model.msgpack](https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/flax_model.msgpack)
- **merges.txt** (None bytes)
  - Download: [https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/merges.txt](https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/merges.txt)
- **pytorch_model.bin** (None bytes)
  - Download: [https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/pytorch_model.bin](https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/pytorch_model.bin)
- **rust_model.ot** (None bytes)
  - Download: [https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/rust_model.ot](https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/rust_model.ot)
- **tokenizer_config.json** (None bytes)
  - Download: [https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/tokenizer_config.json](https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/tokenizer_config.json)
- **vocab.json** (None bytes)
  - Download: [https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/vocab.json](https://huggingface.co/sshleifer/distilbart-cnn-12-6/resolve/main/vocab.json)


## External Links

- [huggingface.co](https://huggingface.co/transformers/model_doc/bart.html?#transformers.BartForConditionalGeneration)


## README.md

```markdown
---
language: en
tags:
- summarization
license: apache-2.0
datasets:
- cnn_dailymail
- xsum
thumbnail: https://huggingface.co/front/thumbnails/distilbart_medium.png
---

### Usage

This checkpoint should be loaded into `BartForConditionalGeneration.from_pretrained`. See the [BART docs](https://huggingface.co/transformers/model_doc/bart.html?#transformers.BartForConditionalGeneration) for more information.

### Metrics for DistilBART models

| Model Name                 |   MM Params |   Inference Time (MS) |   Speedup |   Rouge 2 |   Rouge-L |
|:---------------------------|------------:|----------------------:|----------:|----------:|----------:|
| distilbart-xsum-12-1       |         222 |                    90 |      2.54 |     18.31 |     33.37 |
| distilbart-xsum-6-6        |         230 |                   132 |      1.73 |     20.92 |     35.73 |
| distilbart-xsum-12-3       |         255 |                   106 |      2.16 |     21.37 |     36.39 |
| distilbart-xsum-9-6        |         268 |                   136 |      1.68 |     21.72 |     36.61 |
| bart-large-xsum (baseline) |         406 |                   229 |      1    |     21.85 |     36.50 |
| distilbart-xsum-12-6       |         306 |                   137 |      1.68 |     22.12 |     36.99 |
| bart-large-cnn (baseline)  |         406 |                   381 |      1    |     21.06 |     30.63 |
| distilbart-12-3-cnn        |         255 |                   214 |      1.78 |     20.57 |     30.00 |
| distilbart-12-6-cnn        |         306 |                   307 |      1.24 |     21.26 |     30.59 |
| distilbart-6-6-cnn         |         230 |                   182 |      2.09 |     20.17 |     29.70 |

```


---

*Generated on 2025-06-21 15:06:52*
*Source: https://huggingface.co/sshleifer/distilbart-cnn-12-6*
