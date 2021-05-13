#!  /usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


fdata = open('lp_2_3.txt', 'r') #open file
data_x = []                #  first column
data_y = []                #  second column
rows = fdata.readlines() 
for row in rows:
    x, y = row.split()     # split in two elements
    data_x.append(float(x)) # add x to list data_x
    data_y.append(float(y)) # add y to list data_y

fdata.close()

plt.plot(data_x,data_y,'x')
plt.title('LP coefficients')
plt.show()