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
SILVER = (192,192,192)
######END Colors###########

########Sizing###########
SCREEN_HEIGHT = 905
SCREEN_WIDTH = 1000



#Node dimensions
WIDTH = 10
HEIGHT = 10
MARGIN = 5

# Button dimensions
BUTTON_WIDTH =  75
BUTTON_HEIGHT = 25

numRows, numColumns = 60, 60
x_offset = MARGIN+WIDTH
y_offset = MARGIN+HEIGHT
#########END Sizing###########


#### Helper functions ####
def conv_screen_to_grid(pos):
    column = pos[0] // (WIDTH + MARGIN)
    row = pos[1] // (HEIGHT + MARGIN)
    return column, row

def draw_text(text, font_name, size, color, x, y, align="nw"):
    font = pygame.font.SysFont(font_name, size, bold=False, italic=False)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "nw":
        text_rect.topleft = (x, y)
    if align == "ne":
        text_rect.topright = (x, y)
    if align == "sw":
        text_rect.bottomleft = (x, y)
    if align == "se":
        text_rect.bottomright = (x, y)
    if align == "n":
        text_rect.midtop = (x, y)
    if align == "s":
        text_rect.midbottom = (x, y)
    if align == "e":
        text_rect.midright = (x, y)
    if align == "w":
        text_rect.midleft = (x, y)
    if align == "center":
        text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def place_button(x, y, width, height, text, font, font_color, selected, node_color = 'None'):
    text_x = x
    text_y = y+5
    pygame.draw.rect(screen, WHITE, [x, y, width, height])
    draw_text(text, font, 15, BLACK, text_x, text_y)
    if node_color != 'None':
        node_x = (x+width)-20
        node_y = text_y+2
        pygame.draw.rect(screen, node_color, [node_x, node_y, WIDTH, HEIGHT])
    if selected:
        pygame.draw.rect(screen, BLACK, [x, y, width, 0])
        pygame.draw.rect(screen, BLACK, [x, y+height, width, 0])
        pygame.draw.rect(screen, BLACK, [x, y, 0, height])
        pygame.draw.rect(screen, BLACK, [x+width, y, 0, height])

def button_clicked(pos, x, y, width, height):
    button_limit_x = x+width
    button_limit_y = y+height
    if pos[0] in range(x, button_limit_x) and pos[1] in range(y, button_limit_y):
        return True
    else: 
        return False
        


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
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.update()

# Draw grid
for row in range(numRows):
    for column in range(numColumns):
        color = WHITE
        pygame.draw.rect(screen, color,
                         [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])



#********************GAME LOOP********************#

### runtime flags ###
running = True
start_node_placed = False
end_node_placed = False
target_node_placed = False
clicked_run = False
finished = False
start_selected = False
end_selected = False
wall_selected = False
clear_selected = False
run_selected = False
###END RUNTIME FLAGS#####

node_select_count = 0
visited_nodes = []
while running:
    screen.fill(BLACK)
    #**************Event Handler****************#
    if not run_selected:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] > 905:
                        start_selected = button_clicked(pos, 910, 10, 85, 30)
                        end_selected = button_clicked(pos, 910, 50, 85, 30)
                        wall_selected = button_clicked(pos, 910, 90, 85, 30)
                        run_selected = button_clicked(pos, 910, 130, 85, 30)
                        clear_selected = button_clicked(pos, 910, 170, 85, 30)
                    
                    column, row = conv_screen_to_grid(pos)  #convert the screen coordinates to grid coordinates
                    if start_selected:
                        if not start_node_placed:
                            start_node = str([column, row])
                            grid[row][column] = 1   # will cause the node to turn green when drawn again
                            start_node_placed = True
                    elif end_selected:
                        end_node = str([column, row])
                        if grid[row][column] != 1 and not end_node_placed:
                            grid[row][column] = 2   # will cause the node to turn red when drawn again
                            end_node_placed = True
                    elif wall_selected:
                        wall_node = str([column, row])
                        if grid[row][column] != 1 and grid[row][column] != 2:
                            graph.remove_vertex(wall_node)
                            grid[row][column] = 3  # will cause the node to turn black when drawn again
                        elif grid[row][column] == 3:
                            graph.add_removed_vertex(wall_node)
                            grid[row][column] = 0
                    elif run_selected:
                        print("running...")
                        graph.det_adjacent_nodes()              # calls function to determine the adjacent nodes in the grid
                        shortest_path, visited_nodes = djikstra(graph, start_node, end_node)   # calls function that performs the pathfinding algorithm on the grid
                    elif clear_selected:
                        graph.reset_graph()
                        grid = [[[x,y] for x in range(numRows)] for y in range(numColumns)]
                        # take each element(node) from the grid array, which is [x, y], and load it to the graph as a vertex
                        for row in range(numRows):
                            for column in range(numColumns):
                                vertex_key = str(grid[row][column]) # a string version of the coordinate is used as the nodes key
                                graph.add_vertex(Node(vertex_key, grid[row][column]))
                        clicked_run = False
                        finished = False
                        start_node_placed = False
                        end_node_placed = False

                    """
                    elif pygame.mouse.get_pressed()[0] and wall_selected:
                            wall_node = str([column, row])
                            if grid[row][column] != 1 and grid[row][column] != 2:
                                graph.remove_vertex(wall_node)
                                grid[row][column] = 3  # will cause the node to turn black when drawn again
                           
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        graph.det_adjacent_nodes()              # calls function to determine the adjacent nodes in the grid
                        shortest_path, visited_nodes = djikstra(graph, start_node, end_node)   # calls function that performs the pathfinding algorithm on the grid
                        pressed_r = True
                    if event.key == pygame.K_c:
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
                """
                        
                # end event handler
        except KeyError:
            pass
        except IndexError:
            pass
    
    if run_selected and not finished:
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
                run_selected = False
                    

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
            if grid[row][column] == 0:
                color = WHITE
            pygame.draw.rect(screen, color,
                             [x_offset * column + MARGIN, y_offset * row + MARGIN, WIDTH, HEIGHT])
    pygame.draw.rect(screen, SILVER, [905, 0, SCREEN_WIDTH-SCREEN_HEIGHT, SCREEN_HEIGHT]) 
    place_button(910, 10, 85, 30, 'Start node', 'calibri', BLACK, start_selected, node_color=GREEN)
    place_button(910, 50, 85, 30, 'End node', 'calibri', BLACK, end_selected, node_color=RED)
    place_button(910, 90, 85, 30, 'Wall node', 'calibri', BLACK, wall_selected, node_color=BLACK)
    place_button(910, 130, 85, 30, 'Run', 'calibri', BLACK, run_selected, node_color='None')
    place_button(910, 170, 85, 30, 'Clear', 'calibri', BLACK, clear_selected, node_color='None')
            
            

    pygame.display.update()

    #****************END GAME LOOP********************#

#*************************************************#


