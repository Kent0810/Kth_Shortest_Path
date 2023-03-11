# Maximum flow problem

This folder contains algorithms implementations and visualization code. This README file will instruct you how to use them, modify on your own to solve your own inputs and visualize your map.

Ford-Fulkerson algorithm
---
In `ford_fulkerson.py` - line 70, you will see 
```python
test_graph = [[...],
              [...],
              ...]
```
That is where you put your input graph (as adjacency matrix, as describe in the report), and you will have to install `numpy` as a dependency to run the code. The output flow graph and other information will be printed out to standard output.

Dinic's algorithm
---
in `dinic_algorithm.py` - line 61, you will see
```python
test_graph = [[...],
              [...],
              ...]
```
Place your input there and run the code, without installing any other dependency. The output will be printed out to standard output.

Visualization
---
`visualize.py` will handle all the visualizations, given all the inputs are done correctly. There are 2 files that you need to care about - `map.txt` and `flow_graph.json`.

## map.txt
will tell the program how to place endpoints on the screen. For example, in `map (theoretical).txt` (which holds the map for theretical map. You can use this by replacing `map.txt` with this file and rename this to `map.txt`), you will see
```
-1	-1	-1	-1	-1	-1	-1
-1	-1	1	-1	3	-1	-1
-1	-1	-1	-1	-1	-1	-1
0	-1	-1	-1	-1	-1	5
-1	-1	-1	-1	-1	-1	-1
-1	-1	2	-1	4	-1	-1
-1	-1	-1	-1	-1	-1	-1
```
This is a grid that the map will be shown according to. `-1` cells are empty space and `0-5` cells are where the endpoints will be placed. To create a file like this, simplest way is to do the placing in Excel, then copy the whole thing right into this txt file. It will be tab-delimited and ready to go.

## flow_graph.json
Simply paste the output graph from above algorithms into this file and save it!

## visualize.py
This is the visualization code. To run it, simply install `Pygame` and run it (with `map.txt` and `flow_graph.json` done beforehand). A window will pop up with the visualization run forever.