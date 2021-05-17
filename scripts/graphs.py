import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np
import os

os.getcwd()
path = os.getcwd()

lpFile = open(path + '/lp_2_3.txt', 'r')
lpLines = lpFile.read().splitlines()
c2lp = []
c3lp = []
for x in lpLines:
    c2lp.append(x.split('\t')[0])
    c3lp.append(x.split('\t')[1])
lpFile.close()

lpccFile = open(path + '/lpcc_2_3.txt', 'r')
lpccLines = lpccFile.read().splitlines()
c2lpcc = []
c3lpcc = []
for x in lpccLines:
    c2lpcc.append(x.split('\t')[0])
    c3lpcc.append(x.split('\t')[1])
lpccFile.close()

mfccFile = open(path + '/mfcc_2_3.txt', 'r')
mfccLines = mfccFile.read().splitlines()
c2mfcc = []
c3mfcc = []
for x in mfccLines:
    c2mfcc.append(x.split('\t')[0])
    c3mfcc.append(x.split('\t')[1])
mfccFile.close()

plt.figure(1)
fig, axs = plt.subplots(3)
fig.suptitle('LP, LPCC and MFCC 2nd and 3rd coefficients')
axs[0].scatter(c2lp, c3lp, s = 1)
axs[0].set_title('LP')
axs[0].tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False, labelleft=False)  
axs[1].scatter(c2lpcc, c3lpcc, s = 1)
axs[1].set_title('LPCC')
axs[1].tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False, labelleft=False) 
axs[2].scatter(c2mfcc, c3mfcc, s = 1)
axs[2].set_title('MFCC')
axs[2].tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False, labelleft=False) 
plt.show()
