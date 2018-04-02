from moldmates.compare import Transformer
import numpy as np


def test_translation():
    # identity
    x = np.eye(2)
    y = x
    y_hat = Transformer().fit(x, y).transform(y)
    assert (y_hat == x).all()
    # translation
    y = x + 1
    y_hat = Transformer().fit(x, y).transform(y)
    assert (y_hat == x).all()
    y = x + np.random.randint(0, 10, size=2)
    print(y)
    y_hat = Transformer().fit(x, y).transform(y)
    assert (y_hat == x).all()


def test_reflection():
    # reflection
    x = np.eye(2)
    y = -x
    y_hat = Transformer(True, True).fit(x, y).transform(y)
    assert (y_hat == x).all()
    y[:, 1] = -y[:, 1]
    y_hat = Transformer(True, False).fit(x, y).transform(y)
    assert (y_hat == x).all()
    y = -y
    y_hat = Transformer(False, True).fit(x, y).transform(y)
    assert (y_hat == x).all()

def test_both():
    x = np.eye(2)
    y = -x + np.random.randint(0, 10, size=2)
    y_hat = Transformer(True, True).fit(x, y).transform(y)
    assert (y_hat == x).all()


