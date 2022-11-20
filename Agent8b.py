import copy
import random

from Constants import NO_OF_STEPS_1, NO_OF_NODES, NO_OF_STEPS_4
from Agent import Agent
from Predator import Predator
from Prey import Prey
from BiBFS import BidirectionalSearch


class Agent8b(Agent):

    def move_agent(self, dist_dict, transition_mat):
        # Return 1 for Success, -1 when predator catches the Agent and 0 when counter exhausts
        belief_mat_predator = [0] * NO_OF_NODES
        belief_mat_prey = [1 / 49] * NO_OF_NODES
        belief_mat_predator[self.predator.currPos] = 1
        belief_mat_prey[self.currPos] = 0

        count = 0

        while count <= NO_OF_STEPS_4:

            # Check if Agent knows where the predator is:
            if 1 in belief_mat_predator:
                # Choose a node to survey for the prey
                to_survey = self.select_node_prey(belief_mat_prey)
                belief_mat_prey = self.update_belief_after_survey(belief_mat_prey, to_survey, self.prey.currPos)
            else:
                # Choose a node to survey to find the predator
                to_survey = self.select_node_predator(belief_mat_predator, dist_dict)
                belief_mat_predator = self.update_belief_after_survey(belief_mat_predator, to_survey, self.predator.currPos)

            # Selecting a node with the highest probability and moving towards it.
            predicted_pred_pos = self.select_node_predator(belief_mat_predator, dist_dict)
            predicted_prey_pos = self.select_node_prey(belief_mat_prey)

            expected_distance_for_prey = self.get_expected_distance_of_prey_from_agent(
                belief_mat_prey.copy(), transition_mat.copy(), self.currPos, predicted_prey_pos, dist_dict)
            expected_distance_for_predator = self.get_expected_distance_of_predator_from_agent(
                belief_mat_predator.copy(), self.currPos, dist_dict)

            next_move = self.get_next_move(
                predicted_pred_pos, predicted_prey_pos, expected_distance_for_prey, expected_distance_for_predator)

            # When Agent Chooses to stay in its position
            if next_move == -1:

                self.prey.take_next_move(copy.deepcopy(self.graph))

                # What if prey accidentally ends up in the Agent's location?
                if self.currPos == self.prey.currPos:
                    count += 1
                    print("Yippiieeee")
                    return [count, 1]
                belief_mat_prey = self.update_belief_using_transition_mat(belief_mat_prey, transition_mat)

                # Predator moves closer to Agent with a probability of 0.6
                decision = random.uniform(0, 1)
                if decision < 0.6:
                    self.predator.take_next_move()
                else:
                    self.predator.currPos = random.choice(self.graph[self.predator.currPos])
                    self.predator.path.append(self.predator.currPos)
                # belief_mat_predator = self.update_belief_using_distance_dic(belief_mat_predator, dist_dict)
                belief_mat_predator = self.update_belief_after_distracted_predator_moves(belief_mat_predator,
                                                                                         self.currPos)
                if self.currPos == self.predator.currPos:
                    print("Ded")
                    return [count, -1]

                count += 1
                continue

            self.currPos = next_move
            self.path.append(next_move)

            # Checks if Prey is in current position
            if self.currPos == self.prey.currPos:
                print("Yippiieeee")
                count += 1
                return [count, 1]

            # Check if Predator is in current position
            if self.currPos == self.predator.currPos:
                print("Ded")
                count += 1
                return [count, -1]

            belief_mat_prey = self.update_belief_after_agent_moves(belief_mat_prey, next_move, self.prey.currPos)
            belief_mat_predator = self.update_belief_after_agent_moves(belief_mat_predator, next_move, self.predator.currPos)

            self.prey.take_next_move(copy.deepcopy(self.graph))
            if self.currPos == self.prey.currPos:
                print("Yippiieeee")
                count += 1
                return [count, 1]

            # Predator moves closer to prey with a probability of 0.6
            decision = random.uniform(0, 1)
            if decision < 0.6:
                self.predator.take_next_move()
            else:
                self.predator.currPos = random.choice(self.graph[self.predator.currPos])
                self.predator.path.append(self.predator.currPos)

            if self.currPos == self.predator.currPos:
                print("Ded")
                count += 1
                return [count, -1]

            belief_mat_prey = self.update_belief_using_transition_mat(belief_mat_prey, transition_mat)
            # belief_mat_predator = self.update_belief_using_distance_dic(belief_mat_predator, dist_dict)
            belief_mat_predator = self.update_belief_after_distracted_predator_moves(belief_mat_predator,
                                                                                     self.currPos)

            count += 1
        return [count, 0]

    def get_next_move(self, pred_pos, prey_pos, expected_distance_for_prey, expected_distance_for_predator):
        neighbours = self.graph[self.currPos]
        # To find the distance between neighbours of Agent and Predator
        path_predator = self.find_path(neighbours, pred_pos)
        # To find the distance between neighbours of Agent and Prey
        path_prey = self.find_path(neighbours, prey_pos)

        # Current Position to Predator/Prey
        currpos_to_predator = self.find_path([self.currPos], pred_pos)[self.currPos]
        currpos_to_prey = self.find_path([self.currPos], prey_pos)[self.currPos]

        # The distance between each neighbour of agent and prey/predator
        len_agent_predator = {key: len(value) for key, value in path_predator.items()}
        len_agent_prey = {key: len(value) for key, value in path_prey.items()}

        # Logic for Agent 1

        best_neighbour = []
        # Neighbors that are closer to the Prey and farther from the Predator.
        for i in neighbours:
            if (expected_distance_for_prey[i] < len(currpos_to_prey) and (len_agent_predator[i] > len(currpos_to_predator))) or \
                    (len_agent_prey[i] < len(currpos_to_prey) and (expected_distance_for_predator[i] > len(currpos_to_predator))):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are closer to the Prey and not closer to the Predator.
        for i in neighbours:
            if (expected_distance_for_prey[i] < len(currpos_to_prey) and (len_agent_predator[i] == len(currpos_to_predator))) or \
                    (len_agent_prey[i] < len(currpos_to_prey) and (expected_distance_for_predator[i] == len(currpos_to_predator))):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not farther from the Prey and farther from the Predator.
        for i in neighbours:
            if (expected_distance_for_prey[i] == len(currpos_to_prey) and (len_agent_predator[i] > len(currpos_to_predator))) or \
                    (len_agent_prey[i] == len(currpos_to_prey) and (expected_distance_for_predator[i] > len(currpos_to_predator))):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not farther from the Prey and not closer to the Predator.
        for i in neighbours:
            if (expected_distance_for_prey[i] == len(currpos_to_prey) and (len_agent_predator[i] == len(currpos_to_predator))) or \
                    (len_agent_prey[i] == len(currpos_to_prey) and (expected_distance_for_predator[i] == len(currpos_to_predator))):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are farther from the Predator.
        for i in neighbours:
            if (expected_distance_for_predator[i] > len(currpos_to_predator)) or (len_agent_predator[i] > len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not closer to the Predator.
        for i in neighbours:
            if (expected_distance_for_predator[i] == len(currpos_to_predator)) or (len_agent_predator[i] == len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Sit still and pray.
        return -1

    def select_node_predator(self, belief_mat, dist_dict):
        # Maximum probability of finding a predator
        max_in_belief_mat = max(belief_mat)
        possible_nodes = []
        for i in range(len(belief_mat)):
            if belief_mat[i] == max_in_belief_mat:
                possible_nodes.append(i)
        # Breaking ties, first based on proximity, then at random
        if len(possible_nodes) > 1:
            temp = {}
            for i in possible_nodes:
                temp[i] = dist_dict[i][self.currPos]
            ties = {}
            for i in temp.items():
                if i[1] not in ties:
                    ties[i[1]] = []
                ties[i[1]].append(i[0])
            return random.choice(ties[min(ties)])
        else:
            return possible_nodes[0]

    def select_node_prey(self, belief_mat):
        max_in_belief_mat = max(belief_mat)
        possible_nodes = []
        # print("Inside ",belief_mat,self.currPos,max_in_belief_mat)
        for i in range(len(belief_mat)):
            if belief_mat[i] == max_in_belief_mat:
                possible_nodes.append(i)
        if possible_nodes:
            return random.choice(possible_nodes)
        else:
            return -1

    def update_belief_after_survey(self, belief_mat, node, player):
        if node == player:
            decision=random.uniform(0,1)
            if decision>0.1:
                belief_mat = [0] * 50
                belief_mat[node] = 1
                return belief_mat
        temp = 1 - belief_mat[node]
        belief_mat[node] = 0
        for i in range(len(belief_mat)):
            belief_mat[i] = belief_mat[i] / temp
        return belief_mat

    def update_belief_after_agent_moves(self, belief_mat, node, player):
        if node == player:
            belief_mat = [0] * NO_OF_NODES
            belief_mat[node] = 1
        else:
            temp = 1 - belief_mat[node]
            belief_mat[node] = 0
            for i in range(len(belief_mat)):
                belief_mat[i] = belief_mat[i] / temp
        return belief_mat

    def update_belief_using_transition_mat(self, belief_mat, transition_mat):
        new_belief_mat = [0] * NO_OF_NODES
        for i in range(len(belief_mat)):
            # P(Prey in i)= Summation(P(Prey in neighbour of i)*P(Prey in neighbour of i|Prey in i))
            summation = 0
            for j in range(len(transition_mat[i])):
                summation += (belief_mat[j] * transition_mat[j][i])
            new_belief_mat[i] = summation
        return new_belief_mat

    def update_belief_using_distance_dic(self, belief_mat, dist_dict):
        new_belief_mat = [0] * NO_OF_NODES

        # Transition probabilities of each node based on the current position of Agent
        transition_probabilities = {}
        for i in range(len(belief_mat)):
            transition_probabilities[i] = self.neighbours_order(i, dist_dict)

        for i in range(len(belief_mat)):
            summation = 0
            for j in self.graph[i]:
                summation += (belief_mat[j] * transition_probabilities[j][i])
            new_belief_mat[i] = summation
        return new_belief_mat

