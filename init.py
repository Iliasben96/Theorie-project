from netlist_reader import netlistreader
from grid import Grid
from gate import Gate
from plot import Plot


if __name__ == "__main__":

    start_grid = Grid()

    grid = start_grid.get_start_grid(1, 25)

    start_grid.print_grid()

    chip_plot = Plot(start_grid)

    chip_plot.plot()