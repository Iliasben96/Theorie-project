from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from grid import Grid


class Plot:

    def __init__(self, grid):
        self.grid = grid


    def plot(self):

        gate_numbers = []
        gates_x = []
        gates_y = []
        gates_z = []

        grid = self.grid

        gate_list = grid.gate_list

        for gate in gate_list:
            gate_numbers.append(gate.nr)
            gates_x.append(gate.x)
            gates_y.append(gate.y)
            gates_z.append(0)
            

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
        for i,gate in enumerate(gate_numbers):
            x = gates_x[i]
            y = gates_y[i]
            z = gates_z[i]
            ax.scatter(x, y, z, c='r')
            ax.text(x, y, z + 0.2, gate, fontsize=9)    

        # Set limits an labels
        ax.set_xlim(0, grid.grid_max_x)
        ax.set_ylim(0, grid.grid_max_y)
        ax.set_zlim(0, 6)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        plt.xticks(np.arange(0, grid.grid_max_x, 1.0))
        plt.yticks(np.arange(0, grid.grid_max_y, 1.0))

        plt.show()