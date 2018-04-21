from typing import List
from moldmates.objects import Chainline, Image, ChainlineGroup
from moldmates.utils import subseqs, rtheta2xy
from itertools import product
import numpy as np
from scipy.spatial import procrustes
from scipy.linalg import orthogonal_procrustes
from sklearn.preprocessing import StandardScaler
from dataclasses import replace


class BestFit:
    def __init__(self):
        pass

    def fit(self, image: Image):
        self.image = image
        self.mean = image.chainlines.rtheta.mean(0)
        return self

    def transform(self, images: List[Image]):
        n_chainlines = max([i.n_chainlines for i in images])
        return images

    def fit_transform(self, images):
        self.fit(images[0])
        return self.transform(images)


class Reflector:
    def __init__(self, reflect_r: bool=False, reflect_theta: bool=False):
        self.R = np.eye(2)
        if reflect_r:
            self.R[0, 0] = -1
        if reflect_theta:
            self.R[1, 1] = -1

    def fit(self, *args, **kwargs) -> 'Reflector':
        return self

    def transform(self, image: Image) -> Image:
        return image.apply(self.transform_line)

    def transform_line(self, line: Chainline) -> Chainline:
        r, theta = np.dot(line.rtheta, self.R)
        xs, ys = rtheta2xy(r, theta)
        return replace(line, xs=xs, ys=ys)


def get_reflections(image: Image):
    reflectors = [Reflector(), Reflector(True), Reflector(False, True), Reflector(True, True)]
    reflections = [r.transform for r in reflectors]
    if isinstance(image, List):
        return list(map(get_reflections, image))
    return list(map(lambda r: r(image), reflections))


def score_pair(i1: Image, i2: Image, n_chainlines=3):
    i1_candidates = map(ChainlineGroup, subseqs(i1.chainlines, n_chainlines))
    i2_candidates = map(ChainlineGroup, subseqs(i2.chainlines, n_chainlines))
    candidates = product(i1_candidates, i2_candidates)
    scores = map(score_candidate, candidates)
    print(min(scores))


def score_candidate(c: List[ChainlineGroup]):
    return np.linalg.norm(c[0].rtheta_n - c[1].rtheta_n)

