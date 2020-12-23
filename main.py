"""
Visualizer for djikstra's algorithm
"""
import pygame
from NodeGraph import *


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


#### Helper functions ####
def conv_screen_to_grid(pos):
    column = pos[0] // (WIDTH + MARGIN)
    row = pos[1] // (HEIGHT + MARGIN)
    return column, row
    
####END HELPER FUNCTIONS####

pygame.init()

# create 2-d grid array (which will be loaded to graph)
grid = [[[x,y] for x in range(numRows)] for y in range(numColumns)]


# graph object used for djikstra's algorithm
graph = Graph()

# take each element(node) from the grid array, which is [x, y], and load it to the graph as a vertex
for row in range(numRows):
    for column in range(numColumns):
        vertex_key = str(grid[row][column]) # a string version of the coordinate is used as the nodes key
        graph.add_vertex(Node(vertex_key, grid[row][column]))
top = pygame.display.set_mode([20, SCREEN_SIZE])
screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])
pygame.display.update()

#Draw grid
for row in range(numRows):
    for column in range(numColumns):
        color = WHITE
        pygame.draw.rect(screen, color,
                         [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])

#********************GAME LOOP********************#

### runtime flags ###
running = True
start_node_placed = False
target_node_placed = False
pressed_r = False
finished = False
###END RUNTIME FLAGS#####

node_select_count = 0
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
                    start_node = str([column, row])
                    grid[row][column] = 1   # will cause the node to turn green when drawn again
                    start_node_placed = True
                elif event.type == pygame.MOUSEBUTTONDOWN and not target_node_placed:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    column, row = conv_screen_to_grid(pos)  # convert the screen coordinates to grid coordinates
                    end_node = str([column, row])
                    if grid[row][column] != 1:
                        grid[row][column] = 2   # will cause the node to turn red when drawn again
                        target_node_placed = True
                elif pygame.mouse.get_pressed()[0] and start_node_placed and target_node_placed:
                        pos = pygame.mouse.get_pos()
                        column, row = conv_screen_to_grid(pos)  # convert the screen coordinates to grid coordinates
                        wall_node = str([column, row])
                        if grid[row][column] != 1 and grid[row][column] != 2:
                            graph.remove_vertex(wall_node)
                            grid[row][column] = 3  # will cause the node to turn black when drawn again
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        graph.det_adjacent_nodes()              # calls function to determine the adjacent nodes in the grid
                        shortest_path, visited_nodes = djikstra(graph, start_node, end_node)   # calls function that performs the pathfinding algorithm on the grid
                        pressed_r = True
                    if event.key == pygame.K_t:
                        graph.reset_graph()
                        grid = [[[x,y] for x in range(numRows)] for y in range(numColumns)]
                        # take each element(node) from the grid array, which is [x, y], and load it to the graph as a vertex
                        for row in range(numRows):
                            for column in range(numColumns):
                                vertex_key = str(grid[row][column]) # a string version of the coordinate is used as the nodes key
                                graph.add_vertex(Node(vertex_key, grid[row][column]))
                        start_node_placed = False
                        target_node_placed = False
                        pressed_r = False
                        finished = False
                        
                # end event handler
        except KeyError:
            pass
    
    if pressed_r and not finished:
        if visited_nodes:
            node_coord = graph.get_vertex(visited_nodes.pop(0)).get_value()
            if str(node_coord) != end_node and not finished:
                column = node_coord[0]
                row = node_coord[1]
                grid[row][column] = 4
            else:
                for node_key in shortest_path:
                    node_coord = graph.get_vertex(node_key).get_value()
                    column = node_coord[0]
                    row = node_coord[1]
                    grid[row][column] = 5
                finished = True 
                pressed_r = False
                    

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


