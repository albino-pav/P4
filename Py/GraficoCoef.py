import numpy as np
import matplotlib.pyplot as plt
import os

ARCHIVOS_FOLDER = os.path.join(os.getcwd(), "Archivos")

plt.figure(figsize=(30, 18), dpi=80)
i = 311

for file in sorted(os.listdir(ARCHIVOS_FOLDER)):                                        
  if file.endswith(".txt"):
    plt.subplot(i)
    file_dir = os.path.join(ARCHIVOS_FOLDER, file)
    data = np.loadtxt(file_dir)
    plt.scatter(data[:,0], data[:,1], s=0.5, color = 'blue')
    plt.xlabel(file[:-8])
    plt.grid()
    i += 1

plt.savefig("grafica.png") 
plt.show()