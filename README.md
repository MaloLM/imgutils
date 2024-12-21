# imgutils

[![GitHub license](https://img.shields.io/github/license/deepghs/imgutils)](https://github.com/deepghs/imgutils/blob/master/LICENSE)

A convenient and user-friendly anime-style image data processing library that integrates various advanced anime-style
image processing models.

## Installation

You can simply install it with `pip` command line from the official PyPI site.

```shell
pip install -e .
```

<!-- If your operating environment includes a available GPU, you can use the following installation command to achieve higher
performance:

```shell
pip install dghs-imgutils[gpu]
``` -->

For more information about installation, you can refer
to [Installation](https://deepghs.github.io/imgutils/main/tutorials/installation/index.html).

## Supported or Developing Features

* [Tachie(差分) Detection and Clustering](https://github.com/deepghs/imgutils#tachie%E5%B7%AE%E5%88%86-detection-and-clustering)
* [Contrastive Character Image Pretraining](https://github.com/deepghs/imgutils#contrastive-character-image-pretraining)
* [Object Detection](https://github.com/deepghs/imgutils#object-detection)
* [Edge Detection / Lineart Generation](https://github.com/deepghs/imgutils#edge-detection--lineart-generation)
* [Monochrome Image Detection](https://github.com/deepghs/imgutils#monochrome-image-detection)
* [Truncated Image Check](https://github.com/deepghs/imgutils#truncated-image-check)
* [Image Tagging](https://github.com/deepghs/imgutils#image-tagging)
* [Character Extraction](https://github.com/deepghs/imgutils#character-extraction)

`imgutils` also includes many other features besides that. For detailed descriptions and examples, please refer to
the [official documentation](https://deepghs.github.io/imgutils/main/index.html). Here, we won't go into each of them
individually.

### Contrastive Character Image Pretraining

We can use `imgutils` to extract features from anime character images (containing only a single character), calculate
the visual dissimilarity between two characters, and determine whether two images depict the same character. We can also
perform clustering operations based on this metric, as shown below

<!-- ![ccip](https://github.com/deepghs/imgutils/blob/gh-pages/main/_images/ccip_full.plot.py.svg) -->

```python
from imgutils.metrics import ccip_difference, ccip_clustering

# same character
print(ccip_difference('ccip/1.jpg', 'ccip/2.jpg'))  # 0.16583099961280823

# different characters
print(ccip_difference('ccip/1.jpg', 'ccip/6.jpg'))  # 0.42947039008140564
print(ccip_difference('ccip/1.jpg', 'ccip/7.jpg'))  # 0.4037521779537201
print(ccip_difference('ccip/2.jpg', 'ccip/6.jpg'))  # 0.4371533691883087
print(ccip_difference('ccip/2.jpg', 'ccip/7.jpg'))  # 0.40748104453086853
print(ccip_difference('ccip/6.jpg', 'ccip/7.jpg'))  # 0.392294704914093

images = [f'ccip/{i}.jpg' for i in range(1, 13)]
print(images)
# ['ccip/1.jpg', 'ccip/2.jpg', 'ccip/3.jpg', 'ccip/4.jpg', 'ccip/5.jpg', 'ccip/6.jpg', 'ccip/7.jpg', 'ccip/8.jpg', 'ccip/9.jpg', 'ccip/10.jpg', 'ccip/11.jpg', 'ccip/12.jpg']
print(ccip_clustering(images, min_samples=2))  # few images, min_sample should not be too large
# [0, 0, 0, 3, 3, 3, 1, 1, 1, 1, 2, 2]
```

For more usage, please refer
to [official documentation of CCIP](https://deepghs.github.io/imgutils/main/api_doc/metrics/ccip.html).

### Object Detection

Currently, object detection is supported for anime heads and person, as shown below

* Face Detection

<!-- ![face detection](https://github.com/deepghs/imgutils/blob/gh-pages/main/_images/face_detect_demo.plot.py.svg) -->

* Head Detection

<!-- ![head detection](https://github.com/deepghs/imgutils/blob/gh-pages/main/_images/head_detect_demo.plot.py.svg) -->

* Person Detection

<!-- ![person detection](https://github.com/deepghs/imgutils/blob/gh-pages/main/_images/person_detect_demo.plot.py.svg) -->

Based on practical tests, head detection currently has a very stable performance and can be used for automation tasks.
However, person detection is still being further iterated and will focus on enhancing detection capabilities for
artistic illustrations in the future.

### Edge Detection / Lineart Generation

Anime images can be converted to line drawings using the model provided
by [patrickvonplaten/controlnet_aux](https://github.com/patrickvonplaten/controlnet_aux), as shown below.

<!-- ![edge example](https://github.com/deepghs/imgutils/blob/gh-pages/main/_images/edge_demo.plot.py.svg) -->

It is worth noting that the `lineart` model may consume more computational resources, while `canny` is the fastest but
has average effect. Therefore, `lineart_anime` may be the most balanced choice in most cases.

### Truncated Image Check

The following code can be used to detect incomplete image files (such as images interrupted during the download
process):

```python
from imgutils.validate import is_truncated_file

if __name__ == '__main__':
    filename = 'test_jpg.jpg'
    if is_truncated_file(filename):
        print('This image is truncated, you\'d better '
              'remove this shit from your dataset.')
    else:
        print('This image is okay!')

```

### Character Extraction

When we need to extract the character parts from anime images, we can use
the [`segment-rgba-with-isnetis`](https://deepghs.github.io/imgutils/main/api_doc/segment/isnetis.html#segment-rgba-with-isnetis)
function for extraction and obtain an RGBA format image (with the background part being transparent), just like the
example shown below.

<!-- ![isnetis](https://deepghs.github.io/imgutils/main/_images/isnetis_trans.plot.py.svg) -->

```python
from imgutils.segment import segment_rgba_with_isnetis

mask_, image_ = segment_rgba_with_isnetis('hutao.png')
image_.save('hutao_seg.png')

mask_, image_ = segment_rgba_with_isnetis('skadi.jpg')
image_.save('skadi_seg.png')
```

This model can be found at https://huggingface.co/skytnt/anime-seg .
