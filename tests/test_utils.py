from moldmates.utils import rtheta2xy, xy2ab, xy2rtheta
import numpy as np


def test_xy2rtheta():
    x, y = [0, 1], [1, 0]
    r, t = xy2rtheta(x, y)
    np.testing.assert_almost_equal(r, .5**.5)
    np.testing.assert_almost_equal(t, np.pi/4)

    x, y = [0, 3**.5], [1, 0]
    r, t = xy2rtheta(x, y)
    np.testing.assert_almost_equal(r, 3**.5/2)
    np.testing.assert_almost_equal(t, np.pi/3)


def test_rtheta2xy():
    r, t = .5**.5, np.pi/4
    x, y = rtheta2xy(r, t)
    x1, x2 = x
    y1, y2 = y
    np.testing.assert_almost_equal(x1, 1)
    np.testing.assert_almost_equal(x2, 0)
    np.testing.assert_almost_equal(y1, 0)
    np.testing.assert_almost_equal(y2, 1)

    r, t = 3**.5/2, np.pi/3
    x, y = rtheta2xy(r, t)
    x1, x2 = x
    y1, y2 = y
    np.testing.assert_almost_equal(x1, 3**.5)
    np.testing.assert_almost_equal(x2, 0)
    np.testing.assert_almost_equal(y1, 0)
    np.testing.assert_almost_equal(y2, 1)


def test_xy2ab():
    x, y = [0, 1], [1, 0]
    a, b = xy2ab(x, y)
    np.testing.assert_almost_equal(a, -1)
    np.testing.assert_almost_equal(b, 1)
