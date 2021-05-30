import numpy as np
import matplotlib.pyplot as plt

with open("lp_2_3.txt") as f:
    lines = f.readlines()
    x = [line.split()[0] for line in lines]
    y = [line.split()[1] for line in lines]

plt.plot(x)
plt.plot(y)


plt.show()