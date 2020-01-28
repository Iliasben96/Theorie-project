from code.classes.netlist_reader import netlistreader
from code.classes.grid import Grid
from code.classes.gate import Gate
from code.visualisation.plot import Plot
from code.classes.chip_solver import ChipSolver
from code.algorithms.random_loop import start_random_solutions
from code.classes.table_creator import table_creator

"""
File that has functions to get relevant user inputs as integers
It retrieves the chip_nr, netlist_nr to choose what chip to use with what netlist
It retrieves the heuristics_nr and neighbor_locking_nr to decide which heuristics and neighborlocking options to use
"""

def get_user_chip_nr():

    chip_nr = input("Please choose the chip number: (1 or 2) ")

    while chip_nr.isdigit() == False:
        chip_nr = input("Error: please input either 1 or 2: ")

    chip_nr = int(chip_nr)
    while chip_nr < 0 or chip_nr > 2:
        chip_nr = input("Error please input either 1 or 2: ")

    return int(chip_nr)

def get_user_netlist_nr(chip_nr):

    netlist_nr = 0
    if chip_nr == 1:

        netlist_nr = input("Please choose netlist number (1, 2, or 3): ")

        while netlist_nr.isdigit() == False:
            netlist_nr = input("Error: please choose netlist number (1, 2, or 3): ")
        
        netlist_nr = int(netlist_nr)
        while netlist_nr < 0 or netlist_nr > 3:
            netlist_nr = input("Error: please choose netlist number (1, 2, or 3): ")

    if chip_nr == 2:
        netlist_nr = input("Please choose netlist number (4, 5, or 6): ")

        while netlist_nr.isdigit() == False:
            netlist_nr = input("Error: please choose netlist number (4, 5, or 6): ")
        
        netlist_nr = int(netlist_nr)
        while netlist_nr < 4 or netlist_nr > 6:
            netlist_nr = input("Error: please choose netlist number (4, 5, or 6): ")

    return netlist_nr

def get_user_heuristic_nr():

    heuristic_nr = input("What heuristics do you want to run? \n 1: none, 2:" + 
    "connection_length, 3: random, 4: amount of connections, 5: center grid: 6: random_iterations:" +
    " 7: level up: ")     

    while heuristic_nr.isdigit() == False:
        heuristic_nr = input("Error: please choose heuristic number (1 through 7): ")

    heuristic_nr = int(heuristic_nr)
    while heuristic_nr < 0 or heuristic_nr > 7:
        heuristic_nr = input("Error: please choose heuristic number (1 through 7): ")

    return heuristic_nr

def get_user_neighbor_lock_nr():

    neighbor_lock_input = input("What kind of neighbor locking would you like to enable? \n " + 
    "1: No locking 2: Lock everything before running 3: Lock dynamically during runtime (1, 2 or 3) ")

    while neighbor_lock_input.isdigit() == False:
        neighbor_lock_input = input("Error: please a valid option (1, 2, or 3): ")
        
    neighbor_lock_input = int(neighbor_lock_input)
    while neighbor_lock_input < 0 or neighbor_lock_input > 3:
        neighbor_lock_input = input("Error: please choose a valid option (1, 2, or 3): ")

    return neighbor_lock_input