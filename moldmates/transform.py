import numpy as np
from typing import List, Iterable
from moldmates.objects import Image, ChainlineSet
from itertools import product


class ChainlinesTransformer:
    def transform(self, chainlines: ChainlineSet) -> ChainlineSet:
        raise NotImplementedError

    def transform_many(self, chainline_groups: Iterable[ChainlineSet]) -> List[ChainlineSet]:
        return [self.transform(chainlines) for chainlines in chainline_groups]


class ChainlinesPipeline(ChainlinesTransformer):
    def __init__(self, steps: List[ChainlinesTransformer]):
        self.steps = steps

    def transform(self, chainlines: ChainlineSet) -> ChainlineSet:
        for step in self.steps:
            chainlines = step.transform(chainlines)
        return chainlines

    def __repr__(self):
        return ' -> '.join(map(str, self.steps))


class Aligner(ChainlinesTransformer):
    def __init__(self):
        self.r_mean = 0
        self.t_mean = 0

    def fit(self, chainlines: ChainlineSet):
        self.r_mean, self.t_mean = Aligner.get_chainlines_means(chainlines)
        return self

    def transform(self, chainlines: ChainlineSet) -> ChainlineSet:
        r_mean, t_mean = Aligner.get_chainlines_means(chainlines)
        return ChainlineSet((chainline.trans_rtheta(self.r_mean - r_mean, self.t_mean - t_mean) for chainline in chainlines.chainlines))

    @staticmethod
    def get_chainlines_means(chainlines: ChainlineSet):
        return np.mean(chainlines.rtheta, axis=0)

    def __repr__(self):
        return f'(+{self.r_mean}, +{self.t_mean})'


class Reflector(ChainlinesTransformer):
    def __init__(self, reflect_r: bool=False, reflect_t: bool=False):
        self.reflect_r = reflect_r
        self.reflect_t = reflect_t

    def transform(self, chainlines: ChainlineSet) -> ChainlineSet:
        return chainlines.reflect_rtheta(self.reflect_r, self.reflect_t)

    @classmethod
    def reflections(cls) -> List['Reflector']:
        return [cls(r, t) for r, t in product([True, False], [True, False])]

    def __repr__(self):
        s = '('
        if self.reflect_r:
            s += 'flip r'
        elif self.reflect_t:
            if s != '(':
                s += ', '
            s += 'flip t'
        s += ')'
        return s


class BestAligner:
    def __init__(self, n_chainlines=3):
        self.base_subsets = None
        self.base_aligners = None
        self.pipeline = None
        self.n_chainlines = n_chainlines

    def fit(self, chainlines: ChainlineSet):
        self.base_subsets = chainlines.subsets(self.n_chainlines)
        self.base_aligners = [Aligner().fit(subset) for subset in self.base_subsets]
        return self

    def transform(self, chainlines: ChainlineSet) -> ChainlineSet:
        if self.base_subsets is None:
            raise AttributeError
        best_score = np.inf
        best_pipeline = None
        for subset in chainlines.subsets(self.n_chainlines):
            for reflector in Reflector.reflections():
                reflected_chainlines = reflector.transform(subset)
                for base_subset, base_aligner in zip(self.base_subsets, self.base_aligners):
                    aligned_chainlines = base_aligner.transform(reflected_chainlines)
                    score = l1_l1_score(base_subset, aligned_chainlines)
                    if score < best_score:
                        best_score = score
                        best_pipeline = ChainlinesPipeline([reflector, base_aligner])
        self.pipeline = best_pipeline
        return best_pipeline.transform(chainlines)


def l1_l1_score(c1: ChainlineSet, c2: ChainlineSet) -> float:
    return np.abs(c1.rtheta - c2.rtheta).sum()
