from typing import List
from moldmates.objects import Chainline, Image, ChainlineGroup
from moldmates.utils import subseqs
from itertools import product
import numpy as np
from scipy.spatial import procrustes
from scipy.linalg import orthogonal_procrustes
from sklearn.preprocessing import StandardScaler


class Transformer:
    def __init__(self, reflect_r=False, reflect_theta=False):
        self.R = np.eye(2)
        if reflect_r:
            self.R[0, 0] = -1
        if reflect_theta:
            self.R[1, 1] = -1

    def fit(self, X, y):
        y = np.dot(y, self.R)
        self.T = X.mean(0) - y.mean(0)
        return self

    def transform(self, X) -> np.ndarray:
        return np.dot(X, self.R) + self.T

    def score(self, x, y):
        x_hat = self.fit(x, y).transform(y)
        return np.linalg.norm(x_hat - x, ord='fro')

    @classmethod
    def reflections(cls):
        return [cls(), cls(True), cls(False, True), cls(True, True)]


def score_transformation(rs1, rs2, thetas1, thetas2):
    return True


def score_candidate(c1: ChainlineGroup, c2: ChainlineGroup):
    for t in Transformer.reflections():
        score = t.score(c1.rtheta, c2.rtheta)
        print(score)


def compare_images(i1: Image, i2: Image, n_chainlines=3):
    i1_candidates = map(ChainlineGroup, subseqs(i1.chainlines, n_chainlines))
    i2_candidates = map(ChainlineGroup, subseqs(i2.chainlines, n_chainlines))
    candidates = product(i1_candidates, i2_candidates)
    for c1, c2 in candidates:
        score_candidate(c1, c2)
