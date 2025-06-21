# microsoft/table-transformer-structure-recognition-v1.1-all

## Model Information

- **Model ID**: microsoft/table-transformer-structure-recognition-v1.1-all
- **Author**: microsoft
- **Last Updated**: 2023-11-18 21:58:10+00:00
- **Repository**: https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all

## Tags

transformers, safetensors, table-transformer, object-detection, arxiv:2303.00716, license:mit, endpoints_compatible, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all/resolve/main/.gitattributes](https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all/resolve/main/.gitattributes)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all/resolve/main/README.md](https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all/resolve/main/config.json](https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all/resolve/main/config.json)
- **model.safetensors** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all/resolve/main/model.safetensors](https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all/resolve/main/model.safetensors)
- **preprocessor_config.json** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all/resolve/main/preprocessor_config.json](https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all/resolve/main/preprocessor_config.json)


## External Links

- [arxiv.org](https://arxiv.org/abs/2303.00716)
- [github.com](https://github.com/microsoft/table-transformer)
- [huggingface.co](https://huggingface.co/docs/transformers/main/en/model_doc/table-transformer)
- [huggingface.co](https://huggingface.co/docs/transformers/model_doc/detr)


## README.md

```markdown
---
license: mit
---

# Table Transformer (pre-trained for Table Structure Recognition) 

Table Transformer (TATR) model trained on PubTables1M and FinTabNet.c. It was introduced in the paper [Aligning benchmark datasets for table structure recognition](https://arxiv.org/abs/2303.00716) by Smock et al. and first released in [this repository](https://github.com/microsoft/table-transformer). 

Disclaimer: The team releasing Table Transformer did not write a model card for this model so this model card has been written by the Hugging Face team.

## Model description

The Table Transformer is equivalent to [DETR](https://huggingface.co/docs/transformers/model_doc/detr), a Transformer-based object detection model. Note that the authors decided to use the "normalize before" setting of DETR, which means that layernorm is applied before self- and cross-attention.

## Usage

You can use the raw model for detecting tables in documents. See the [documentation](https://huggingface.co/docs/transformers/main/en/model_doc/table-transformer) for more info.
```


---

*Generated on 2025-06-21 15:07:03*
*Source: https://huggingface.co/microsoft/table-transformer-structure-recognition-v1.1-all*
