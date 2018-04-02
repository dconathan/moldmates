import re
import os
from moldmates.objects import Image, Chainline, ChainlineGroup
import zipfile


def load_zip(filename):
    with zipfile.ZipFile(filename) as f:
        filenames = f.namelist()
        filenames = filter(lambda x: x.endswith('.txt'), filenames)
        filenames = filter(lambda x: not x.startswith('__MACOSX'), filenames)
        raise NotImplementedError



def load_image(filename):
    with open(filename) as f:
        chainlines = ChainlineGroup(list(map(parse_line, f)))
    return Image(filename=os.path.split(filename)[-1], chainlines=chainlines).process()



def parse_line(line):
    # clear whitespace
    line = re.sub(r'\s*', '', line)
    # coordinates pattern
    parsed = re.match(r'{{(-?\d+),(-?\d+)},{(-?\d+),(-?\d+)}}', line)
    if parsed is None:
        raise Exception(f'line "{line}" could not be parsed')
    x1, y1, x2, y2 = map(int, parsed.groups())
    return Chainline([x1, x2], [y1, y2])
