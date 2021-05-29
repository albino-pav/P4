import matplotlib.pyplot as plt
import sys

if len( sys.argv ) < 2:
    print("Invalid Args!")
    sys.exit()

for feat in sys.argv[1:]:
    fdata = open(feat + '_2_3.txt', 'r')
    x_data = []                
    y_data = []               
    lines = fdata.readlines() 

    for line in lines:
        x, y = line.split()     
        x_data.append(float(x))
        y_data.append(float(y))

    fdata.close()
    plt.figure(figsize=(10,7))
    plt.title(feat.upper())
    plt.plot(x_data,y_data,'o',markersize=2)
    plt.savefig("./assets/" + feat + "-feature-plot.png")