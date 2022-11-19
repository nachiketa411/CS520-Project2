# This is a sample Python script.
import json

from Agent1 import Agent1
from Agent2_1 import Agent2_1
from Agent2_2 import Agent2_2
from Agent3 import Agent3
from Agent4_1 import Agent4_1
from Agent5 import Agent5
from Agent7 import Agent7

from Constants import ENVIRONMENT_PATH, GRAPH_DIST_PATH
from Graph import Graph
from GraphVisualizer import visualize
from BiBFS import BidirectionalSearch
from Predator import Predator
from Prey import Prey

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    success_of_Agent = 0
    failure_rate_1 = 0
    failure_rate_2 = 0

    # # ---------------------Write to JSON-------------------
    # graphs = {}
    # graph_distance = {}
    # for k in range(100):
    #     graph = Graph()
    #     graphs[k] = graph.graph
    #     graph_distance[k] = graph.distance_from_each_node
    #
    # json_object = json.dumps(graphs, indent=4)
    # json_object_2 = json.dumps(graph_distance, indent=4)
    # with open(ENVIRONMENT_PATH, "w") as outfile:
    #     outfile.write(json_object)
    #
    # with open(GRAPH_DIST_PATH, "w") as outfile2:
    #     outfile2.write(json_object_2)
    # # ----------------------------------------------------

    # ---------------------Read from JSON-------------------
    with open(ENVIRONMENT_PATH, "r") as env_file:
        json_object = json.load(env_file)

    with open(GRAPH_DIST_PATH, "r") as node_dist:
        json_object_2 = json.load(node_dist)

    # print(json_object)
    # print(json_object.items())
    # convertedGraph = {int(k): [int(i) for i in v] for k, v in json_object.items()}
    converted_graph = {}
    print(json_object)
    for g_id in json_object.items():
        graph_id = int(g_id[0])
        graph = {}
        for k in g_id[1]:
            graph[int(k)] = g_id[1][k]
        converted_graph[graph_id] = graph

    converted_distances = {}
    for g_id in json_object_2.items():
        graph_id = int(g_id[0])
        distance_mat=[]
        for j in g_id[1].items():
            temp = []
            for k in j[1].items():
                temp.append(int(k[1]))
            distance_mat.append(temp)
        converted_distances[graph_id] = distance_mat

    # ----------------------------------------------------

    for k in range(100):
        # graph_1 = Graph()
        # visualize(graph_1)

        graph_1 = converted_graph[k]
        graph_distances = converted_distances[k]
        print('Graph Distances: ', graph_distances)

        transition_matrix = []
        for i in range(len(graph_1)):
            transition_matrix.append([0] * 50)
            neighbours = graph_1[i]
            k = 1 / (len(neighbours) + 1)
            transition_matrix[i][i] = k
            for j in neighbours:
                transition_matrix[i][j] = k
        print("*********************************")

        successRate = 0
        for i in range(30):

            prey = Prey(graph_1)
            predator = Predator(graph_1)
            print('Prey position: ', prey.currPos)
            print('Predator position: ', predator.currPos)

            # change this with each agent
            # agent1 = Agent1(prey, graph_1)
            # agent1 = Agent2_1(prey, graph_1)
            # agent1 = Agent2_2(prey, graph_1)
            # agent1 = Agent3(prey, graph_1)
            # agent1 = Agent4_1(prey, graph_1)
            # agent1 = Agent5(prey, graph_1)
            agent1 = Agent7(prey, graph_1)
            agent1.initialize(predator)
            predator.initialize(agent1)

            print('Agent location: ', agent1.currPos)
            # for Agents: 1
            # steps_taken = agent1.move_agent()

            # for Agents: 2.1, 4.1
            #steps_taken = agent1.move_agent(transition_matrix, graph_distances)

            # for Agents: 2.2, 3
            # steps_taken = agent1.move_agent(transition_matrix)

            # for Agents: 5
            # steps_taken = agent1.move_agent(graph_distances)

            # for Agents: 5
            print("Main me: ",transition_matrix)
            steps_taken = agent1.move_agent(graph_distances, transition_matrix)
            if steps_taken[1] == 1:
                successRate += 1
            if steps_taken[1] == 0:
                failure_rate_2 += 1
            if steps_taken[1] == -1:
                failure_rate_1 += 1
            print("No of steps: ", steps_taken[0])
            print("Agent:", agent1.path)
            print("Prey:", prey.path)
            print("Predator:", predator.path)
            del prey
            del predator
            del agent1
            print("------------------------------------")

        del graph_1
        print("Success Rate for #", k, " is: ", successRate)
        success_of_Agent += successRate

    print("Final Success Rate: ", success_of_Agent)
    print("Marr Gaya Mai: ", failure_rate_1)
    print("Ghoom Gaya Mai: ", failure_rate_2)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
