
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


fdata = open('lp_2_3.txt', 'r') 
data_x = []                
data_y = []                
rows = fdata.readlines() 
for row in rows:
    x, y = row.split()     
    data_x.append(float(x)) 
    data_y.append(float(y)) 

fdata.close()

plt.plot(data_x,data_y,'x')
plt.title('Coeficients LP')
plt.xlabel("Mostres")
plt.ylabel("Autocorrelació")
plt.grid(True)
plt.show()