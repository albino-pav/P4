import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import numpy as np


lp = np.loadtxt('lp_2_3.txt')
lpcc = np.loadtxt('lpcc_2_3.txt')
mfcc = np.loadtxt('mfcc_2_3.txt')

fig, (plot_lp,plot_lpcc,plot_mfcc) = plt.subplots(3)
fig.suptitle("Coefficients 2 & 3 of LP, LPCC y MFCC", fontsize=16, fontweight="bold")

plot_lp.plot(lp[:, 0], lp[:, 1],'.')
plot_lpcc.plot(lpcc[:, 0], lpcc[:, 1],'.')
plot_mfcc.plot(mfcc[:, 0], mfcc[:, 1],'.')

plot_lp.set_title('LP')
plot_lp.set(xlabel='Coefficients 2', ylabel='Coefficients 3')
plot_lpcc.set_title('LPCC')
plot_lpcc.set(xlabel='Coefficients 2', ylabel='Coefficients 3')
plot_mfcc.set_title('MFCC')
plot_mfcc.set(xlabel='Coefficients 2', ylabel='Coefficients 3')

plot_lp.grid()
plot_lpcc.grid()
plot_mfcc.grid()

plt.subplots_adjust(hspace=1)
plt.show()