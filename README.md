# Chips & Circuits
<p>In the Chips & Circuits problem, a number of gates need to be connected with eachother, with the lowest amount of wires possible. The wires that connect the gates, cannot use the positions of the gates and the wires cannot cross paths. Wires can also go up in the 3rd dimension to allow for more space to connect the wires.</p>

<p>The case provides at least 2 csv files, one file with x and y coordinates for gates that need to be place, and one netlist that provides the connections that need to be made between these </p>

## This programme

<p>This programme attempts to solve the Chips & Circuits problem in a multitude of ways. It uses an implementation of Astar to find the shortest paths for each connection in the netlist. This however, is not enough to solve the problem. Heuristics need to be applied to find a valid solution to the problem.</p>

## Getting setup
### Requirements
<p> This code was completly writen in Python 3.8. In requirement.txt are all packages required to run this code. Use pip to install the packages:</p>
<pre>
    <code>pip install -r requirements.txt</code>
</pre>

### Usage: 
<p>The program can be run by running:</p>
<pre>
    <code>python main.py</code>
</pre>
<p>After running main the user is prompted for several option which will all determine the outcome of the code.</p>

### Structure:
<p> Here are all the important maps and files in the project</p>
<ul>
    <li><strong>/code</strong>
        ": Contains all code of the project"
    </li>
    <ul>
        <li><strong>/code/algorithms</strong>
            ": contains all algortihms"
        </li>
        <li><strong>/code/classes</strong>
            ": contains all classes and helper functions"
        </li>
        <li><strong>/code/heuristics</strong>
            ": contains all heuristics"
        </li>
        <li><strong>/code/user_interface</strong>
            ": contains all files for user interface"
        </li>
        <li><strong>/code/visualisation</strong>
            ": contains all code required for the visualitsation"
        </li>
    </ul>
</ul>
<ul>
    <li><strong>/data</strong>
        ": Contains all data of the plot"
    </li>
    <ul>
        <li><strong>/data/gates&netlists</strong>
            ": contains the files needed to generate the plots"
        </li>
        <ul>
            <li><strong>/data/gates&netlists/chip_1</strong>
            ": contains all files involving chip 1."
            </li>
            <li><strong>/data/gates&netlists/chip_2</strong>
            ": contains all files involving chip 2."
            </li>
        </ul>
        <li><strong>/data/results</strong>
            ": contains a result csv file as output from the code"
        </li>
    </ul>
</ul>

## Authors:
- Ilias Benaissa
- Stijn Bekkers
- Sjors Lockhorst