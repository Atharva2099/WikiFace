# google-bert/bert-base-uncased

## Model Information

- **Model ID**: google-bert/bert-base-uncased
- **Author**: google-bert
- **Last Updated**: 2024-02-19 11:06:12+00:00
- **Repository**: https://huggingface.co/google-bert/bert-base-uncased

## Tags

transformers, pytorch, tf, jax, rust, coreml, onnx, safetensors, bert, fill-mask, exbert, en, dataset:bookcorpus, dataset:wikipedia, arxiv:1810.04805, license:apache-2.0, autotrain_compatible, endpoints_compatible, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/.gitattributes](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/.gitattributes)
- **LICENSE** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/LICENSE](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/LICENSE)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/README.md](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/config.json](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/config.json)
- **coreml/fill-mask/float32_model.mlpackage/Data/com.apple.CoreML/model.mlmodel** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/coreml/fill-mask/float32_model.mlpackage/Data/com.apple.CoreML/model.mlmodel](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/coreml/fill-mask/float32_model.mlpackage/Data/com.apple.CoreML/model.mlmodel)
- **coreml/fill-mask/float32_model.mlpackage/Data/com.apple.CoreML/weights/weight.bin** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/coreml/fill-mask/float32_model.mlpackage/Data/com.apple.CoreML/weights/weight.bin](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/coreml/fill-mask/float32_model.mlpackage/Data/com.apple.CoreML/weights/weight.bin)
- **coreml/fill-mask/float32_model.mlpackage/Manifest.json** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/coreml/fill-mask/float32_model.mlpackage/Manifest.json](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/coreml/fill-mask/float32_model.mlpackage/Manifest.json)
- **flax_model.msgpack** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/flax_model.msgpack](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/flax_model.msgpack)
- **model.onnx** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/model.onnx](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/model.onnx)
- **model.safetensors** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/model.safetensors](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/model.safetensors)
- **pytorch_model.bin** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/pytorch_model.bin](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/pytorch_model.bin)
- **rust_model.ot** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/rust_model.ot](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/rust_model.ot)
- **tf_model.h5** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/tf_model.h5](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/tf_model.h5)
- **tokenizer.json** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/tokenizer.json](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/tokenizer.json)
- **tokenizer_config.json** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/tokenizer_config.json](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/tokenizer_config.json)
- **vocab.txt** (None bytes)
  - Download: [https://huggingface.co/google-bert/bert-base-uncased/resolve/main/vocab.txt](https://huggingface.co/google-bert/bert-base-uncased/resolve/main/vocab.txt)


## External Links

- [arxiv.org](https://arxiv.org/abs/1810.04805)
- [en.wikipedia.org](https://en.wikipedia.org/wiki/English_Wikipedia)
- [github.com](https://github.com/google-research/bert)
- [github.com](https://github.com/google-research/bert/blob/master/README.md)
- [huggingface.co](https://huggingface.co/bert-base-cased)
- [huggingface.co](https://huggingface.co/bert-base-chinese)
- [huggingface.co](https://huggingface.co/bert-base-multilingual-cased)
- [huggingface.co](https://huggingface.co/bert-base-uncased)
- [huggingface.co](https://huggingface.co/bert-large-cased)
- [huggingface.co](https://huggingface.co/bert-large-cased-whole-word-masking)
- [huggingface.co](https://huggingface.co/bert-large-uncased)
- [huggingface.co](https://huggingface.co/bert-large-uncased-whole-word-masking)
- [huggingface.co](https://huggingface.co/models?filter=bert)
- [yknzhu.wixsite.com](https://yknzhu.wixsite.com/mbweb)


## README.md

```markdown
---
language: en
tags:
- exbert
license: apache-2.0
datasets:
- bookcorpus
- wikipedia
---

# BERT base model (uncased)

Pretrained model on English language using a masked language modeling (MLM) objective. It was introduced in
[this paper](https://arxiv.org/abs/1810.04805) and first released in
[this repository](https://github.com/google-research/bert). This model is uncased: it does not make a difference
between english and English.

Disclaimer: The team releasing BERT did not write a model card for this model so this model card has been written by
the Hugging Face team.

## Model description

BERT is a transformers model pretrained on a large corpus of English data in a self-supervised fashion. This means it
was pretrained on the raw texts only, with no humans labeling them in any way (which is why it can use lots of
publicly available data) with an automatic process to generate inputs and labels from those texts. More precisely, it
was pretrained with two objectives:

- Masked language modeling (MLM): taking a sentence, the model randomly masks 15% of the words in the input then run
  the entire masked sentence through the model and has to predict the masked words. This is different from traditional
  recurrent neural networks (RNNs) that usually see the words one after the other, or from autoregressive models like
  GPT which internally masks the future tokens. It allows the model to learn a bidirectional representation of the
  sentence.
- Next sentence prediction (NSP): the models concatenates two masked sentences as inputs during pretraining. Sometimes
  they correspond to sentences that were next to each other in the original text, sometimes not. The model then has to
  predict if the two sentences were following each other or not.

This way, the model learns an inner representation of the English language that can then be used to extract features
useful for downstream tasks: if you have a dataset of labeled sentences, for instance, you can train a standard
classifier using the features produced by the BERT model as inputs.

## Model variations

BERT has originally been released in base and large variations, for cased and uncased input text. The uncased models also strips out an accent markers.  
Chinese and multilingual uncased and cased versions followed shortly after.  
Modified preprocessing with whole word masking has replaced subpiece masking in a following work, with the release of two models.  
Other 24 smaller models are released afterward.  

The detailed release history can be found on the [google-research/bert readme](https://github.com/google-research/bert/blob/master/README.md) on github.

| Model | #params | Language |
|------------------------|--------------------------------|-------|
| [`bert-base-uncased`](https://huggingface.co/bert-base-uncased) | 110M   | English |
| [`bert-large-uncased`](https://huggingface.co/bert-large-uncased)              | 340M    | English | sub 
| [`bert-base-cased`](https://huggingface.co/bert-base-cased)        | 110M    | English |
| [`bert-large-cased`](https://huggingface.co/bert-large-cased) | 340M    |  English |
| [`bert-base-chinese`](https://huggingface.co/bert-base-chinese) | 110M    | Chinese |
| [`bert-base-multilingual-cased`](https://huggingface.co/bert-base-multilingual-cased) | 110M | Multiple |
| [`bert-large-uncased-whole-word-masking`](https://huggingface.co/bert-large-uncased-whole-word-masking) | 340M | English |
| [`bert-large-cased-whole-word-masking`](https://huggingface.co/bert-large-cased-whole-word-masking) | 340M | English |

## Intended uses & limitations

You can use the raw model for either masked language modeling or next sentence prediction, but it's mostly intended to
be fine-tuned on a downstream task. See the [model hub](https://huggingface.co/models?filter=bert) to look for
fine-tuned versions of a task that interests you.

Note that this model is primarily aimed at being fine-tuned on tasks that use the whole sentence (potentially masked)
to make decisions, such as sequence classification, token classification or question answering. For tasks such as text
generation you should look at model like GPT2.

### How to use

You can use this model directly with a pipeline for masked language modeling:

```python
>>> from transformers import pipeline
>>> unmasker = pipeline('fill-mask', model='bert-base-uncased')
>>> unmasker("Hello I'm a [MASK] model.")

[{'sequence': "[CLS] hello i'm a fashion model. [SEP]",
  'score': 0.1073106899857521,
  'token': 4827,
  'token_str': 'fashion'},
 {'sequence': "[CLS] hello i'm a role model. [SEP]",
  'score': 0.08774490654468536,
  'token': 2535,
  'token_str': 'role'},
 {'sequence': "[CLS] hello i'm a new model. [SEP]",
  'score': 0.05338378623127937,
  'token': 2047,
  'token_str': 'new'},
 {'sequence': "[CLS] hello i'm a super model. [SEP]",
  'score': 0.04667217284440994,
  'token': 3565,
  'token_str': 'super'},
 {'sequence': "[CLS] hello i'm a fine model. [SEP]",
  'score': 0.027095865458250046,
  'token': 2986,
  'token_str': 'fine'}]
```

Here is how to use this model to get the features of a given text in PyTorch:

```python
from transformers import BertTokenizer, BertModel
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")
text = "Replace me by any text you'd like."
encoded_input = tokenizer(text, return_tensors='pt')
output = model(**encoded_input)
```

and in TensorFlow:

```python
from transformers import BertTokenizer, TFBertModel
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertModel.from_pretrained("bert-base-uncased")
text = "Replace me by any text you'd like."
encoded_input = tokenizer(text, return_tensors='tf')
output = model(encoded_input)
```

### Limitations and bias

Even if the training data used for this model could be characterized as fairly neutral, this model can have biased
predictions:

```python
>>> from transformers import pipeline
>>> unmasker = pipeline('fill-mask', model='bert-base-uncased')
>>> unmasker("The man worked as a [MASK].")

[{'sequence': '[CLS] the man worked as a carpenter. [SEP]',
  'score': 0.09747550636529922,
  'token': 10533,
  'token_str': 'carpenter'},
 {'sequence': '[CLS] the man worked as a waiter. [SEP]',
  'score': 0.0523831807076931,
  'token': 15610,
  'token_str': 'waiter'},
 {'sequence': '[CLS] the man worked as a barber. [SEP]',
  'score': 0.04962705448269844,
  'token': 13362,
  'token_str': 'barber'},
 {'sequence': '[CLS] the man worked as a mechanic. [SEP]',
  'score': 0.03788609802722931,
  'token': 15893,
  'token_str': 'mechanic'},
 {'sequence': '[CLS] the man worked as a salesman. [SEP]',
  'score': 0.037680890411138535,
  'token': 18968,
  'token_str': 'salesman'}]

>>> unmasker("The woman worked as a [MASK].")

[{'sequence': '[CLS] the woman worked as a nurse. [SEP]',
  'score': 0.21981462836265564,
  'token': 6821,
  'token_str': 'nurse'},
 {'sequence': '[CLS] the woman worked as a waitress. [SEP]',
  'score': 0.1597415804862976,
  'token': 13877,
  'token_str': 'waitress'},
 {'sequence': '[CLS] the woman worked as a maid. [SEP]',
  'score': 0.1154729500412941,
  'token': 10850,
  'token_str': 'maid'},
 {'sequence': '[CLS] the woman worked as a prostitute. [SEP]',
  'score': 0.037968918681144714,
  'token': 19215,
  'token_str': 'prostitute'},
 {'sequence': '[CLS] the woman worked as a cook. [SEP]',
  'score': 0.03042375110089779,
  'token': 5660,
  'token_str': 'cook'}]
```

This bias will also affect all fine-tuned versions of this model.

## Training data

The BERT model was pretrained on [BookCorpus](https://yknzhu.wixsite.com/mbweb), a dataset consisting of 11,038
unpublished books and [English Wikipedia](https://en.wikipedia.org/wiki/English_Wikipedia) (excluding lists, tables and
headers).

## Training procedure

### Preprocessing

The texts are lowercased and tokenized using WordPiece and a vocabulary size of 30,000. The inputs of the model are
then of the form:

```
[CLS] Sentence A [SEP] Sentence B [SEP]
```

With probability 0.5, sentence A and sentence B correspond to two consecutive sentences in the original corpus, and in
the other cases, it's another random sentence in the corpus. Note that what is considered a sentence here is a
consecutive span of text usually longer than a single sentence. The only constrain is that the result with the two
"sentences" has a combined length of less than 512 tokens.

The details of the masking procedure for each sentence are the following:
- 15% of the tokens are masked.
- In 80% of the cases, the masked tokens are replaced by `[MASK]`.
- In 10% of the cases, the masked tokens are replaced by a random token (different) from the one they replace.
- In the 10% remaining cases, the masked tokens are left as is.

### Pretraining

The model was trained on 4 cloud TPUs in Pod configuration (16 TPU chips total) for one million steps with a batch size
of 256. The sequence length was limited to 128 tokens for 90% of the steps and 512 for the remaining 10%. The optimizer
used is Adam with a learning rate of 1e-4, \\(\beta_{1} = 0.9\\) and \\(\beta_{2} = 0.999\\), a weight decay of 0.01,
learning rate warmup for 10,000 steps and linear decay of the learning rate after.

## Evaluation results

When fine-tuned on downstream tasks, this model achieves the following results:

Glue test results:

| Task | MNLI-(m/mm) | QQP  | QNLI | SST-2 | CoLA | STS-B | MRPC | RTE  | Average |
|:----:|:-----------:|:----:|:----:|:-----:|:----:|:-----:|:----:|:----:|:-------:|
|      | 84.6/83.4   | 71.2 | 90.5 | 93.5  | 52.1 | 85.8  | 88.9 | 66.4 | 79.6    |


### BibTeX entry and citation info

```bibtex
@article{DBLP:journals/corr/abs-1810-04805,
  author    = {Jacob Devlin and
               Ming{-}Wei Chang and
               Kenton Lee and
               Kristina Toutanova},
  title     = {{BERT:} Pre-training of Deep Bidirectional Transformers for Language
               Understanding},
  journal   = {CoRR},
  volume    = {abs/1810.04805},
  year      = {2018},
  url       = {http://arxiv.org/abs/1810.04805},
  archivePrefix = {arXiv},
  eprint    = {1810.04805},
  timestamp = {Tue, 30 Oct 2018 20:39:56 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1810-04805.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

<a href="https://huggingface.co/exbert/?model=bert-base-uncased">
	<img width="300px" src="https://cdn-media.huggingface.co/exbert/button.png">
</a>

```


---

*Generated on 2025-06-21 15:06:37*
*Source: https://huggingface.co/google-bert/bert-base-uncased*
