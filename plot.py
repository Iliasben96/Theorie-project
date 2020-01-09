from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

gate_numbers = [1,2,3,4]

def plot():
    # Create figure
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_title('Chipset')
    
    # Add coordinates
    x_1 = [1,2,3]
    y_1 = [3,3,3]
    z_1 = [0,0,0]

    x_2 = [2,3,4,4,4,4,5]
    y_2 = [1,1,1,2,3,4,4]
    z_2 = [0,0,0,0,0,0,0]
    
    # Add Lines
    ax.plot(xs=x_1, ys=y_1, zs=z_1, c='b')
    ax.plot(xs=x_2, ys=y_2, zs=z_2, c='y')

    # Add gates
    x_gates = [1,5,2,3]
    y_gates = [3,4,1,3]
    z_gates = [0,0,0,0]
    for i,gate in enumerate(gate_numbers):
        x = x_gates[i]
        y = y_gates[i]
        z = z_gates[i]
        ax.scatter(x, y, z, c='r')
        ax.text(x, y, z + 0.2, gate, fontsize=9)    

    # Set limits an labels
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.set_zlim(0, 6)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    plt.show()

plot()

