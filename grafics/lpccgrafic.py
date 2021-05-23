import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


fdata = open('lpcc_2_3.txt', 'r') 
data_x = []                
data_y = []               
rows = fdata.readlines() 
for row in rows:
    x, y = row.split()     
    data_x.append(float(x)) 
    data_y.append(float(y)) 

plt.plot(data_x,data_y,'x')
plt.title('Coeficients LPCC')
plt.xlabel("C2")
plt.ylabel("C3")
plt.grid(True)
plt.show()

fdata.close()