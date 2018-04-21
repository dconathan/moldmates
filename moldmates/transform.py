import numpy as np
from typing import List
from moldmates.objects import Image, ChainlineGroup


class Aligner:
    def __init__(self):
        self.r_mean = 0
        self.t_mean = 0

    def fit(self, image: Image):
        self.r_mean, self.t_mean = Aligner.get_image_means(image)
        return self

    def transform(self, image: Image) -> Image:
        r_mean, t_mean = Aligner.get_image_means(image)
        new_chainlines = ChainlineGroup((chainline.trans_rtheta(r_mean, t_mean) for chainline in image.chainlines))
        return Image(new_chainlines, image.filename, image.index)

    def transform_many(self, images: List[Image]) -> List[Image]:
        return [self.transform(image) for image in images]

    @staticmethod
    def get_image_means(image):
        return np.mean(image.rtheta, axis=0)
