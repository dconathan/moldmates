import numpy as np


def process_image(obj: dict):
    chainlines: list = obj['chainlines']
    chainlines = map(lambda x: zip(*x), chainlines)
    for X, y in chainlines:
        m, b = np.polyfit(X, y, 1)
        print(m, b)
