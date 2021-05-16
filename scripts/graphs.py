import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np

plt.figure(1)
lpFile = open('lp_2_3.txt', 'r')
lp = np.loadtxt(lpFile, usecols = (0,2))
plt.plot(lp(0), lp(1))
plt.show()

plt.figure(2)
lpccFile = open('lpcc_2_3.txt', 'r')
lpcc = np.loadtxt(lpccFile, usecols = (0,2))
plt.plot(lpcc(0), lpcc(1))
plt.show()

plt.figure(3)
mfccFile = open('mfcc_2_3.txt', 'r')
mfcc = np.loadtxt(mfccFile, usecols = (0,2))
plt.plot(mfcc(0), mfcc(1))
plt.show()

plt.figure(3)
fig, axs = plt.subplots(3)
fig.suptitle('LP, LPCC and MFCC 2nd and 3rd coefficients')
axs[0].plot(lp(0), lp(1))
axs[0].set_title('LP')
axs[1].plot(lpcc(0), lpcc(1))
axs[1].set_title('LPCC')
axs[2].plot(mfcc(0), mfcc(1))
axs[2].set_title('MFCC')
plt.show()
