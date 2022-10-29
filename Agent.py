import random
from abc import ABC, abstractmethod

from Prey import Prey


class Agent(ABC):
    def __init__(self, prey, graph_dict):
        self.predator = None
        self.currPos = None
        self.path = None

        self.prey = prey
        self.graph = graph_dict
        self.counter = 0

    def initialize(self, predator):
        self.predator = predator
        node_list = list(self.graph.keys())
        node_list.remove(self.predator.currPos)
        if self.predator.currPos != self.prey.currPos:
            node_list.remove(self.prey.currPos)
        self.currPos = random.choice(node_list)
        self.path = []
        self.path.append(self.currPos)

    @abstractmethod
    def move_agent(self):
        pass

    @abstractmethod
    def take_next_move(self):
        pass
