from netlist_reader import netlistreader
from grid import Grid
from gate import Gate
from plot import Plot


if __name__ == "__main__":

    # Make new grid instance
    start_grid = Grid()

    # Generate start grid
    # TODO: Make this dynamic according to size of print
    grid = start_grid.get_start_grid(1, 25)

    # DEBUG: print grid
    start_grid.print_grid()

    # Create new plot
    chip_plot = Plot(start_grid)


    start_grid.put_wire(1, 5, 0)
    start_grid.put_wire(2, 5, 0)
    start_grid.put_wire(3, 5, 0)
    start_grid.put_wire(3, 6, 0)
    start_grid.put_wire(4, 6, 0)
    start_grid.put_wire(5, 6, 0)
    
    

    # Show new plot
    chip_plot.plot()