import copy
import random

import numpy as np

from Constants import NO_OF_STEPS_1, NO_OF_NODES, NO_OF_NEXT_STEP_PREDICTIONS_FOR_AGENT_2, NO_OF_STEPS_4
from Agent import Agent
from Predator import Predator
from Prey import Prey
from BiBFS import BidirectionalSearch

# Our Agent 2 simply prefers moving away from the Predator and going closer to Prey and only when that option is also
# exhausted, does it think of keeping its distance equal to the Predator and think of other options.


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
                    return [count, 1]
                self.predator.take_next_move()
                if self.currPos == self.predator.currPos:
                    print("Ded")
                    count += 1
                    return [count, -1]
                count += 1
                continue
            self.currPos = next_move
            self.path.append(next_move)
            if self.currPos == self.prey.currPos:
                print("Yippiieeee")
                count += 1
                return [count, 1]
            elif self.currPos == self.predator.currPos:
                print("Ded")
                count += 1
                return [count, -1]
            # print("Inside Agent",self.graph)
            self.prey.take_next_move(copy.deepcopy(self.graph))
            belief_mat = [0] * NO_OF_NODES
            belief_mat[self.prey.currPos] = 1

            if self.currPos == self.prey.currPos:
                print("Yippiieeee")
                count += 1
                return [count, 1]

            self.predator.take_next_move()

            if self.currPos == self.predator.currPos:
                print("Ded")
                count += 1
                return [count, -1]

            # print("For count = ", count, "###################")
            # print("Agent: ", self.currPos)
            # print("Prey: ", self.prey.currPos)
            # print("Predator", self.predator.currPos)


            count += 1
        return [count, 0]

    def get_next_move(self, belief, transition_matrix):

        no_of_prediction_steps = NO_OF_NEXT_STEP_PREDICTIONS_FOR_AGENT_2

        neighbours = self.graph[self.currPos]
        # To find the distance between neighbours of Agent and Predator
        path_predator = self.find_path(neighbours, self.predator.currPos)
        # To find the distance between neighbours of Agent and Prey
        path_prey = self.find_path(neighbours, self.prey.currPos)

        # print("----Neighbours Path-----")
        # print("Prey",path_prey)
        # print("Predator",path_predator)

        # Current Position to Predator/Prey
        currpos_to_predator = self.find_path([self.currPos], self.predator.currPos)[self.currPos]
        currpos_to_prey = self.find_path([self.currPos], self.prey.currPos)[self.currPos]

        while no_of_prediction_steps >= len(currpos_to_prey):
            no_of_prediction_steps = no_of_prediction_steps - 1

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

        # print("-----Current Position Path-----")
        # print("Prey",currpos_to_prey)
        # print("Predator",currpos_to_predator)

        # The distance between each neighbour of agent and prey/predator
        len_agent_predator = {key: len(value) for key, value in path_predator.items()}
        # len_agent_prey = {key: len(value) for key, value in path_prey.items()}
        len_agent_prey_expected = {key: len(value) for key, value in path_to_prey_expected.items()}

        # Reversing the dictionaries
        # reversed_len_agent_predator = self.reverse_dict(len_agent_predator)
        # reversed_len_agent_prey = self.reverse_dict(len_agent_prey)

        # Max and Min distances tuples in the form : (Neighbour_Number, Distance)
        # min_prey_dist = min(len_agent_prey.items(), key=lambda data: data[1])
        # max_prey_dist = max(len_agent_prey.items(), key=lambda data: data[1])
        # min_predator_dist = min(len_agent_predator.items(), key=lambda data: data[1])
        # max_predator_dist = max(len_agent_predator.items(), key=lambda data: data[1])

        # print(min_prey_dist)
        # print(max_prey_dist)
        # print(min_predator_dist)
        # print(max_predator_dist)

        # Logic for Agent 1

        best_neighbour = []
        # Neighbors that are closer to the Prey and farther from the Predator.
        for i in neighbours:
            # if len_agent_prey[i] < len(currpos_to_prey) and (len_agent_predator[i] > len(currpos_to_predator)):
            if len_agent_prey_expected[i] < len(curr_pos_to_prey_expected) and \
                    (len_agent_predator[i] > len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not farther from the Prey and farther from the Predator.
        for i in neighbours:
            # if len_agent_prey[i] == len(currpos_to_prey) and (len_agent_predator[i] > len(currpos_to_predator)):
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
            # if len_agent_prey[i] < len(currpos_to_prey) and (len_agent_predator[i] == len(currpos_to_predator)):
            if len_agent_prey_expected[i] < len(curr_pos_to_prey_expected) and \
                    (len_agent_predator[i] == len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not farther from the Prey and not closer to the Predator.
        for i in neighbours:
            # if len_agent_prey[i] == len(currpos_to_prey) and (len_agent_predator[i] == len(currpos_to_predator)):
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


    # def reverse_dict(self, mydict):
    #     reversed_dict = {}
    #     for key, value in mydict.items():
    #         reversed_dict.setdefault(value, [])
    #         reversed_dict[value].append(key)
    #     return reversed_dict
