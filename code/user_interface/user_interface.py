def get_user_chip_nr():
    """Fucntion to retrieves the chip_nr as a integer"""

    chip_nr = input("Please choose the chip number: (1 or 2) ")

    while chip_nr.isdigit() == False:
        chip_nr = input("Error: please input either 1 or 2: ")

    chip_nr = int(chip_nr)
    while chip_nr < 0 or chip_nr > 2:
        chip_nr = input("Error please input either 1 or 2: ")

    return int(chip_nr)

def get_user_netlist_nr(chip_nr):
    """Fucntion to retrieves the netlist_nr as a integer for the correct chip"""

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
    """Fucntion to retrieves the heuristic_nr as a integer, to decide what heuristic to use"""

    heuristic_nr = input("What heuristics do you want to run? \n 1: none, 2: " + 
    "connection_length, 3: random, 4: amount of connections, 5: center grid: ")     

    while heuristic_nr.isdigit() == False:
        heuristic_nr = input("Error: please choose heuristic number (1 through 5): ")

    heuristic_nr = int(heuristic_nr)
    while heuristic_nr < 0 or heuristic_nr > 5:
        heuristic_nr = input("Error: please choose heuristic number (1 through 5): ")

    return heuristic_nr

def get_user_neighbor_lock_nr():
    """Fucntion to retrieves the chip_neighbor_locker_nr as a integer, to decide what locking option to use"""

    neighbor_lock_input = input("What kind of neighbor locking would you like to enable? \n " + 
    "1: No locking 2: Lock everything before running 3: Lock during runtime (1, 2 or 3): ")

    while neighbor_lock_input.isdigit() == False:
        neighbor_lock_input = input("Error: please a valid option (1, 2, or 3): ")
        
    neighbor_lock_input = int(neighbor_lock_input)
    while neighbor_lock_input < 0 or neighbor_lock_input > 3:
        neighbor_lock_input = input("Error: please choose a valid option (1, 2, or 3): ")

    return neighbor_lock_input

def get_z_up():
    """Fucntion to retrieves the user choice if they want to use 
    Z-up Heuristic in combination with the already chosen heurstic
    """

    z_up_input = input("Would you like to increment Z of all connections every time a connections can't be laid? (yes/no) ")

    while z_up_input != "yes" and z_up_input != "no":
        print(z_up_input)
        z_up_input = input("Error: yes or no") 
    if z_up_input == "yes":
        z_up = True
    else:
        z_up = False

    return z_up