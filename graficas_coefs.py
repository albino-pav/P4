import numpy as np
import matplotlib.pyplot as plt

arxiu = []
arxiu1='lp_2_3.txt'
arxiu2='lpcc_2_3.txt'
arxiu3='mfcc_2_3.txt'

lp_2 = np.loadtxt(arxiu1, skiprows=0, usecols=0)
lp_3 = np.loadtxt(arxiu1, skiprows=0, usecols=1)
lpcc_2 = np.loadtxt(arxiu2, skiprows=0, usecols=0)
lpcc_3 = np.loadtxt(arxiu2, skiprows=0, usecols=1)
mfcc_2 = np.loadtxt(arxiu3, skiprows=0, usecols=0)
mfcc_3 = np.loadtxt(arxiu3, skiprows=0, usecols=1)


plt.subplot(3,1,1)
plt.title('LP Parametrization')
plt.plot(lp_2,lp_3,'+', mew=0.5) #grueso
plt.xlabel('Coefficient 2')
plt.ylabel('Coefficient 3')
plt.grid(True)
plt.subplot(3,1,2)
plt.title('LPCC Parametrization')
plt.plot(lpcc_2,lpcc_3,'r+', mew=0.5)
plt.xlabel('Coefficient 2')
plt.ylabel('Coefficient 3')
plt.grid(True)
plt.subplot(3,1,3)
plt.title('MFCC Parametrization')
plt.plot(mfcc_2,mfcc_3,'g+', mew=0.5)
plt.xlabel('Coefficient 2')
plt.ylabel('Coefficient 3')
plt.grid(True)
plt.show()
