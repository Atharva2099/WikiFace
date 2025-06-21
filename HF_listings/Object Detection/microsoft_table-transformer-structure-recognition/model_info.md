# microsoft/table-transformer-structure-recognition

## Model Information

- **Model ID**: microsoft/table-transformer-structure-recognition
- **Author**: microsoft
- **Last Updated**: 2023-09-06 14:50:49+00:00
- **Repository**: https://huggingface.co/microsoft/table-transformer-structure-recognition

## Tags

transformers, pytorch, safetensors, table-transformer, object-detection, arxiv:2110.00061, license:mit, endpoints_compatible, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/.gitattributes](https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/.gitattributes)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/README.md](https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/config.json](https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/config.json)
- **model.safetensors** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/model.safetensors](https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/model.safetensors)
- **preprocessor_config.json** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/preprocessor_config.json](https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/preprocessor_config.json)
- **pytorch_model.bin** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/pytorch_model.bin](https://huggingface.co/microsoft/table-transformer-structure-recognition/resolve/main/pytorch_model.bin)


## External Links

- [arxiv.org](https://arxiv.org/abs/2110.00061)
- [github.com](https://github.com/microsoft/table-transformer)
- [huggingface.co](https://huggingface.co/docs/transformers/main/en/model_doc/table-transformer)
- [huggingface.co](https://huggingface.co/docs/transformers/model_doc/detr)


## README.md

```markdown
---
license: mit
widget:
- src: https://documentation.tricentis.com/tosca/1420/en/content/tbox/images/table.png
  example_title: Table
---

# Table Transformer (fine-tuned for Table Structure Recognition) 

Table Transformer (DETR) model trained on PubTables1M. It was introduced in the paper [PubTables-1M: Towards Comprehensive Table Extraction From Unstructured Documents](https://arxiv.org/abs/2110.00061) by Smock et al. and first released in [this repository](https://github.com/microsoft/table-transformer). 

Disclaimer: The team releasing Table Transformer did not write a model card for this model so this model card has been written by the Hugging Face team.

## Model description

The Table Transformer is equivalent to [DETR](https://huggingface.co/docs/transformers/model_doc/detr), a Transformer-based object detection model. Note that the authors decided to use the "normalize before" setting of DETR, which means that layernorm is applied before self- and cross-attention.

## Usage

You can use the raw model for detecting the structure (like rows, columns) in tables. See the [documentation](https://huggingface.co/docs/transformers/main/en/model_doc/table-transformer) for more info.
```


---

*Generated on 2025-06-21 15:07:02*
*Source: https://huggingface.co/microsoft/table-transformer-structure-recognition*
