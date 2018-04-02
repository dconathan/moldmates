import numpy as np
from dataclasses import dataclass, field, asdict
from typing import List
import json
from moldmates.utils import consume, ab2rtheta
from collections import UserList


@dataclass
class Chainline:
    xs: List[int] = None
    ys: List[int] = None
    r: float = None
    theta: float = None

    def process(self):
        a, b = np.polyfit(self.xs, self.ys, 1)
        self.r, self.theta = ab2rtheta(a, b)
        return self

    def dump(self):
        return asdict(self)

    def dumps(self):
        return json.dumps(self.dump())

    @classmethod
    def loads(cls, s):
        return cls.load(json.loads(s))

    @classmethod
    def load(cls, d):
        return cls(**d)


class ChainlineGroup(list):
    @property
    def rtheta(self):
        rs = np.array([c.r for c in self])
        thetas = np.array([c.theta for c in self])
        return np.vstack([rs, thetas]).T


@dataclass
class Image:
    chainlines: ChainlineGroup = None
    index: int = None
    filename: str = None

    def process(self):
        consume(map(lambda x: x.process(), self.chainlines))
        return self
        

@dataclass
class ImageSet:
    images: List[Image] = None
