import pytest

from imgutils.detect import detection_similarity
from imgutils.detect.head import detect_heads
from imgutils.generic.yolo import _open_models_for_repo_id
from test.testings import get_testfile


@pytest.fixture(scope='module', autouse=True)
def _release_model_after_run():
    try:
        yield
    finally:
        _open_models_for_repo_id.cache_clear()


@pytest.mark.unittest
class TestDetectHead:
    def test_detect_heads(self):
        detections = detect_heads(get_testfile('genshin_post.jpg'))
        assert len(detections) == 4

        values = []
        for bbox, label, score in detections:
            assert label == 'head'
            values.append((bbox, int(score * 1000) / 1000))

        assert values == pytest.approx([
            ((202, 156, 356, 293), 0.876),
            ((936, 86, 1134, 267), 0.834),
            ((650, 444, 720, 518), 0.778),
            ((461, 247, 536, 330), 0.434),
        ])

    def test_detect_heads_none(self):
        assert detect_heads(get_testfile('png_full.png')) == []

    def test_detect_heads_not_found(self):
        with pytest.raises(ValueError):
            _ = detect_heads(get_testfile('genshin_post.png'), model_name='not_found')

    @pytest.mark.parametrize(['model_name'], [
        ('head_detect_v1.6_n_yv10',),
    ])
    def test_detect_with_yolov10(self, model_name: str):
        detections = detect_heads(get_testfile('genshin_post.jpg'), model_name=model_name)
        similarity = detection_similarity(detections, [
            ((202, 156, 356, 293), 'head', 0.876),
            ((936, 86, 1134, 267), 'head', 0.834),
            ((650, 444, 720, 518), 'head', 0.778),
            ((461, 247, 536, 330), 'head', 0.434),
        ])
        assert similarity >= 0.85
