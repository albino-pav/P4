import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

fdata = open('lp_2_3.txt', 'r')
x_data = []                
y_data = []               
lines = fdata.readlines() 
for line in lines:
    x, y = line.split()     
    x_data.append(float(x))
    y_data.append(float(y))

fdata.close()


plt.figure(figsize=(10,7))
plt.plot(x_data,y_data,'o',markersize=2)
plt.show()
plt.savefig("./assets/plot-feature.png")