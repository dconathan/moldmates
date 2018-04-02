from moldmates.utils import ab2rtheta
import numpy as np


def test_ab2rtheta():
    assert ab2rtheta(-1, 1) == (.5**.5, np.pi / 4)