import re
import os
from moldmates.objects import Image, Chainline, ChainlineSet, ImageSet
from moldmates.utils import rotation_matrix
import zipfile
import pathlib
import numpy as np


def load_zip(filename):
    with zipfile.ZipFile(filename) as f:
        filenames = f.namelist()
        filenames = filter(lambda x: x.endswith('.txt'), filenames)
        filenames = filter(lambda x: not x.startswith('__MACOSX'), filenames)
        raise NotImplementedError


def load_dir(dirname) -> ImageSet:
    files = pathlib.Path(dirname).iterdir()
    images = list(map(load_image, files))
    return ImageSet(images)


def load_image(filename):
    with open(filename) as f:
        chainlines = ChainlineSet(list(map(parse_line, f)))
    return Image(filename=os.path.split(filename)[-1], chainlines=chainlines)


def parse_line(line, reorient=True):
    # clear whitespace
    line = re.sub(r'\s*', '', line)
    # coordinates pattern
    parsed = re.match(r'{{(-?\d+),(-?\d+)},{(-?\d+),(-?\d+)}}', line)
    if parsed is None:
        raise Exception(f'line "{line}" could not be parsed')
    x1, y1, x2, y2 = map(int, parsed.groups())
    if reorient:
        rot = rotation_matrix(-np.pi/4)
        xy = np.array([[x1, y1], [x2, y2]])
        xy = np.dot(xy, rot)
        x1, y1 = xy[0]
        x2, y2 = xy[1]
    return Chainline([x1, x2], [y1, y2])
