"""
Overview:
    Restore the images using `SCUNet <https://github.com/cszn/SCUNet>`_.

    .. image:: scunet_demo.plot.py.svg
        :align: center

    This is an overall benchmark of all the SCUNet models:

    .. image:: scunet_benchmark.plot.py.svg
        :align: center

    .. note::
        New in version v0.4.4, **images with alpha channel supported**.

        If you use an image with alpha channel (e.g. RGBA images),
        it will return a RGBA image, otherwise return RGG image.
"""
from functools import lru_cache
from typing import Literal

import numpy as np
from PIL import Image
from huggingface_hub import hf_hub_download

from .transparent import _rgba_preprocess, _rgba_postprocess
from ..data import ImageTyping, load_image
from ..utils import open_onnx_model, area_batch_run

SCUNetModelTyping = Literal['GAN', 'PSNR']


@lru_cache()
def _open_scunet_model(model: SCUNetModelTyping):
    """
    Open the SCUNet model for image restoration.

    :param model: The SCUNet model type ('GAN', 'PSNR').
    :type model: SCUNetModelTyping
    :return: The SCUNet ONNX model.
    """
    return open_onnx_model(hf_hub_download(
        f'deepghs/image_restoration',
        f'SCUNet-{model}.onnx'
    ))


def restore_with_scunet(image: ImageTyping, model: SCUNetModelTyping = 'GAN',
                        tile_size: int = 128, tile_overlap: int = 16, batch_size: int = 4,
                        silent: bool = False) -> Image.Image:
    """
    Restore an image using the SCUNet model.

    :param image: The input image.
    :type image: ImageTyping
    :param model: The SCUNet model type ('GAN', 'PSNR'). Default is 'GAN'.
    :type model: SCUNetModelTyping
    :param tile_size: The size of processing tiles. Default is 128.
    :type tile_size: int
    :param tile_overlap: The overlap between tiles. Default is 16.
    :type tile_overlap: int
    :param batch_size: The batch size of inference. Default is 4.
    :type batch_size: int
    :param silent: If True, the progress will not be displayed. Default is False.
    :type silent: bool
    :return: The restored image.
    :rtype: Image.Image
    """
    image, alpha_mask = _rgba_preprocess(image)
    image = load_image(image, mode='RGB', force_background='white')
    input_ = np.array(image).astype(np.float32) / 255.0
    input_ = input_.transpose((2, 0, 1))[None, ...]

    def _method(ix):
        ox, = _open_scunet_model(model).run(['output'], {'input': ix})
        return ox

    output_ = area_batch_run(
        input_, _method,
        tile_size=tile_size, tile_overlap=tile_overlap, batch_size=batch_size,
        silent=silent, process_title='SCUNet Restore',
    )
    output_ = np.clip(output_, a_min=0.0, a_max=1.0)
    ret_image = Image.fromarray((output_[0].transpose((1, 2, 0)) * 255).astype(np.int8), 'RGB')
    return _rgba_postprocess(ret_image, alpha_mask)
