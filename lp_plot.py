#!  /usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np

fdatos = open('lp_2_3.txt', 'r')
x_datos = []                
y_datos = []               
lineas = fdatos.readlines() 
for linea in lineas:
    x, y = linea.split()     
    x_datos.append(float(x)) 
    y_datos.append(float(y)) 

fdatos.close()


plt.figure(figsize=(10,7))
plt.plot(x_datos,y_datos,'o',markersize=2)

plt.title('Coefficients LPC', fontsize=16, fontweight="bold")
plt.xlabel('Coefficients 2')
plt.ylabel('Coefficients 3')

plt.show()