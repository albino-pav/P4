import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 170
plt.rcParams.update({'font.size': 9})

lp = np.loadtxt('lp_2_3.txt')
lpcc = np.loadtxt('lpcc_2_3.txt')
mfcc = np.loadtxt('mfcc_2_3.txt')
fig, axs = plt.subplots(3, ncols=2)
fig.suptitle("2nd and 3rd coefficients", y=1.02)

lp_2 = lp[:, 0]
lp_3 = lp[:, 1]

lpcc_2 = lpcc[:, 0]
lpcc_3 = lpcc[:, 1]

mfcc_2 = mfcc[:, 0]
mfcc_3 = mfcc[:, 1]

plt.tight_layout()

axs[0,0].plot(lp_2, label="Lp 2nd coefficient", color='blue', linewidth=0.5)
axs[1,0].plot(lpcc_2, label="Lpcc 2nd coefficient", color='red', linewidth=0.5)
axs[2,0].plot(mfcc_2, label="Mfcc 2nd coefficient",color='green', linewidth=0.5)

axs[0,1].plot(lp_3, label="Lp 3rd coefficient", color='blue', linewidth=0.5)
axs[1,1].plot(lpcc_3, label="Lpcc 3rd coefficient", color='red', linewidth=0.5)
axs[2,1].plot(mfcc_3, label="Mfcc 3rd coefficient",color='green', linewidth=0.5)
for i in range(2):
  for j in range(3):
    axs[j,i].set_ylabel("Value")
    axs[j,i].set_xlabel("Window #")
    axs[j,i].legend(loc='upper right', prop={'size': 6})

plt.show()