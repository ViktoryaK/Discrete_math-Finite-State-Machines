import random

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from celluloid import Camera

numpoints = 10
# points = np.random.random((2, numpoints))
# colors = cm.rainbow(np.linspace(0, 1, numpoints))
c = ['#5fb458', '#bb1212']
camera = Camera(plt.figure())
for i in range(25):
    for _ in range(100):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        # points += 0.1 * (np.random.random((2, numpoints)) - .5)
        plt.scatter(x, y, c=random.choice(c), s=10)
    camera.snap()
anim = camera.animate(blit=True)
anim.save('my.mp4')
# plt.show()