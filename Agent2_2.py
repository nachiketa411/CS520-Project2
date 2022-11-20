import copy
import random

import numpy as np

from Constants import NO_OF_STEPS_1, NO_OF_NODES, NO_OF_NEXT_STEP_PREDICTIONS_FOR_AGENT_2, NO_OF_STEPS_4
from Agent import Agent
from Predator import Predator
from Prey import Prey
from BiBFS import BidirectionalSearch


class Agent2_2(Agent):

    def move_agent(self, trans_mat):

        # Creating a belief List
        belief_mat = [0] * NO_OF_NODES
        belief_mat[self.prey.currPos] = 1

        # Return 1 for Success, -1 when predator catches the Agent and 0 when counter exhausts
        count = 0
        while count <= NO_OF_STEPS_4:
            next_move = self.get_next_move(belief_mat, trans_mat)
            if next_move == -1:
                self.prey.take_next_move(copy.deepcopy(self.graph))
                if self.currPos == self.prey.currPos:
                    print("Yippiieeee")
                    count += 1
                    return [count, -1, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]
                self.predator.take_next_move()
                if self.currPos == self.predator.currPos:
                    print("Ded")
                    count += 1
                    return [count, -2, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]
                count += 1
                continue
            self.currPos = next_move
            self.path.append(next_move)
            if self.currPos == self.prey.currPos:
                print("Yippiieeee")
                count += 1
                return [count, -1, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]
            elif self.currPos == self.predator.currPos:
                print("Ded")
                count += 1
                return [count, -2, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]
            self.prey.take_next_move(copy.deepcopy(self.graph))
            belief_mat = [0] * NO_OF_NODES
            belief_mat[self.prey.currPos] = 1

            if self.currPos == self.prey.currPos:
                print("Yippiieeee")
                count += 1
                return [count, -1, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]

            self.predator.take_next_move()

            if self.currPos == self.predator.currPos:
                print("Ded")
                count += 1
                return [count, -2, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]

            count += 1
        return [count, -3, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]

    def get_next_move(self, belief, transition_matrix):

        no_of_prediction_steps = 0

        neighbours = self.graph[self.currPos]
        # To find the distance between neighbours of Agent and Predator
        path_predator = self.find_path(neighbours, self.predator.currPos)
        # To find the distance between neighbours of Agent and Prey
        path_prey = self.find_path(neighbours, self.prey.currPos)

        # Current Position to Predator/Prey
        currpos_to_predator = self.find_path([self.currPos], self.predator.currPos)[self.currPos]
        currpos_to_prey = self.find_path([self.currPos], self.prey.currPos)[self.currPos]

        while no_of_prediction_steps < len(currpos_to_prey) - 1:
            no_of_prediction_steps = no_of_prediction_steps + 1

        for i in range(no_of_prediction_steps):
            np_belief = np.array(belief)
            np_2d_transition_matrix = np.array(transition_matrix)
            np_belief = np_belief @ np_2d_transition_matrix
            belief = list(np_belief)

        max_belief = max(belief)
        possible_prey_positions = []
        for i in range(len(belief)):
            if belief[i] == max_belief:
                possible_prey_positions.append(i)

        prey_next_position = 0
        if possible_prey_positions:
            prey_next_position = random.choice(possible_prey_positions)

        curr_pos_to_prey_expected = self.find_path([self.currPos], prey_next_position)[self.currPos]

        # To find the distance between neighbours of Agent and expected Prey position
        path_to_prey_expected = self.find_path(neighbours, prey_next_position)

        # The distance between each neighbour of agent and prey/predator
        len_agent_predator = {key: len(value) for key, value in path_predator.items()}
        # len_agent_prey = {key: len(value) for key, value in path_prey.items()}
        len_agent_prey_expected = {key: len(value) for key, value in path_to_prey_expected.items()}

        # Logic for Agent 1

        best_neighbour = []
        # Neighbors that are closer to the Prey and farther from the Predator.
        for i in neighbours:
            if len_agent_prey_expected[i] < len(curr_pos_to_prey_expected) and \
                    (len_agent_predator[i] > len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not farther from the Prey and farther from the Predator.
        for i in neighbours:
            if len_agent_prey_expected[i] == len(curr_pos_to_prey_expected) and \
                    (len_agent_predator[i] > len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are farther from the Predator.
        for i in neighbours:
            if len_agent_predator[i] > len(currpos_to_predator):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are closer to the Prey and not closer to the Predator.
        for i in neighbours:
            if len_agent_prey_expected[i] < len(curr_pos_to_prey_expected) and \
                    (len_agent_predator[i] == len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not farther from the Prey and not closer to the Predator.
        for i in neighbours:
            if len_agent_prey_expected[i] == len(curr_pos_to_prey_expected) and \
                    (len_agent_predator[i] == len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not closer to the Predator.
        for i in neighbours:
            if len_agent_predator[i] == len(currpos_to_predator):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Sit still and pray.
        return -1

