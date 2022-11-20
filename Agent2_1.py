import copy
import random

from Constants import NO_OF_STEPS_1, NO_OF_NODES, NO_OF_STEPS_4
from Agent import Agent
from Predator import Predator
from Prey import Prey
from BiBFS import BidirectionalSearch


class Agent2_1(Agent):

    def move_agent(self, trans_mat, graph_distances):

        # Creating a belief List
        belief_mat = [0] * NO_OF_NODES
        belief_mat[self.prey.currPos] = 1

        # Return 1 for Success, -1 when predator catches the Agent and 0 when counter exhausts
        count = 0
        while count <= NO_OF_STEPS_4:

            expected_distance = self.get_expected_distance_of_prey_from_agent(belief_mat, trans_mat, self.currPos,
                                                                              self.prey.currPos, graph_distances)

            next_move = self.get_next_move(expected_distance)
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

            count += 1
        return [count, 0]

    def get_next_move(self, expected_distance):

        neighbours = self.graph[self.currPos]
        # To find the distance between neighbours of Agent and Predator
        path_predator = self.find_path(neighbours, self.predator.currPos)
        # To find the distance between neighbours of Agent and Prey
        path_prey = self.find_path(neighbours, self.prey.currPos)

        # Current Position to Predator/Prey
        currpos_to_predator = self.find_path([self.currPos], self.predator.currPos)[self.currPos]
        currpos_to_prey = self.find_path([self.currPos], self.prey.currPos)[self.currPos]

        # The distance between each neighbour of agent and prey/predator
        len_agent_predator = {key: len(value) for key, value in path_predator.items()}

        # Logic for Agent 1
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
