import random
from abc import ABC, abstractmethod

from Constants import NO_OF_NODES
from Predator import Predator
from Prey import Prey


class Agent(ABC):
    def __init__(self, prey: Prey, graph_dict):
        self.predator = None
        self.currPos = None
        self.path = None

        self.prey = prey
        self.graph = graph_dict
        self.counter = 0

    def initialize(self, predator: Predator):
        self.predator = predator
        node_list = list(self.graph.getKeys())
        node_list.remove(self.predator.currPos)
        node_list.remove(self.prey.currPos)
        self.currPos = random.choice(node_list)
        self.path = [].append(self.currPos)

    @abstractmethod
    def move_agent(self):
        pass

    @abstractmethod
    def take_next_move(self):
        pass
