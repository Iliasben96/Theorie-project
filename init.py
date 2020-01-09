from netlist_reader import netlistreader
from grid import Grid
from gate import Gate


if __name__ == "__main__":
    # print(netlistreader(1, 1))

    start_grid = Grid()

    grid = start_grid.get_start_grid(1, 25)

    # start_grid.put_wire(2, 1, 0)
    # start_grid.put_wire(1, 1, 0)

    # print(start_grid.get_gate_distance(1, 2))
    
    start_grid.print_grid()

    start_grid.fill_priority_queue()