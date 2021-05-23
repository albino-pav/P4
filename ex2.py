import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import numpy as np


lp = np.loadtxt('lp_2_3.txt')
lpcc = np.loadtxt('lpcc_2_3.txt')
mfcc = np.loadtxt('mfcc_2_3.txt')

fig, (axlp,axlpcc,axmfcc) = plt.subplots(3)
fig.suptitle("Coeficientes 2 y 3 usando LP, LPCC y MFCC de las senales de un locutor")
axlp.plot(lp[:, 0], lp[:, 1],'.')
axlpcc.plot(lpcc[:, 0], lpcc[:, 1],'.')
axmfcc.plot(mfcc[:, 0], mfcc[:, 1],'.')
axlp.set_title('LP')
axlp.set(xlabel='Coeficiente 2', ylabel='Coeficiente 3')
axlpcc.set_title('LPCC')
axlpcc.set(xlabel='Coeficiente 2', ylabel='Coeficiente 3')
axmfcc.set_title('MFCC')
axmfcc.set(xlabel='Coeficiente 2', ylabel='Coeficiente 3')
axlp.grid()
axlpcc.grid()
axmfcc.grid()
plt.show()
