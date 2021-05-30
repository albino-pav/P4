import numpy as np
import matplotlib.pyplot as plt

p = 3

if p == 1:
    param = 'lp'
    color = 'blue'
elif p == 2:
    param = 'lpcc'
    color = 'green'
else:
    param = 'mfcc'
    color = 'red'

coefs = np.loadtxt(param + '_2_3.txt')

coef_2 = coefs[:, 0]
coef_3 = coefs[:, 1]

plt.title(param.upper())
plt.xlabel("2nd coefficient")
plt.ylabel("3rd coefficient")
plt.scatter(coef_2, coef_3, s=1, c=color)
plt.show()