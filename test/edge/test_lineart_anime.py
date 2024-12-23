import os.path

import pytest
from hbutils.testing import tmatrix

from imgutils.data import load_image
from imgutils.edge import edge_image_with_lineart_anime
from imgutils.edge.lineart_anime import _open_la_anime_model
from test.testings import get_testfile


@pytest.fixture()
def _release_model_after_run():
    try:
        yield
    finally:
        _open_la_anime_model.cache_clear()


@pytest.mark.unittest
class TestEdgeLineartAnime:
    @pytest.mark.parametrize(*tmatrix({
        'original_image': ['6125785.jpg', '6125901.jpg'],
        'backcolor': ['transparent', 'white'],
        'forecolor': ['', 'black']
    }))
    def test_edge_image_with_lineart_anime(self, original_image, backcolor, forecolor,
                                           image_diff, _release_model_after_run):
        image = edge_image_with_lineart_anime(
            get_testfile(original_image),
            backcolor=backcolor, forecolor=None if not forecolor else forecolor,
        )
        body, _ = os.path.splitext(original_image)

        assert image_diff(
            load_image(get_testfile(f'lineart_anime_{body}_{backcolor}_{forecolor}.png'),
                       mode='RGB', force_background='pink'),
            load_image(image, mode='RGB', force_background='pink'),
            throw_exception=False
        ) < 1e-2
