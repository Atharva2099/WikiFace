# microsoft/table-transformer-detection

## Model Information

- **Model ID**: microsoft/table-transformer-detection
- **Author**: microsoft
- **Last Updated**: 2023-09-06 14:49:09+00:00
- **Repository**: https://huggingface.co/microsoft/table-transformer-detection

## Tags

transformers, pytorch, safetensors, table-transformer, object-detection, arxiv:2110.00061, license:mit, endpoints_compatible, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-detection/resolve/main/.gitattributes](https://huggingface.co/microsoft/table-transformer-detection/resolve/main/.gitattributes)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-detection/resolve/main/README.md](https://huggingface.co/microsoft/table-transformer-detection/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-detection/resolve/main/config.json](https://huggingface.co/microsoft/table-transformer-detection/resolve/main/config.json)
- **model.safetensors** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-detection/resolve/main/model.safetensors](https://huggingface.co/microsoft/table-transformer-detection/resolve/main/model.safetensors)
- **preprocessor_config.json** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-detection/resolve/main/preprocessor_config.json](https://huggingface.co/microsoft/table-transformer-detection/resolve/main/preprocessor_config.json)
- **pytorch_model.bin** (None bytes)
  - Download: [https://huggingface.co/microsoft/table-transformer-detection/resolve/main/pytorch_model.bin](https://huggingface.co/microsoft/table-transformer-detection/resolve/main/pytorch_model.bin)


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
- src: https://www.invoicesimple.com/wp-content/uploads/2018/06/Sample-Invoice-printable.png
  example_title: Invoice
---

# Table Transformer (fine-tuned for Table Detection) 

Table Transformer (DETR) model trained on PubTables1M. It was introduced in the paper [PubTables-1M: Towards Comprehensive Table Extraction From Unstructured Documents](https://arxiv.org/abs/2110.00061) by Smock et al. and first released in [this repository](https://github.com/microsoft/table-transformer). 

Disclaimer: The team releasing Table Transformer did not write a model card for this model so this model card has been written by the Hugging Face team.

## Model description

The Table Transformer is equivalent to [DETR](https://huggingface.co/docs/transformers/model_doc/detr), a Transformer-based object detection model. Note that the authors decided to use the "normalize before" setting of DETR, which means that layernorm is applied before self- and cross-attention.

## Usage

You can use the raw model for detecting tables in documents. See the [documentation](https://huggingface.co/docs/transformers/main/en/model_doc/table-transformer) for more info.
```


---

*Generated on 2025-06-21 15:07:00*
*Source: https://huggingface.co/microsoft/table-transformer-detection*
