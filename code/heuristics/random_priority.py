import random

def get_random_priority(gate_connections):

    connection_numbers = []

    # fills the list with connections
    for connection_nr in gate_connections.keys():
        connection_numbers.append(connection_nr)

    # randomizes the order of the list with connectios
    random.shuffle(connection_numbers)

    counter = 0
    for connection_nr in connection_numbers:

        # gives priority based on the order in the list
        connection = gate_connections[counter]
        connection.priority = connection_numbers[connection_nr]
        counter += 1
    
    return gate_connections