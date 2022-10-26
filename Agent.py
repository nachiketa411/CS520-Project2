import random

from Constants import NO_OF_NODES


class Agent:
    def __init__(self, predator_position, prey_position, graph_dict):
        node_list = list(graph_dict.graph.getKeys())
        node_list.remove(predator_position)
        node_list.remove(prey_position)
        self.curPos = random.choice(node_list)
        self.path = []
