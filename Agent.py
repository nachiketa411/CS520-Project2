import heapq
import operator
import random
import copy
import numpy as np

from abc import ABC, abstractmethod

from BiBFS import BidirectionalSearch
from Constants import NO_OF_NEXT_STEP_PREDICTIONS_FOR_AGENT_2, NO_OF_NODES, PROB_OF_DISTRACTED_PREDATOR
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

    # To know which neighbour is closer to the Agent and generating transition probabilities accordingly
    def neighbours_order(self, node, dist_dict):
        probabilities = {}
        if len(self.graph[node]) == 2:
            a = self.graph[node][0]
            b = self.graph[node][1]
            a_dist_from_agent = dist_dict[a][self.currPos]
            b_dist_from_agent = dist_dict[b][self.currPos]
            if a_dist_from_agent > b_dist_from_agent:
                probabilities[a] = 0.8
                probabilities[b] = 0.2
            elif a_dist_from_agent < b_dist_from_agent:
                probabilities[a] = 0.2
                probabilities[b] = 0.8
            else:
                probabilities[a] = 0.5
                probabilities[b] = 0.5

        else:
            a = self.graph[node][0]
            b = self.graph[node][1]
            c = self.graph[node][2]
            a_dist_from_agent = dist_dict[a][self.currPos]
            b_dist_from_agent = dist_dict[b][self.currPos]
            c_dist_from_agent = dist_dict[c][self.currPos]
            if a_dist_from_agent < b_dist_from_agent:
                if a_dist_from_agent < c_dist_from_agent:
                    probabilities[a] = (0.4 / 3) + 0.6
                    probabilities[b] = (0.4 / 3)
                    probabilities[c] = (0.4 / 3)

                elif a_dist_from_agent == c_dist_from_agent:
                    probabilities[a] = (0.4 / 3) + 0.3
                    probabilities[b] = (0.4 / 3)
                    probabilities[c] = (0.4 / 3) + 0.3

                else:
                    probabilities[a] = (0.4 / 3)
                    probabilities[b] = (0.4 / 3)
                    probabilities[c] = (0.4 / 3) + 0.6

            elif a_dist_from_agent > b_dist_from_agent:
                if b_dist_from_agent < c_dist_from_agent:
                    probabilities[a] = (0.4 / 3)
                    probabilities[b] = (0.4 / 3) + 0.6
                    probabilities[c] = (0.4 / 3)

                elif b_dist_from_agent == c_dist_from_agent:
                    probabilities[a] = (0.4 / 3)
                    probabilities[b] = (0.4 / 3) + 0.3
                    probabilities[c] = (0.4 / 3) + 0.3

                else:
                    probabilities[a] = (0.4 / 3)
                    probabilities[b] = (0.4 / 3)
                    probabilities[c] = (0.4 / 3) + 0.6

            else:
                if a_dist_from_agent > c_dist_from_agent:
                    probabilities[a] = (0.4 / 3)
                    probabilities[b] = (0.4 / 3)
                    probabilities[c] = (0.4 / 3) + 0.6

                elif a_dist_from_agent == c_dist_from_agent:
                    probabilities[a] = (0.4 / 3) + 0.2
                    probabilities[b] = (0.4 / 3) + 0.2
                    probabilities[c] = (0.4 / 3) + 0.2

                else:
                    probabilities[a] = (0.4 / 3) + 0.3
                    probabilities[b] = (0.4 / 3) + 0.3
                    probabilities[c] = (0.4 / 3)

        return probabilities

    def convert_dict_to_transition_matrix(self, dist_dict):
        dynamic_transition_matrix = []
        for i in range(50):
            temp = [0] * 50
            neighbour_probability = self.neighbours_order(i, dist_dict)
            for j in neighbour_probability.items():
                temp[j[0]] = j[1]
            dynamic_transition_matrix.append(temp)
        return dynamic_transition_matrix

    def get_expected_distance_of_predator_from_agent(self, belief_mat_for_predator,
                                                     curr_pos_of_agent, graph_distances):

        expected_distance = {}
        neighbours_of_agent = self.graph[curr_pos_of_agent]

        for neighbour in neighbours_of_agent:
            expected_distance[neighbour] = np.dot(np.array(graph_distances[neighbour]), np.array(belief_mat_for_predator))
        return expected_distance

    def get_smallest_path_from_source_to_dest(self, source, dest):
        temp = copy.deepcopy(self.graph)
        bi_bfs = BidirectionalSearch(temp)
        return bi_bfs.bidirectional_search(source, dest)

    # Finds a path from the given list of neighbours to the destination/pos_y
    def find_path(self, neighbours, pos_y):
        path_dictionary = {}
        for i in range(len(neighbours)):
            temp = copy.deepcopy(self.graph)
            bi_bfs = BidirectionalSearch(temp)
            x = neighbours[i]
            y = pos_y
            path = bi_bfs.bidirectional_search(x, y)
            path_dictionary[neighbours[i]] = path
        return path_dictionary

    def update_belief_after_distracted_predator_moves(self, old_belief_mat, agent_curr_pos):
        belief_mat = np.zeros(len(old_belief_mat))
        for node in range(len(belief_mat)):
            neighbours = self.graph[node]
            for neighbour in neighbours:
                neighbours_of_neighbour = self.graph[neighbour]
                best_equivalent_set_of_moves = self.get_neighbours_with_equal_distance_to_agent(neighbours_of_neighbour, agent_curr_pos)
                if node in best_equivalent_set_of_moves:
                    belief_mat[node] += (1 - PROB_OF_DISTRACTED_PREDATOR) * old_belief_mat[neighbour] * (1 / len(best_equivalent_set_of_moves))

                neighbours_of_prev_pred_pos = self.graph[neighbour]
                belief_mat[node] += PROB_OF_DISTRACTED_PREDATOR * old_belief_mat[neighbour] * (1 / len(neighbours_of_prev_pred_pos))

        return belief_mat

    def get_neighbours_with_equal_distance_to_agent(self, neighbours, destination):
        dict_of_paths = self.find_path(neighbours, destination)
        list_of_paths = dict_of_paths.values()
        list_of_dist = []
        for path in list_of_paths:
            list_of_dist.append(len(path))
        smallest_dist = min(list_of_dist)
        best_neighbours = []
        for neighbour, path in dict_of_paths.items():
            if len(path) == smallest_dist:
                best_neighbours.append(neighbour)
        return best_neighbours



