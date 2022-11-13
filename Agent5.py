import copy
import random

from Constants import NO_OF_STEPS_1, NO_OF_NODES
from Agent import Agent
from Predator import Predator
from Prey import Prey
from BiBFS import BidirectionalSearch


class Agent5(Agent):

    def move_agent(self, dist_dict):
        # Return 1 for Success, -1 when predator catches the Agent and 0 when counter exhausts

        belief_mat = [0] * NO_OF_NODES
        belief_mat[self.predator.currPos] = 1

        count = 0

        while count <= NO_OF_STEPS_1:

            print(count)
            # Selecting a node to survey.
            to_survey = self.select_node(belief_mat, dist_dict)

            # Survey the selected Node and update the belief matrix
            belief_mat = self.update_belief(belief_mat, to_survey)

            print("After Survey:", sum(belief_mat))

            # Selecting a node with the highest probability and moving towards it.
            predicted_pred_pos = self.select_node(belief_mat, dist_dict)
            next_move = self.get_next_move(predicted_pred_pos)

            # When Agent Chooses to stay in its position
            if next_move == -1:
                self.prey.take_next_move(copy.deepcopy(self.graph))

                # What if prey accidentally ends up in the Agent's location?
                if self.currPos == self.prey.currPos:
                    count += 1
                    print("Yippiieeee")
                    return [count, 1]
                print("Agent Chose to not move: ", sum(belief_mat))

                self.predator.take_next_move()
                belief_mat = self.update_belief_using_transition_mat(belief_mat, dist_dict)
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

            belief_mat = self.update_belief_using_transition_mat(belief_mat, dist_dict)
            print("After prey moved", sum(belief_mat))

            count += 1
        return [count, 0]

    def get_next_move(self, pred_pos):
        neighbours = self.graph[self.currPos]
        # To find the distance between neighbours of Agent and Predator
        path_predator = self.find_path(neighbours, pred_pos)
        # To find the distance between neighbours of Agent and Prey
        path_prey = self.find_path(neighbours, self.prey.currPos)

        # Current Position to Predator/Prey
        currpos_to_predator = self.find_path([self.currPos], pred_pos)[self.currPos]
        currpos_to_prey = self.find_path([self.currPos], self.prey.currPos)[self.currPos]

        # The distance between each neighbour of agent and prey/predator
        len_agent_predator = {key: len(value) for key, value in path_predator.items()}
        len_agent_prey = {key: len(value) for key, value in path_prey.items()}

        # Logic for Agent 1

        best_neighbour = []
        # Neighbors that are closer to the Prey and farther from the Predator.
        for i in neighbours:
            if len_agent_prey[i] < len(currpos_to_prey) and (len_agent_predator[i] > len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are closer to the Prey and not closer to the Predator.
        for i in neighbours:
            if len_agent_prey[i] < len(currpos_to_prey) and (len_agent_predator[i] == len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not farther from the Prey and farther from the Predator.
        for i in neighbours:
            if len_agent_prey[i] == len(currpos_to_prey) and (len_agent_predator[i] > len(currpos_to_predator)):
                best_neighbour.append(i)

        if best_neighbour:
            return random.choice(best_neighbour)

        # Neighbors that are not farther from the Prey and not closer to the Predator.
        for i in neighbours:
            if len_agent_prey[i] == len(currpos_to_prey) and (len_agent_predator[i] == len(currpos_to_predator)):
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

    def select_node(self, belief_mat, dist_dict):
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

    def update_belief(self, belief_mat, node):
        if node == self.predator.currPos:
            belief_mat = [0] * 50
            belief_mat[node] = 1
        else:
            temp = 1 - belief_mat[node]
            belief_mat[node] = 0
            for i in range(len(belief_mat)):
                belief_mat[i] = belief_mat[i] / temp
        return belief_mat

    def update_belief_using_transition_mat(self, belief_mat, dist_dict):
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
