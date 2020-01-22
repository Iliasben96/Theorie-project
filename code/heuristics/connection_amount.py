
def get_amount_of_connections_priority(netlist, gate_connections):

    connections_per_gate = get_connections_per_gate(netlist)
    for gate_nr,n_connections in connections_per_gate.items():

        priority = (6 - n_connections) / 2
        for connection_nr in gate_connections:
            connection = gate_connections[connection_nr]
            gate_a = connection.gate_a
            gate_b = connection.gate_b

            if gate_nr == gate_a.nr or gate_nr == gate_b.nr:
                connection.priority += priority

    return gate_connections
        
def get_connections_per_gate(netlist):

    gate_n_connections = {}


    # Calculate priority for each connection based on number of connections
    for connection in netlist:

        # Get gate numbers from netlist
        gate_a_nr = connection[0]
        gate_b_nr = connection[1]

        # Count number of connections per gate
        if gate_a_nr in gate_n_connections.keys():
            gate_n_connections[gate_a_nr] += 1
        else: 
            gate_n_connections[gate_a_nr] = 1
        if gate_b_nr in gate_n_connections.keys():
            gate_n_connections[gate_b_nr] += 1
        else:
            gate_n_connections[gate_b_nr] = 1

    # Sorting dictionary from: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    # Sort dictionary based on number of connections, highest first
    sorted_gate_n_connections = {k: v for k, v in sorted(gate_n_connections.items(), key=lambda item: item[1], reverse=True)}
    return sorted_gate_n_connections