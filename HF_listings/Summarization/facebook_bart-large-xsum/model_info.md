# facebook/bart-large-xsum

## Model Information

- **Model ID**: facebook/bart-large-xsum
- **Author**: facebook
- **Last Updated**: 2023-01-24 16:28:59+00:00
- **Repository**: https://huggingface.co/facebook/bart-large-xsum

## Tags

transformers, pytorch, tf, jax, rust, bart, text2text-generation, summarization, en, arxiv:1910.13461, license:mit, model-index, autotrain_compatible, endpoints_compatible, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/.gitattributes](https://huggingface.co/facebook/bart-large-xsum/resolve/main/.gitattributes)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/README.md](https://huggingface.co/facebook/bart-large-xsum/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/config.json](https://huggingface.co/facebook/bart-large-xsum/resolve/main/config.json)
- **flax_model.msgpack** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/flax_model.msgpack](https://huggingface.co/facebook/bart-large-xsum/resolve/main/flax_model.msgpack)
- **generation_config.json** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/generation_config.json](https://huggingface.co/facebook/bart-large-xsum/resolve/main/generation_config.json)
- **merges.txt** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/merges.txt](https://huggingface.co/facebook/bart-large-xsum/resolve/main/merges.txt)
- **pytorch_model.bin** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/pytorch_model.bin](https://huggingface.co/facebook/bart-large-xsum/resolve/main/pytorch_model.bin)
- **rust_model.ot** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/rust_model.ot](https://huggingface.co/facebook/bart-large-xsum/resolve/main/rust_model.ot)
- **tf_model.h5** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/tf_model.h5](https://huggingface.co/facebook/bart-large-xsum/resolve/main/tf_model.h5)
- **tokenizer.json** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/tokenizer.json](https://huggingface.co/facebook/bart-large-xsum/resolve/main/tokenizer.json)
- **tokenizer_config.json** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/tokenizer_config.json](https://huggingface.co/facebook/bart-large-xsum/resolve/main/tokenizer_config.json)
- **vocab.json** (None bytes)
  - Download: [https://huggingface.co/facebook/bart-large-xsum/resolve/main/vocab.json](https://huggingface.co/facebook/bart-large-xsum/resolve/main/vocab.json)


## README.md

```markdown
---
tags:
- summarization
language:
- en
license: mit
model-index:
- name: facebook/bart-large-xsum
  results:
  - task:
      type: summarization
      name: Summarization
    dataset:
      name: cnn_dailymail
      type: cnn_dailymail
      config: 3.0.0
      split: test
    metrics:
    - name: ROUGE-1
      type: rouge
      value: 25.2697
      verified: true
    - name: ROUGE-2
      type: rouge
      value: 7.6638
      verified: true
    - name: ROUGE-L
      type: rouge
      value: 17.1808
      verified: true
    - name: ROUGE-LSUM
      type: rouge
      value: 21.7933
      verified: true
    - name: loss
      type: loss
      value: 3.5042972564697266
      verified: true
    - name: gen_len
      type: gen_len
      value: 27.4462
      verified: true
  - task:
      type: summarization
      name: Summarization
    dataset:
      name: xsum
      type: xsum
      config: default
      split: test
    metrics:
    - name: ROUGE-1
      type: rouge
      value: 45.4525
      verified: true
    - name: ROUGE-2
      type: rouge
      value: 22.3455
      verified: true
    - name: ROUGE-L
      type: rouge
      value: 37.2302
      verified: true
    - name: ROUGE-LSUM
      type: rouge
      value: 37.2323
      verified: true
    - name: loss
      type: loss
      value: 2.3128726482391357
      verified: true
    - name: gen_len
      type: gen_len
      value: 25.5435
      verified: true
  - task:
      type: summarization
      name: Summarization
    dataset:
      name: samsum
      type: samsum
      config: samsum
      split: train
    metrics:
    - name: ROUGE-1
      type: rouge
      value: 24.7852
      verified: true
    - name: ROUGE-2
      type: rouge
      value: 5.2533
      verified: true
    - name: ROUGE-L
      type: rouge
      value: 18.6792
      verified: true
    - name: ROUGE-LSUM
      type: rouge
      value: 20.629
      verified: true
    - name: loss
      type: loss
      value: 3.746837854385376
      verified: true
    - name: gen_len
      type: gen_len
      value: 23.1206
      verified: true
  - task:
      type: summarization
      name: Summarization
    dataset:
      name: samsum
      type: samsum
      config: samsum
      split: test
    metrics:
    - name: ROUGE-1
      type: rouge
      value: 24.9158
      verified: true
    - name: ROUGE-2
      type: rouge
      value: 5.5837
      verified: true
    - name: ROUGE-L
      type: rouge
      value: 18.8935
      verified: true
    - name: ROUGE-LSUM
      type: rouge
      value: 20.76
      verified: true
    - name: loss
      type: loss
      value: 3.775235891342163
      verified: true
    - name: gen_len
      type: gen_len
      value: 23.0928
      verified: true
---
### Bart model finetuned on xsum

docs: https://huggingface.co/transformers/model_doc/bart.html

finetuning: examples/seq2seq/ (as of Aug 20, 2020)

Metrics: ROUGE > 22 on xsum.

variants: search for distilbart

paper: https://arxiv.org/abs/1910.13461
```


---

*Generated on 2025-06-21 15:06:54*
*Source: https://huggingface.co/facebook/bart-large-xsum*
