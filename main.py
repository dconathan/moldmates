from moldmates.constants import LINES, ZIP
from moldmates.load import load_image, load_zip, load_dir
from moldmates.objects import Image
import matplotlib.pyplot as plt
from moldmates.transform import Aligner
from moldmates.utils import xy2ab, xy2rtheta


aligner = Aligner()

images = load_dir(LINES)

ax = plt.gca()

image1: Image = images[0]
image2: Image = images[1]

image1.plot(ax, label='1')
Aligner().fit(image1).transform(image1).plot(ax, label='t1')
Aligner().fit(image1).transform(image2).plot(ax, label='t2')

plt.xlim([-1, 1])
plt.ylim([-1, 1])

plt.legend()

plt.show()


