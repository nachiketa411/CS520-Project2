from abc import ABC

from Agent import Agent
from Predator import Predator
from Prey import Prey


class Agent1(Agent, ABC):

    def __init__(self, prey: Prey, graph_dict):
        super().__init__(prey, graph_dict)
        self.predator = Predator(self.graph)
        super().initialize(self.predator)
        self.predator.initialize(super().__class__)

        print('Agent location: ', self.currPos)
        print('Prey location: ', self.prey.currPos)
        print('Predator Object agent location: ', self.predator.agent.currPos)

    def move_agent(self):
        pass
