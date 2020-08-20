import sys
import pygame

# returns the key in a dictionary given the value
def get_key(dict, val):

    for key, node in dict.items():
        if val == node.value:
            return key

class Node:
    def __init__(self, n, n_val):
        self.name = n
        self.value = n_val
        self.adj_list = list()
        self.distance = sys.maxsize
        self.visited = False
        self.pred_node = 0

    # adds a adjacent node to the current node's adjacency list
    def add_adj_node(self, adjNode):
        if adjNode not in self.adj_list:
            self.adj_list.append(adjNode)
  
    def print_adj_nodes(self):
        print("Node {} is adjacent to: ".format(self.vertex))
        for adjNode in self.adj_list:
            print(adjNode.data)

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_distance(self):
        return self.distance

    def get_neighbors(self):
        return self.adj_list

    def set_distance(self, dist):
        self.distance = dist

    def set_pred_node(self, prev):
        self.pred_node = prev

    def get_pred_node(self):
        return self.pred_node

    def set_visited(self):
        self.visited = True


class Graph:

    def __init__(self):
        self.vertices = {}
        self.num_vertices = 0

    def add_vertex(self, vertex):
        if isinstance(vertex, Node) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            self.num_vertices+=1
            return True
        else:
            return False

    def remove_vertex(self, node_key):
        self.get_vertices().pop(node_key)

    def get_vertex(self, n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def get_vertices(self):
        return self.vertices

    def get_numVertices(self):
        return self.num_vertices

        # Function to add an edge in an undirected graph
    def add_edge(self, u, v):
        if u in self.vertices and v in self.vertices:
            for key, value in self.vertices.items():
                if key == u:
                    value.add_adj_node(v)
                if key == v:
                    value.add_adj_node(u)

    def min_distance(self, dist, shortest_path_set):
        # minimum distance for next node
        min = sys.maxsize

        # search for the nearest node that is not in the shortest path tree
        for v in range(self.num_vertices):
            if dist[v] < min and shortest_path_set[v] == False:
                min = dist[v]
                min_index = v

        return min_index


    def det_adjacent_nodes(self):
        "key 0-25, val [0,0]-[3,3]"
        for key in self.vertices:
            val = self.vertices[key].value
            left, right, bottom, top = [val[0] - 1, val[1]], [val[0] + 1, val[1]], [val[0], val[1] - 1], [val[0], val[1] + 1]

            if left[0] >= 0:
                self.add_edge(key, get_key(self.vertices, left))
                #print(str(key) + " is adjacent to " + str(get_key(self.vertices, left)))
            if right[0] <= 59:
                self.add_edge(key, get_key(self.vertices, right))
                #print(str(key) + " is adjacent to " + str(get_key(self.vertices, right)))
            if bottom[1] >= 0:
                self.add_edge(key, get_key(self.vertices, bottom))
                #print(str(key) + " is adjacent to " + str(get_key(self.vertices, bottom)))
            if top[1] <= 59:
                self.add_edge(key, get_key(self.vertices, top))
                #print(str(key) + " is adjacent to " + str(get_key(self.vertices, top)))


    def print_vertices(self):
        for key, value in self.vertices.items():
            print(key)


    def print_graph(self):
        for i in range(self.V):
            node = self.graph[i]
            node.print_adj_nodes

    def print_pred_nodes_distance(self):
        for key, value in self.vertices.items():
            #print(str(key) + "'s predecessor is: " + str(value.get_pred_node().get_name()))
            print(str(key) + ": " + str(value.get_distance()))


def det_min_distance(queue):
    min_index = 0
    for i, node in enumerate(queue):
        if node.get_distance() < queue[min_index].get_distance():
            min_index = i
    return min_index


def djikstra(graph, start, end):
    start_node = graph.get_vertex(start)

    unvisited_queue = []
    for node in graph.get_vertices().values():
        unvisited_queue.append(node)

    # set the distance of the start node to 0
    start_node.set_distance(0)

    # while unvisited_queue is not empty
    while len(unvisited_queue):
        # need to pop the vertex with the shortest distance from the start node

        cur_node = unvisited_queue.pop(det_min_distance(unvisited_queue))

        # for nodes adjacent to cur_node
        for adjV in cur_node.get_neighbors():
            adj_node = graph.get_vertex(adjV)
            alt_path_dist = cur_node.get_distance() + 1
            if alt_path_dist < adj_node.get_distance():
                adj_node.set_distance(alt_path_dist)
                adj_node.set_pred_node(cur_node)

    cur_node = graph.get_vertex(end).get_pred_node()
    shortest_path = []
    while cur_node != start_node:

        shortest_path.insert(0, cur_node.get_name())
        cur_node = cur_node.get_pred_node()
    return shortest_path


def djikstra(graph, start, end):
    start_node = graph.get_vertex(start)

    unvisited_queue = []
    for node in graph.get_vertices().values():
        unvisited_queue.append(node)

    # set the distance of the start node to 0
    start_node.set_distance(0)

    # while unvisited_queue is not empty
    while len(unvisited_queue):
        # need to pop the vertex with the shortest distance from the start node

        cur_node = unvisited_queue.pop(det_min_distance(unvisited_queue))

        # for nodes adjacent to cur_node
        for adjV in cur_node.get_neighbors():
            adj_node = graph.get_vertex(adjV)
            alt_path_dist = cur_node.get_distance() + 1
            if alt_path_dist < adj_node.get_distance():
                adj_node.set_distance(alt_path_dist)
                adj_node.set_pred_node(cur_node)

    cur_node = graph.get_vertex(end).get_pred_node()
    shortest_path = []
    while cur_node != start_node:

        shortest_path.insert(0, cur_node.get_name())
        cur_node = cur_node.get_pred_node()
    return shortest_path

    
def djikstra(graph, start, end):
    start_node = graph.get_vertex(start)

    unvisited_queue = []
    for node in graph.get_vertices().values():
        unvisited_queue.append(node)

    # set the distance of the start node to 0
    start_node.set_distance(0)

    # while unvisited_queue is not empty
    while len(unvisited_queue):
        # need to pop the vertex with the shortest distance from the start node

        cur_node = unvisited_queue.pop(det_min_distance(unvisited_queue))

        # for nodes adjacent to cur_node
        for adjV in cur_node.get_neighbors():
            adj_node = graph.get_vertex(adjV)
            alt_path_dist = cur_node.get_distance() + 1
            if alt_path_dist < adj_node.get_distance():
                adj_node.set_distance(alt_path_dist)
                adj_node.set_pred_node(cur_node)

    cur_node = graph.get_vertex(end).get_pred_node()
    shortest_path = []
    while cur_node != start_node:

        shortest_path.insert(0, cur_node.get_name())
        cur_node = cur_node.get_pred_node()
    return shortest_path





def main():
    V = 16
    numRows = 4
    numCol = 4
    """
    grid = [
        [0, 0], [1, 0], [2, 0], [3, 0],
        [0, 1], [1, 1], [2, 1], [3, 1],
        [0, 2], [1, 2], [2, 2], [3, 2],
        [0, 3], [1, 3], [2, 3], [3, 3]
    ]
    """
    grid = [
        [[0, 0], [1, 0], [2, 0], [3, 0]],
        [[0, 1], [1, 1], [2, 1], [3, 1]],
        [[0, 2], [1, 2], [2, 2], [3, 2]],
        [[0, 3], [1, 3], [2, 3], [3, 3]]
    ]

    graph = Graph()

    for row in range(numRows):
        for column in range(numCol):
            graph.add_vertex(Node(str(grid[row][column]), grid[row][column]))

    graph.remove_vertex("[1, 2]")

    #graph.print_vertices()

    graph.det_adjacent_nodes()

    djikstra(graph, str([0,2]), str([2, 2]))

    #graph.print_pred_nodes_distance()


#main()



























