# Chips & Circuits

## A programma that attempts to solve the Chips & Circuits problem

### The Chips & Circuits problem:

<p>In the Chips & Circuits problem, a number of gates need to be connected with eachother, with the lowest amount of wires possible. The wires that connect the gates, cannot use the positions of the gates and the wires cannot cross paths. Wires can also go up in the 3rd dimension to allow for more space to connect the wires.</p>
<p>The case provides at least 2 csv files, one file with x and y coordinates for gates that need to be place, and one netlist that provides the connections that need to be made between these </p>

### This programme

<p>This programme attempts to solve the Chips & Circuits problem in a multitude of ways. It uses an implementation of Astar to find the shortest paths for each connection in the netlist. This however, is not enough to solve the problem. Heuristics need to be applied to find a valid solution to the problem.</p>
