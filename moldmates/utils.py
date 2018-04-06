from collections import deque
import numpy as np
from scipy.special import cotdg

def consume(seq):
    deque(seq, maxlen=0)


def subseqs(seq, length):
    for i in range(len(seq) - length + 1):
        yield seq[i:i+length]

def xy2ab(xs, ys):
    a, b = np.polyfit(xs, ys, 1)
    return a, b

def ab2rtheta(a, b):
    if b == 0:
        raise ValueError
    min_x = (-b*a) / (1 + b**2)
    min_y = a * min_x + b
    r = (min_x** 2 + min_y**2)**.5
    if min_x == 0:
        theta = np.pi/2
    else:
        theta = np.arctan(min_y/min_x)
    return r, theta


def rtheta2xy(r, theta):
    x = r / np.cos(theta)
    y = r / np.sin(theta)
    return [x, 0], [0, y]


def rtheta2ab(r, theta):
    return xy2ab(*rtheta2xy(r, theta))

def xy2rtheta(xs, ys):
    return ab2rtheta(*xy2ab(xs, ys))

def ab2xy(a, b):
    return rtheta2xy(*ab2rtheta(a, b))

