import re
import os

def load_raw(filename):
    out = []
    with open(filename) as f:
        for line in f:
            out = out + [parse_line(line)]
    return out


def parse_line(line):
    line = re.sub(r'\s*', '', line)
    parsed = re.match(r'{{(-?\d+),(-?\d+)},{(-?\d+),(-?\d+)}}', line)
    if parsed is None:
        raise Exception(f'line "{line}" could not be parsed')
    a, b, c, d = map(int, parsed.groups())
    return [[a, b], [c, d]]


def parse_raw(filename):
    parsed = load_raw(filename)
    obj = {'filename': os.path.split(filename)[-1],
           'chainlines': parsed}
    return obj