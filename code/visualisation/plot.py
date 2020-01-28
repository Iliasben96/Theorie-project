from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Plot:
    """Visualisation of the connections between the gates, according to the gate list, on the grid"""

    def __init__(self, grid):
        self.grid = grid

    def plot(self):

        # Creation of lists with coordinates for the gates
        gate_numbers = []
        gates_x = []
        gates_y = []
        gates_z = []

        grid = self.grid

        gate_list = grid.gate_list
        
        # Adds the gates to the list of coordinates
        for gate in gate_list:
            gate_numbers.append(gate.nr)
            gates_x.append(gate.coordinates[0])
            gates_y.append(gate.coordinates[1])
            gates_z.append(gate.coordinates[2])

        # Create figure
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_title('Chipset')
        

        # Creation of lists with coordinates for the wires
        connections = grid.wired_connections

        for connection_dict in connections.values():
            connection_path = connection_dict["path"]

            # Creation of list of wire coordinates
            wire_x = []
            wire_y = []
            wire_z = []

            # Adds wire to the wire coordinates list
            for wire in connection_path:
                wire_x.append(wire[0])
                wire_y.append(wire[1])
                wire_z.append(wire[2])
            
                # Add wires
                ax.plot(xs=wire_x, ys=wire_y, zs=wire_z, c='r')

        # Add gates
        for i,gate in enumerate(gate_numbers):
            x = gates_x[i]
            y = gates_y[i]
            z = gates_z[i]
            ax.scatter(x, y, z, c='r')
            ax.text(x, y, z + 0.2, gate, fontsize=9)    

        # Padding to fix visual representation of grid
        padding = 1

        # Set limits an labels
        ax.set_xlim(0, grid.grid_max_x - padding)
        ax.set_ylim(0, grid.grid_max_y - padding)
        ax.set_zlim(0, 6)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        plt.xticks(np.arange(0, grid.grid_max_x, 1.0))
        plt.yticks(np.arange(0, grid.grid_max_y, 1.0))

        # Set colors for lines
        colormap = plt.cm.get_cmap('jet') #nipy_spectral, Set1,Paired   
        colors = [colormap(i) for i in np.linspace(0, 1,len(ax.lines))]
        for i,j in enumerate(ax.lines):
            j.set_color(colors[i])

        plt.show()