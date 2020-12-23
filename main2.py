"""
Visualizer for djikstra's algorithm
"""
import pygame
from NodeGraph2 import *


#### Helper functions ####
def conv_screen_to_grid(pos):
    column = pos[0] // (WIDTH + MARGIN)
    row = pos[1] // (HEIGHT + MARGIN)
    return column, row

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
        pygame.draw.rect(screen, color,
                         [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])

#********************GAME LOOP********************#
node_select_count = 0

### runtime flags ###
running = True
start_node_placed = False
target_node_placed = False
pressed_r = False
finished = False


visited_nodes = []
while running:
    screen.fill(BLACK)
    #**************Event Handler****************#
    if not pressed_r:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not start_node_placed:
                    pos = pygame.mouse.get_pos()
                    column, row = conv_screen_to_grid(pos)  #convert the screen coordinates to grid coordinates
                    graph.set_start_node(graph.get_vertex(str([column, row])))
                    start_node_placed = True

                elif event.type == pygame.MOUSEBUTTONDOWN and not target_node_placed:
                    pos = pygame.mouse.get_pos()
                    column, row = conv_screen_to_grid(pos)  # convert the screen coordinates to grid coordinates
                    graph.set_target_node(graph.get_vertex(str([column, row])))
                    target_node_placed = True

                elif pygame.mouse.get_pressed()[0] and start_node_placed and target_node_placed:
                        pos = pygame.mouse.get_pos()
                        column, row = conv_screen_to_grid(pos)  # convert the screen coordinates to grid coordinates
                        node_key = str([column, row])
                        temp_node = graph.get_vertex(node_key)
                        if not graph.is_start_node(temp_node) and not graph.is_target_node(temp_node):
                            graph.set_wall_node(temp_node)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        graph.det_adjacent_nodes()              # calls function to determine the adjacent nodes in the grid
                        shortest_path, visited_nodes = djikstra(graph)   # calls function that performs the pathfinding algorithm on the grid
                        pressed_r = True  

                        
                # end event handler
        except KeyError:
            pass
    
    if pressed_r:
        if visited_nodes:
            visited_node = graph.get_vertex(visited_nodes.pop(0))
            if not graph.is_target_node(visited_node) and not finished:
                graph.set_is_checked_node(visited_node)
            else:
                finished = True 
                for node_key in shortest_path:
                    path_node = graph.get_vertex(node_key)
                    graph.set_is_path_node(path_node)



    #Draw grid
    for row in range(numRows):
        for column in range(numColumns):
            node_key = str(grid[row][column])
            temp_node = graph.get_vertex(node_key)
            color = WHITE
            if temp_node.is_checked_node:
                color = YELLOW
            pygame.draw.rect(screen, color,
                             [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])
            if temp_node.is_path_node:
                color = BLUE
            pygame.draw.rect(screen, color,
                             [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])
            if graph.is_start_node(temp_node):
                color = GREEN
            pygame.draw.rect(screen, color,
                             [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])
            if graph.is_target_node(temp_node):
                color = RED
            pygame.draw.rect(screen, color,
                             [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])
            if temp_node.is_wall_node:
                color = BLACK
                #graph.remove_vertex(node_key)
            pygame.draw.rect(screen, color,
                             [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])
                             
            
            

    pygame.display.update()

    #****************END GAME LOOP********************#

#*************************************************#


