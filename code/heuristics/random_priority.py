import random

def get_random_priority(gate_connections):

    connection_numbers = []
    for connection_nr in gate_connections.keys():
        connection_numbers.append(connection_nr)
    random.shuffle(connection_numbers)

    counter = 0
    for connection_nr in connection_numbers:

        connection = gate_connections[counter]
        connection.priority = connection_numbers[connection_nr]
        counter += 1
    
    return gate_connections