import numpy as np
from typing import List, Iterable, Optional
import json
from moldmates.utils import xy2rtheta, rtheta2xy, xy2ab, rotation_matrix
from moldmates.plot import COLORS
from matplotlib.axes import Axes


class Chainline:
    def __init__(self, xs: Optional[Iterable[float]]=None, ys: Optional[Iterable[float]]=None,
                 r: Optional[float]=None, theta: Optional[float]=None):
        if xs is not None and ys is not None:
            self.xs = list(xs)
            self.ys = list(ys)
            self.r, self.theta = xy2rtheta(self.xs, self.ys)
        elif r is not None and theta is not None:
            self.r = r
            self.theta = theta
            self.xs, self.ys = rtheta2xy(r, theta)
        else:
            raise ValueError

    def trans_rtheta(self, r: float, theta: float) -> 'Chainline':
        theta = (self.theta + theta) % np.pi
        return Chainline(r=self.r + r, theta=theta)

    def reflect_rtheta(self, r: bool=False, t: bool=False) -> 'Chainline':
        r = -1 if r else 1
        t = -1 if t else 1
        return Chainline(r=self.r*r, theta=self.theta*t)

    def dump(self):
        return {'xs': self.xs, 'ys': self.ys}

    def dumps(self):
        return json.dumps(self.dump())

    @classmethod
    def from_array(cls, x: np.ndarray) -> 'Chainline':
        if len(x.shape) != 2 or x.shape[1] != 2:
            raise ValueError
        xs = x[:, 0]
        ys = x[:, 1]
        return cls(xs, ys)

    def to_array(self) -> np.ndarray:
        x = list(zip(self.xs, self.ys))
        return np.array(x)

    @classmethod
    def loads(cls, s):
        return cls.load(json.loads(s))

    @classmethod
    def load(cls, d):
        return cls(d['xs'], d['ys'])

    @property
    def rtheta(self):
        return np.array([self.r, self.theta])

    def plot(self, ax: Axes, color=None, **kwargs):
        a, b = xy2ab(self.xs, self.ys)
        xs = np.linspace(-1, 1)
        ys = list(map(lambda x: a*x + b, xs))
        xy = np.array(list(zip(xs, ys)))
        xy = np.dot(xy, rotation_matrix(np.pi/4))
        ax.plot(xy[:, 0], xy[:, 1], color=color or next(COLORS), **kwargs)


class ChainlineSet(Iterable[Chainline]):
    def __init__(self, chainlines: Iterable[Chainline]):
        self.chainlines = list(chainlines)

    @property
    def n_chainlines(self):
        return len(self.chainlines)

    @property
    def rtheta(self):
        return np.array([c.rtheta for c in self.chainlines])

    def plot(self, ax: Axes, color=None, **kwargs):
        color = color or next(COLORS)
        for chainline in self.chainlines:
            chainline.plot(ax, color, **kwargs)

    def trans_rtheta(self, r: float, theta: float) -> 'ChainlineSet':
        return ChainlineSet((chainline.trans_rtheta(r, theta) for chainline in self.chainlines))

    def reflect_rtheta(self, r: bool=False, t: bool=False) -> 'ChainlineSet':
        return ChainlineSet((chainline.reflect_rtheta(r, t) for chainline in self.chainlines))

    def __iter__(self):
        return iter(self.chainlines)

    def __len__(self):
        return len(self.chainlines)

    def subsets(self, length: int) -> Iterable['ChainlineSet']:
        if length > self.n_chainlines:
            raise ValueError
        subsets = []
        for i in range(self.n_chainlines - length + 1):
            subsets.append(ChainlineSet(self.chainlines[i:i+length]))
        return subsets


global_index = 0


class Image(ChainlineSet):
    def __init__(self, chainlines: Iterable[Chainline], filename: str, index: Optional[int]=None):
        super().__init__(chainlines)
        self.filename = filename
        self.index = self.new_index() if index is None else index

    def trans_rtheta(self, r: float, theta: float) -> 'Image':
        chainlines = ChainlineSet(self.chainlines).trans_rtheta(r, theta)
        return Image(chainlines, self.filename, self.index)

    def reflect_rtheta(self, r: bool=False, t: bool=False) -> 'Image':
        chainlines = ChainlineSet(self.chainlines).reflect_rtheta(r, t)
        return Image(chainlines, self.filename, self.index)

    @staticmethod
    def new_index():
        global global_index
        global_index += 1
        return global_index - 1

    def center(self) -> 'Image':
        xs = []
        ys = []
        for chainline in self.chainlines:
            xs += chainline.xs
            ys += chainline.ys
        x_mean = np.mean(xs)
        y_mean = np.mean(ys)
        centered_chainlines = list()
        for chainline in self.chainlines:
            xy = chainline.to_array()
            new_x = xy[:, 0] - x_mean
            new_y = xy[:, 1] - y_mean
            centered_chainline = Chainline(new_x.tolist(), new_y.tolist())
            centered_chainlines.append(centered_chainline)
        return Image(centered_chainlines, self.filename, self.index)
    
    def scale(self, x: float, y: float) -> 'Image':
        scaled_chainlines = list()
        for chainline in self.chainlines:
            xy = chainline.to_array()
            new_x = xy[:, 0]/x
            new_y = xy[:, 1]/y
            scaled_chainline = Chainline(new_x.tolist(), new_y.tolist())
            scaled_chainlines.append(scaled_chainline)
        return Image(scaled_chainlines, self.filename, self.index)
 

class ImageSet(Iterable[Image]):
    """
    Creates a set of images.

    Centers and scales the x, y pixel values

    To be mean centered with a max value of 1 and a min value of -1
    """
    def __init__(self, images: List[Image]):

        centered_images = []

        pixels = []

        for image in images:
            centered_image = image.center()
            centered_images.append(centered_image)
            for chainline in centered_image.chainlines:
                pixels += chainline.xs
                pixels += chainline.ys

        scale = max(pixels) - min(pixels)

        self.images = [image.scale(scale, scale) for image in centered_images]

    def __iter__(self):
        return iter(self.images)
