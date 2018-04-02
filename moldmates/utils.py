from collections import deque
import numpy as np


def consume(seq):
    deque(seq, maxlen=0)


def subseqs(seq, length):
    for i in range(len(seq) - length + 1):
        yield seq[i:i+length]


def ab2rtheta(a, b):
    min_x = (-b*a) / (1 + b**2)
    min_y = a * min_x + b
    r = (min_x** 2 + min_y**2)**.5
    if min_x == 0:
        theta = np.pi/2
    else:
        theta = np.arctan(min_y/min_x)
    return r, theta
