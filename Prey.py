import random


class Prey:
    def __init__(self, graph_dict):
        node_list = list(graph_dict.graph.getKeys())
        self.currPos = random.choice(node_list)
        self.path = []

    def get_children_for_next_move(self, graph_dict):
        my_neighbours = list(graph_dict.graph[self.currPos])
        my_neighbours.append(self.currPos)
        next_move = random.choice(my_neighbours)
        self.path.append(next_move)
        return next_move
