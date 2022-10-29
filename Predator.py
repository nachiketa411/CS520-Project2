import random

from Agent import Agent
from BiBFS import BidirectionalSearch


class Predator:
    def __init__(self, graph_dict):
        node_list = list(graph_dict.graph.keys())
        self.graph = graph_dict.graph
        self.currPos = random.choice(node_list)
        self.path = []
        self.path.append(self.currPos)
        self.agent = None

    def initialize(self, agent: Agent):
        self.agent = agent

    def take_next_move(self):
        graph_traverse = BidirectionalSearch(self.graph)
        print('Predator Pos: ', self.currPos)
        print('Agent Pos: ', self.agent.currPos)

        # need to update the method to return the complete instead of just the intersection point
        next_move = graph_traverse.bidirectional_search(self.currPos, self.agent.currPos)
        print('Predator Next Move Path: ', next_move)
        self.currPos = next_move[1]
        self.path.append(self.currPos)
