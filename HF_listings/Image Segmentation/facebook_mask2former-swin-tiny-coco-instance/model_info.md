# facebook/mask2former-swin-tiny-coco-instance

## Model Information

- **Model ID**: facebook/mask2former-swin-tiny-coco-instance
- **Author**: facebook
- **Last Updated**: 2023-09-11 20:46:03+00:00
- **Repository**: https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance

## Tags

transformers, pytorch, safetensors, mask2former, vision, image-segmentation, dataset:coco, arxiv:2112.01527, arxiv:2107.06278, license:other, endpoints_compatible, region:us

## File Tree

- **.gitattributes** (None bytes)
  - Download: [https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/.gitattributes](https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/.gitattributes)
- **README.md** (None bytes)
  - Download: [https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/README.md](https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/README.md)
- **config.json** (None bytes)
  - Download: [https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/config.json](https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/config.json)
- **model.safetensors** (None bytes)
  - Download: [https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/model.safetensors](https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/model.safetensors)
- **preprocessor_config.json** (None bytes)
  - Download: [https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/preprocessor_config.json](https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/preprocessor_config.json)
- **pytorch_model.bin** (None bytes)
  - Download: [https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/pytorch_model.bin](https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance/resolve/main/pytorch_model.bin)


## External Links

- [arxiv.org](https://arxiv.org/abs/2107.06278)
- [arxiv.org](https://arxiv.org/abs/2112.01527)
- [github.com](https://github.com/facebookresearch/Mask2Former/)
- [huggingface.co](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/mask2former_architecture.png)
- [huggingface.co](https://huggingface.co/docs/transformers/master/en/model_doc/mask2former)
- [huggingface.co](https://huggingface.co/models?search=mask2former)


## README.md

```markdown
---
license: other
tags:
- vision
- image-segmentation
datasets:
- coco
widget:
- src: http://images.cocodataset.org/val2017/000000039769.jpg
  example_title: Cats
- src: http://images.cocodataset.org/val2017/000000039770.jpg
  example_title: Castle
---

# Mask2Former

Mask2Former model trained on COCO instance segmentation (tiny-sized version, Swin backbone). It was introduced in the paper [Masked-attention Mask Transformer for Universal Image Segmentation
](https://arxiv.org/abs/2112.01527) and first released in [this repository](https://github.com/facebookresearch/Mask2Former/). 

Disclaimer: The team releasing Mask2Former did not write a model card for this model so this model card has been written by the Hugging Face team.

## Model description

Mask2Former addresses instance, semantic and panoptic segmentation with the same paradigm: by predicting a set of masks and corresponding labels. Hence, all 3 tasks are treated as if they were instance segmentation. Mask2Former outperforms the previous SOTA, 
[MaskFormer](https://arxiv.org/abs/2107.06278) both in terms of performance an efficiency by (i) replacing the pixel decoder with a more advanced multi-scale deformable attention Transformer, (ii) adopting a Transformer decoder with masked attention to boost performance without
without introducing additional computation and (iii) improving training efficiency by calculating the loss on subsampled points instead of whole masks.

![model image](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/mask2former_architecture.png)

## Intended uses & limitations

You can use this particular checkpoint for instance segmentation. See the [model hub](https://huggingface.co/models?search=mask2former) to look for other
fine-tuned versions on a task that interests you.

### How to use

Here is how to use this model:

```python
import requests
import torch
from PIL import Image
from transformers import AutoImageProcessor, Mask2FormerForUniversalSegmentation


# load Mask2Former fine-tuned on COCO instance segmentation
processor = AutoImageProcessor.from_pretrained("facebook/mask2former-swin-tiny-coco-instance")
model = Mask2FormerForUniversalSegmentation.from_pretrained("facebook/mask2former-swin-tiny-coco-instance")

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)
inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

# model predicts class_queries_logits of shape `(batch_size, num_queries)`
# and masks_queries_logits of shape `(batch_size, num_queries, height, width)`
class_queries_logits = outputs.class_queries_logits
masks_queries_logits = outputs.masks_queries_logits

# you can pass them to processor for postprocessing
result = processor.post_process_instance_segmentation(outputs, target_sizes=[image.size[::-1]])[0]
# we refer to the demo notebooks for visualization (see "Resources" section in the Mask2Former docs)
predicted_instance_map = result["segmentation"]
```

For more code examples, we refer to the [documentation](https://huggingface.co/docs/transformers/master/en/model_doc/mask2former).
```


---

*Generated on 2025-06-21 15:07:08*
*Source: https://huggingface.co/facebook/mask2former-swin-tiny-coco-instance*
