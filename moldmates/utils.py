from collections import deque
import numpy as np


def consume(seq):
    deque(seq, maxlen=0)


def subseqs(seq, length):
    for i in range(len(seq) - length + 1):
        yield seq[i:i+length]


def xy2rtheta(xs, ys):
    return ab2rtheta(*xy2ab(xs, ys))


def xy2ab(xs, ys):
    a, b = np.polyfit(xs, ys, 1)
    return a, b


def ab2rtheta(a, b):
    if b == 0:
        raise ValueError
    min_x = (-b*a) / (1 + a**2)
    min_y = a * min_x + b
    r = (min_x ** 2 + min_y ** 2)**.5
    if min_x == 0:
        theta = np.pi/2
    else:
        theta = np.arctan2(min_y, min_x) % (2*np.pi)
        if theta > np.pi:
            theta -= np.pi
            r = -r
    return r, theta


def rtheta2xy(r, theta):
    theta = theta % (2*np.pi)
    if theta > np.pi:
        theta -= np.pi
        r = -r
    x = r / np.cos(theta)
    y = r / np.cos(np.pi/2 - theta)
    return [x, 0], [0, y]
