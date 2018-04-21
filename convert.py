from moldmates.utils import ab2rtheta, rtheta2xy
import numpy as np


r, theta = .5**.5, np.pi/4

x, y = rtheta2xy(r, theta)

print(x, y)
