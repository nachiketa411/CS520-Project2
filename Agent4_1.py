import copy

from Agent import Agent
import random

from BiBFS import BidirectionalSearch
from Constants import NO_OF_NODES, NO_OF_STEPS_4


class Agent4_1(Agent):
    def move_agent(self, trans_mat, graph_distances):

        # Creating a belief List
        belief_mat = [1 / (NO_OF_NODES - 1)] * NO_OF_NODES
        belief_mat[self.currPos] = 0

        count = 0

        while count <= NO_OF_STEPS_4:
            if 1 in belief_mat:
                self.counter_for_prey_actually_found = self.counter_for_prey_actually_found + 1

            # Selecting a node to survey.
            to_survey = self.select_node(belief_mat)

            # Survey the selected Node and update the belief matrix
            belief_mat = self.update_belief(belief_mat, to_survey)

            # Selecting a node with the highest probability and moving towards it.
            to_move = self.select_node(belief_mat)

            expected_distance = self.get_expected_distance_of_prey_from_agent(belief_mat.copy(), trans_mat.copy(),
                                                                              self.currPos, to_move, graph_distances)

            next_move = self.get_next_move(to_move, expected_distance)

            # When Agent Chooses to stay in its position
            if next_move == -1:
                self.prey.take_next_move(copy.deepcopy(self.graph))

                # What if prey accidentally ends up in the Agent's location?
                if self.currPos == self.prey.currPos:
                    count += 1
                    print("Yippiieeee")
                    return [count, -1, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]

                belief_mat = self.update_belief_using_transition_mat(belief_mat, trans_mat)

                self.predator.take_next_move()
                if self.currPos == self.predator.currPos:
                    print("Ded")
                    return [count, -2, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]

                count += 1
                continue

            self.currPos = next_move
            self.path.append(next_move)

            # Check if prey is where you moved.
            belief_mat = self.update_belief(belief_mat, next_move)

            # Checks if Prey is in current position
            if belief_mat[next_move] == 1:
                print("Yippiieeee")
                count += 1
                return [count, -1, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]

            self.prey.take_next_move(copy.deepcopy(self.graph))
            self.predator.take_next_move()

            if self.currPos == self.prey.currPos:
                print("Yippiieeee")
                count += 1
                return [count, -1, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]
            elif self.currPos == self.predator.currPos:
                print("Ded")
                count += 1
                return [count, -2, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]

            belief_mat = self.update_belief_using_transition_mat(belief_mat, trans_mat)

            count += 1
        return [count, -3, self.counter_for_prey_actually_found, self.counter_for_predator_actually_found]

    def get_next_move(self, to_survey_prey, expected_distance):
        neighbours = self.graph[self.currPos]
        # To find the distance between neighbours of Agent and Predator
        path_predator = self.find_path(neighbours, self.predator.currPos)
        # To find the distance between neighbours of Agent and Prey
        path_prey = self.find_path(neighbours, to_survey_prey)

        # Current Position to Predator/Prey
        currpos_to_predator = self.find_path([self.currPos], self.predator.currPos)[self.currPos]
        currpos_to_prey = self.find_path([self.currPos], to_survey_prey)[self.currPos]

        # The distance between each neighbour of agent and prey/predator
        len_agent_predator = {key: len(value) for key, value in path_predator.items()}
        # len_agent_prey = {key: len(value) for key, value in path_prey.items()}

        # Logic for Agent 3

        best_neighbour = []
        # Neighbors that are closer to the Prey and farther from the Predator.
        for i in neighbours:
            if expected_distance[i] < len(currpos_to_prey) and (len_agent_predator[i] > len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are closer to the Prey and not closer to the Predator.
        for i in neighbours:
            if expected_distance[i] < len(currpos_to_prey) and (len_agent_predator[i] == len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not farther from the Prey and farther from the Predator.
        for i in neighbours:
            if expected_distance[i] == len(currpos_to_prey) and (len_agent_predator[i] > len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not farther from the Prey and not closer to the Predator.
        for i in neighbours:
            if expected_distance[i] == len(currpos_to_prey) and (len_agent_predator[i] == len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are farther from the Predator.
        for i in neighbours:
            if len_agent_predator[i] > len(currpos_to_predator):
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


    def select_node(self, belief_mat):
        max_in_belief_mat = max(belief_mat)
        possible_nodes = []
        for i in range(len(belief_mat)):
            if belief_mat[i] == max_in_belief_mat:
                possible_nodes.append(i)
        if possible_nodes:
            return random.choice(possible_nodes)
        else:
            return -1

    def update_belief(self, belief_mat, node):
        if node == self.prey.currPos:
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