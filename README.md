# PathfindingVisualizationTool

# This project provides a visualization of Djikstra's algorithm in finding the shortest path between a start node and an end node.

# The user is provided with a 60x60 grid where they can place a start node (green), an end node (red), and however many "wall" nodes 
# they please by simply clicking the cells.

# How to place nodes:
#	- the start node will automatically be the first cell that is clicked
#	- the end node will be the second
#	- any following cells that are clicked will be "walls"

# After all desired nodes are placed, press 'R' to begin the search

# Known issues:
#	- MOST IMPORTANT FOR USER, a runtime error will occur if the same node is clicked twice 
#
#	- after pressing 'R', it will take appriximately 10 seconds for the animation to begin. This is because the program must first
#	  complete the algorithm before beginning the animation. Djikstra's algorith is notoriously slow, as it must first find the distance
#	  between every node in the grid and the start node before it can determine the shortest path. 
#
#	- The animation also takes a very long time to complete. I am currently trying to figure out how to make it more efficient.
#	
