import copy
import random
from Constants import NO_OF_STEPS_1, NO_OF_NODES
from Agent import Agent
from BiBFS import BidirectionalSearch


class Agent3(Agent):

    def move_agent(self, trans_mat):

        # Creating a belief List
        belief_mat = [1 / 49] * NO_OF_NODES
        belief_mat[self.currPos] = 0

        count = 0

        while count <= NO_OF_STEPS_1:

            # Selecting a node to survey.
            to_survey = self.select_node(belief_mat)

            # Survey the selected Node and update the belief matrix
            belief_mat = self.update_belief(belief_mat, to_survey)

            print("After Survey:", sum(belief_mat))

            # Selecting a node with the highest probability and moving towards it.
            to_move = self.select_node(belief_mat)
            next_move = self.get_next_move(to_move)

            # When Agent Chooses to stay in its position
            if next_move == -1:
                self.prey.take_next_move(copy.deepcopy(self.graph))

                # What if prey accidentally ends up in the Agent's location?
                if self.currPos == self.prey.currPos:
                    count += 1
                    print("Yippiieeee")
                    return [count, 1]

                # *********Write something here belief update***************

                self.predator.take_next_move()
                if self.currPos == self.predator.currPos:
                    print("Ded")
                    return [count, -1]

                count += 1
                continue

            self.currPos = next_move
            self.path.append(next_move)

            # Check if prey is where you moved.
            belief_mat = self.update_belief(belief_mat, next_move)
            if belief_mat[next_move] == 1:
                print("Yippiieeee")
                count += 1
                return [count, 1]

            # print("Inside Agent",self.graph)
            self.prey.take_next_move(copy.deepcopy(self.graph))
            self.predator.take_next_move()

            if self.currPos == self.prey.currPos:
                print("Yippiieeee")
                count += 1
                return [count, 1]
            elif self.currPos == self.predator.currPos:
                print("Ded")
                count += 1
                return [count, -1]

            # Update belief Matrix As per Transition Matrix of Prey below.

            count += 1
        return [count, 0]

    def get_next_move(self, to_survey_prey):
        neighbours = self.graph[self.currPos]
        # To find the distance between neighbours of Agent and Predator
        path_predator = self.find_path(neighbours, self.predator.currPos)
        # To find the distance between neighbours of Agent and Prey
        path_prey = self.find_path(neighbours, to_survey_prey)

        # print("----Neighbours Path-----")
        # print("Prey",path_prey)
        # print("Predator",path_predator)

        # Current Position to Predator/Prey
        currpos_to_predator = self.find_path([self.currPos], self.predator.currPos)[self.currPos]
        currpos_to_prey = self.find_path([self.currPos], to_survey_prey)[self.currPos]

        # print("-----Current Position Path-----")
        # print("Prey",currpos_to_prey)
        # print("Predator",currpos_to_predator)

        # The distance between each neighbour of agent and prey/predator
        len_agent_predator = {key: len(value) for key, value in path_predator.items()}
        len_agent_prey = {key: len(value) for key, value in path_prey.items()}

        # Logic for Agent 3

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

    def select_node(self, belief_mat):
        while True:
            max_in_belief_mat = max(belief_mat)
            possible_nodes = []
            for i in belief_mat:
                if belief_mat[i] == max_in_belief_mat:
                    possible_nodes.append(i)
            to_survey = random.choice(possible_nodes)
            if to_survey != self.currPos and len(to_survey) != 0:
                return to_survey

    def update_belief(self, belief_mat, node):
        if node == self.prey.currPos:
            belief_mat = [0] * 50
            belief_mat[node] = 1
        else:
            temp = 1 - belief_mat[node]
            belief_mat[node] = 0
            for i in belief_mat:
                belief_mat[i] = belief_mat[i] / temp
        return belief_mat
