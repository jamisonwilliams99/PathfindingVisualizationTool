"""
Visualizer for djikstra's algorithm
"""
import pygame
from NodeGraph import *

pygame.init()

#########Colors##########
WHITE = (255,255,255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
######END Colors###########

########Sizing###########
SCREEN_SIZE = 905

#Node dimensions
WIDTH = 10
HEIGHT = 10
MARGIN = 5

numRows, numColumns = 60, 60
x_offset = MARGIN+WIDTH
y_offset = MARGIN+HEIGHT
#########END Sizing###########

# create 2-d grid array (which will be loaded to graph)
grid = [[[x,y] for x in range(numRows)] for y in range(numColumns)]

# graph object used for djikstra's algorithm
graph = Graph()

# take each element(node) from the grid array, which is [x, y], and load it to the graph as a vertex
for row in range(numRows):
    for column in range(numColumns):
        vertex_key = str(grid[row][column]) # a string version of the coordinate is used as the nodes key
        graph.add_vertex(Node(vertex_key, grid[row][column]))


screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])
pygame.display.update()

#Draw grid
for row in range(numRows):
    for column in range(numColumns):
        color = WHITE
        if grid[row][column] == 1:
            color = GREEN
        pygame.draw.rect(screen, color,
                         [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])

#********************GAME LOOP********************#
node_select_count = 0


running = True
pressed_r = False
finished = False
visited_nodes = []
while running:
    screen.fill(BLACK)
    #**************Event Handler****************#
    if not pressed_r:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and node_select_count == 0:
                pos = pygame.mouse.get_pos()
                #convert the screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                start_node = str([column, row])
                grid[row][column] = 1   # will cause the node to turn green when drawn again
                node_select_count += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and node_select_count == 1:
                pos = pygame.mouse.get_pos()
                # convert the screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                end_node = str([column, row])
                grid[row][column] = 2   # will cause the node to turn red when drawn again
                node_select_count += 1
                #nodes_selected = True
            elif event.type == pygame.MOUSEBUTTONDOWN and node_select_count == 2:
                pos = pygame.mouse.get_pos()
                # convert the screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                wall_node = str([column, row])
                graph.remove_vertex(wall_node)
                grid[row][column] = 3  # will cause the node to turn red when drawn again
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    graph.det_adjacent_nodes()              # calls function to determine the adjacent nodes in the grid
                    shortest_path, visited_nodes = djikstra(graph, start_node, end_node)   # calls function that performs the pathfinding algorithm on the grid

                    pressed_r = True
                    """
                    for node_key in visited_nodes:
                        node_coord = graph.get_vertex(node_key).get_value()
                        column = node_coord[0]
                        row = node_coord[1]
                        grid[row][column] = 4


                    for node_key in shortest_path:
                        node_coord = graph.get_vertex(node_key).get_value()
                        column = node_coord[0]
                        row = node_coord[1]
                        grid[row][column] = 5
                    """
            # end event handler
    
    if pressed_r:
        if visited_nodes:
            node_coord = graph.get_vertex(visited_nodes.pop(0)).get_value()
            if str(node_coord) != end_node and not finished:
                column = node_coord[0]
                row = node_coord[1]
                grid[row][column] = 4
            else:
                finished = True 
                for node_key in shortest_path:
                    node_coord = graph.get_vertex(node_key).get_value()
                    column = node_coord[0]
                    row = node_coord[1]
                    grid[row][column] = 5





    #Draw grid
    for row in range(numRows):
        for column in range(numColumns):
            color = WHITE
            if grid[row][column] == 4:
                color = YELLOW
            pygame.draw.rect(screen, color,
                             [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])
            if grid[row][column] == 5:
                color = BLUE
            pygame.draw.rect(screen, color,
                             [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen, color,
                             [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])
            if grid[row][column] == 2:
                color = RED
            pygame.draw.rect(screen, color,
                             [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])
            if grid[row][column] == 3:
                color = BLACK
            pygame.draw.rect(screen, color,
                             [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])
            
            

    pygame.display.update()

    #****************END GAME LOOP********************#

#*************************************************#
