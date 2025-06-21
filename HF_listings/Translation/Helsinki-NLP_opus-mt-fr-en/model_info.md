# Helsinki-NLP/opus-mt-fr-en

## Model Information

- **Model ID**: Helsinki-NLP/opus-mt-fr-en
- **Author**: Helsinki-NLP
- **Last Updated**: 2023-08-16 11:36:20+00:00
- **Repository**: https://huggingface.co/Helsinki-NLP/opus-mt-fr-en

## Tags

transformers, pytorch, tf, jax, marian, text2text-generation, translation, fr, en, license:apache-2.0, autotrain_compatible, endpoints_compatible, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/.gitattributes](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/.gitattributes)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/README.md](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/config.json](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/config.json)
- **flax_model.msgpack** (None bytes)
  - Download: [https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/flax_model.msgpack](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/flax_model.msgpack)
- **generation_config.json** (None bytes)
  - Download: [https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/generation_config.json](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/generation_config.json)
- **pytorch_model.bin** (None bytes)
  - Download: [https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/pytorch_model.bin](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/pytorch_model.bin)
- **source.spm** (None bytes)
  - Download: [https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/source.spm](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/source.spm)
- **target.spm** (None bytes)
  - Download: [https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/target.spm](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/target.spm)
- **tf_model.h5** (None bytes)
  - Download: [https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/tf_model.h5](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/tf_model.h5)
- **tokenizer_config.json** (None bytes)
  - Download: [https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/tokenizer_config.json](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/tokenizer_config.json)
- **vocab.json** (None bytes)
  - Download: [https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/vocab.json](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/resolve/main/vocab.json)


## External Links

- [github.com](https://github.com/Helsinki-NLP/OPUS-MT-train/blob/master/models/fr-en/README.md)
- [object.pouta.csc.fi](https://object.pouta.csc.fi/OPUS-MT-models/fr-en/opus-2020-02-26.eval.txt)
- [object.pouta.csc.fi](https://object.pouta.csc.fi/OPUS-MT-models/fr-en/opus-2020-02-26.test.txt)
- [object.pouta.csc.fi](https://object.pouta.csc.fi/OPUS-MT-models/fr-en/opus-2020-02-26.zip)


## README.md

```markdown
---
tags:
- translation
license: apache-2.0
---

### opus-mt-fr-en

* source languages: fr
* target languages: en
*  OPUS readme: [fr-en](https://github.com/Helsinki-NLP/OPUS-MT-train/blob/master/models/fr-en/README.md)

*  dataset: opus
* model: transformer-align
* pre-processing: normalization + SentencePiece
* download original weights: [opus-2020-02-26.zip](https://object.pouta.csc.fi/OPUS-MT-models/fr-en/opus-2020-02-26.zip)
* test set translations: [opus-2020-02-26.test.txt](https://object.pouta.csc.fi/OPUS-MT-models/fr-en/opus-2020-02-26.test.txt)
* test set scores: [opus-2020-02-26.eval.txt](https://object.pouta.csc.fi/OPUS-MT-models/fr-en/opus-2020-02-26.eval.txt)

## Benchmarks

| testset               | BLEU  | chr-F |
|-----------------------|-------|-------|
| newsdiscussdev2015-enfr.fr.en 	| 33.1 	| 0.580 |
| newsdiscusstest2015-enfr.fr.en 	| 38.7 	| 0.614 |
| newssyscomb2009.fr.en 	| 30.3 	| 0.569 |
| news-test2008.fr.en 	| 26.2 	| 0.542 |
| newstest2009.fr.en 	| 30.2 	| 0.570 |
| newstest2010.fr.en 	| 32.2 	| 0.590 |
| newstest2011.fr.en 	| 33.0 	| 0.597 |
| newstest2012.fr.en 	| 32.8 	| 0.591 |
| newstest2013.fr.en 	| 33.9 	| 0.591 |
| newstest2014-fren.fr.en 	| 37.8 	| 0.633 |
| Tatoeba.fr.en 	| 57.5 	| 0.720 |


```


---

*Generated on 2025-06-21 15:06:49*
*Source: https://huggingface.co/Helsinki-NLP/opus-mt-fr-en*
