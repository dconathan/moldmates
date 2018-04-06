from moldmates.utils import ab2rtheta, ab2xy, rtheta2ab, rtheta2xy, xy2ab, xy2rtheta
import numpy as np


def test_ab2rtheta():
    assert ab2rtheta(-1, 1) == (.5**.5, np.pi / 4)
    assert np.allclose(ab2rtheta(*rtheta2ab(.33, .1)), (.33, .1))


def test_rtheta2ab():
    assert np.allclose(rtheta2ab(*ab2rtheta(-1, 1)), (-1, 1))
    assert np.allclose(rtheta2ab(1, np.pi/2), (0, 1))