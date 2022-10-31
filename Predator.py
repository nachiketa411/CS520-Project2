import random
import copy
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
        g = copy.deepcopy(self.graph)
        graph_traverse = BidirectionalSearch(g)
        # print('Predator Pos: ', self.currPos)
        # print('Agent Pos: ', self.agent.currPos)

        # need to update the method to return the complete instead of just the intersection point
        x = self.currPos
        y = self.agent.currPos
        # print(y,type(y))
        next_move = graph_traverse.bidirectional_search(x, y)
        # print('Predator Next Move Path: ', next_move)
        if len(next_move) > 1:
            self.currPos = next_move[1]
        else:
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("Errorrrrrrrrrrrrrr")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        self.path.append(self.currPos)
