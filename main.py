from moldmates.constants import LINES, ZIP
from moldmates.load import load_image, load_zip
from moldmates.plot import plot_images
from moldmates.compare import compare_images, score_candidate
from moldmates.utils import ab2rtheta
from moldmates.objects import ChainlineGroup
import matplotlib.pyplot as plt
import pathlib
import numpy as np

line_files = pathlib.Path(LINES).iterdir()

images = list(map(load_image, line_files))
c1 = ChainlineGroup(images[0].chainlines[:4])
c2 = ChainlineGroup(images[1].chainlines[:4])

score_candidate(c1, c2)

plt.figure()
ax = plt.gca()
plot_images(images[:3], ax)
plt.show()
