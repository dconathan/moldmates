import numpy as np
from typing import List, Iterable, Optional
import json
from moldmates.utils import xy2rtheta, rtheta2xy, xy2ab
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

    def flip_xy(self) -> 'Chainline':
        x = self.to_array()
        rot_angle = -np.pi/4
        rot_sin = np.sin(rot_angle)
        rot_cos = np.cos(rot_angle)
        rot = np.array([[rot_cos, -rot_sin], [rot_sin, rot_cos]])
        x = np.dot(x, rot)
        return Chainline.from_array(x)

    def plot(self, ax: Axes, color=None, **kwargs):
        a, b = xy2ab(self.xs, self.ys)
        xs = np.linspace(-1, 1)
        ys = list(map(lambda x: a*x + b, xs))
        ax.plot(xs, ys, color=color or next(COLORS), **kwargs)


class ChainlineGroup(list):
    @property
    def rtheta(self):
        return np.array([c.rtheta for c in self])

    def flipxy(self) -> 'ChainlineGroup':
        return ChainlineGroup((chainline.flip_xy() for chainline in self))

    def plot(self, ax: Axes, color=None, **kwargs):
        for chainline in self:
            chainline.plot(ax, color or next(COLORS), **kwargs)

    def trans_rtheta(self, r: float, theta: float) ->'ChainlineGroup':
        return ChainlineGroup((chainline.trans_rtheta(r, theta) for chainline in self))


i = 0


class Image:
    def __init__(self, chainlines: ChainlineGroup, filename: str, index: Optional[int]=None, flipxy: bool=False):
        self.chainlines = chainlines.flipxy() if flipxy else chainlines
        self.filename = filename
        self.index = self.new_index() if index is None else index

    def plot(self, ax: Axes, color=None, **kwargs):
        self.chainlines.plot(ax, color or next(COLORS), **kwargs)

    def trans_rtheta(self, r: float, theta: float) -> 'Image':
        chainlines = self.chainlines.trans_rtheta(r, theta)
        return Image(chainlines, self.filename, self.index)

    @property
    def rtheta(self):
        return self.chainlines.rtheta

    @staticmethod
    def new_index():
        global i
        i += 1
        return i - 1

    @property
    def n_chainlines(self):
        return len(self.chainlines)

    def center(self) -> 'Image':
        xs = []
        ys = []
        for chainline in self.chainlines:
            xs += chainline.xs
            ys += chainline.ys
        x_mean = np.mean(xs)
        y_mean = np.mean(ys)
        centered_chainlines = ChainlineGroup()
        for chainline in self.chainlines:
            xy = chainline.to_array()
            new_x = xy[:, 0] - x_mean
            new_y = xy[:, 1] - y_mean
            centered_chainline = Chainline(new_x.tolist(), new_y.tolist())
            centered_chainlines.append(centered_chainline)
        return Image(centered_chainlines, self.filename, self.index)
    
    def scale(self, x: float, y: float) -> 'Image':
        scaled_chainlines = ChainlineGroup()
        for chainline in self.chainlines:
            xy = chainline.to_array()
            new_x = xy[:, 0]/x
            new_y = xy[:, 1]/y
            scaled_chainline = Chainline(new_x.tolist(), new_y.tolist())
            scaled_chainlines.append(scaled_chainline)
        return Image(scaled_chainlines, self.filename, self.index)
 

class ImageSet(list):
    """
    Creates a set of images.

    Centers and scales the x, y pixel values

    To be mean centered with a max value of 1 and a min value of -1
    """
    def __init__(self, images: List[Image]):

        centered_images = []

        xs = []
        ys = []
        
        for image in images:
            centered_image = image.center()
            centered_images.append(centered_image)
            for chainline in centered_image.chainlines:
                xs += chainline.xs
                ys += chainline.ys

        x_scale = max(xs) - min(xs)
        y_scale = max(ys) - min(ys)

        super().__init__((image.scale(x_scale, y_scale) for image in centered_images))
