
from moldmates.load import parse_raw
from moldmates.process import process_image
from moldmates.constants import LINES
import pathlib

line_files = pathlib.Path(LINES).iterdir()

first = next(line_files)
first = next(line_files)

image = parse_raw(first)

process_image(image)



