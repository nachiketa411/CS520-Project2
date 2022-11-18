import heapq
import operator
import random
import copy
import numpy as np

from abc import ABC, abstractmethod

from Constants import NO_OF_NEXT_STEP_PREDICTIONS_FOR_AGENT_2
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
        node_list = copy.deepcopy(list(self.graph.keys()))
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
    def get_next_move(self):
        pass

    def get_expected_distance_of_prey_from_agent(self, belief_mat, transition_matrix,
                                                 curr_pos_of_agent, curr_pos_of_prey, graph_distances):

        no_of_next_steps = NO_OF_NEXT_STEP_PREDICTIONS_FOR_AGENT_2

        expected_distance = {}
        neighbours_of_agent = self.graph[curr_pos_of_agent]
        dist_of_curr_agent_to_prey = graph_distances[curr_pos_of_agent][curr_pos_of_prey]

        while no_of_next_steps >= dist_of_curr_agent_to_prey:
            no_of_next_steps = no_of_next_steps - 1

        for i in range(no_of_next_steps):
            np_belief = np.array(belief_mat)
            np_2d_transition_matrix = np.array(transition_matrix)
            np_belief = np_belief @ np_2d_transition_matrix
            belief_mat = list(np_belief)

        top_3 = list(zip(*heapq.nlargest(3, enumerate(belief_mat), key=operator.itemgetter(1))))[0]
        new_belief_mat = [0] * len(belief_mat)
        for index in top_3:
            new_belief_mat[index] = belief_mat[index]
        for neighbour in neighbours_of_agent:
            expected_distance[neighbour] = np.dot(np.array(graph_distances[neighbour]), np.array(new_belief_mat))
        return expected_distance
