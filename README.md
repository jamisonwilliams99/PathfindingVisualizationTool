# PathfindingVisualizationTool

# This project provides a visualization of Djikstra's algorithm in finding the shortest path between a start node and an end node.

# The user is provided with a 60x60 grid where they can place a start node (green), an end node (red), and however many "wall" nodes (black)
# they please by simply clicking the cells.

# User guide:
# - To place a start node, click the "start node" button on the right side of the grid, and then click the desire cell in the grid for the start node
# - The same steps described above applies for an end node
# - To place a wall node, click the "wall node button" on the right side of the grid, and then click and drag to place the desired number of wall nodes.
#       - NOTE: a wall node acts as a barrier between the start and end nodes which the algorithm will have to work around in order to find the shortest path
# - To remove an undesired wall node, click the the already placed wall node 
#       - NOTE: the "wall node" button on the right must be selected
# - Once a start node and end node (and desired walls) are selected, click the "run" button on the right side of the grid to run Djikstra's algorithm and wait a few moments for the visualization to begin
# - To reset the grid, click the "clear" button on the right side

# Occasionally, the program window will get a "not responding" error. I have not quite figured out why it does this. If this happens, close the window and rerun the program. 
