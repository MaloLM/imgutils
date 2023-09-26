from imgutils.detect import detect_eyes
from imgutils.detect.eye import _LABELS
from imgutils.detect.visual import detection_visualize
from plot import image_plot


def _detect(img, **kwargs):
    return detection_visualize(img, detect_eyes(img, **kwargs), _LABELS)


if __name__ == '__main__':
    image_plot(
        (_detect('nian.png'), 'large scale'),
        (_detect('two_bikini_girls.png'), 'closed heads'),
        (_detect('genshin_post.jpg'), 'multiple'),
        (_detect('mostima_post.jpg'), 'anime style'),
        columns=2,
        figsize=(12, 9),
    )
