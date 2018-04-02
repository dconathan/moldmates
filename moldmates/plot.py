from typing import List
from moldmates.objects import Chainline, Image
from moldmates.utils import consume
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.axes import Axes
from itertools import cycle
from functools import partial

COLORS = cycle(cm.tab10.colors)


def plot_chainline(c: Chainline, ax: Axes, color=None):
    ax.plot(c.xs, c.ys, color=color or next(COLORS))


def plot_image(image: Image, ax: Axes, color=None):
    _plot_chainline = partial(plot_chainline, ax=ax, color=color or next(COLORS)) 
    consume(map(_plot_chainline, image.chainlines))
    return ax


def plot_images(images: List[Image], ax: Axes):
    _plot_image = partial(plot_image, ax=ax)
    consume(map(_plot_image, images))