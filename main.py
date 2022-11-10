# This is a sample Python script.
import json

from Agent1 import Agent1
from Agent2 import Agent2
from Agent3 import Agent3
from Constants import ENVIRONMENT_PATH, GRAPH_DIST_PATH
from Graph import Graph
from GraphVisualizer import visualize
from BiBFS import BidirectionalSearch
from Predator import Predator
from Prey import Prey

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    success_of_Agent=0
    failure_rate_1=0
    failure_rate_2=0

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
    # ----------------------------------------------------

    for k in range(1):

        # graph_1 = Graph()
        # visualize(graph_1)

        graph_1 = converted_graph[k]

        transition_matrix=[]
        for i in range(len(graph_1)):
            transition_matrix.append([0]*50)
            neighbours=graph_1[i]
            k=1/(len(neighbours)+1)
            transition_matrix[i][i]=k
            for j in neighbours:
                transition_matrix[i][j]=k
        print("*********************************")

        successRate = 0
        for i in range(1):

            prey = Prey(graph_1)
            predator = Predator(graph_1)
            print('Prey position: ', prey.currPos)
            print('Predator position: ', predator.currPos)
            # agent1 = Agent1(prey, graph_1.graph)
            # agent1 = Agent1(prey, graph_1)

            # change this with each agent
            agent1 = Agent3(prey, graph_1)
            agent1.initialize(predator)

            predator.initialize(agent1)
            print('Agent location: ', agent1.currPos)
            steps_taken = agent1.move_agent(transition_matrix)
            if steps_taken[1] == 1:
                successRate += 1
            if steps_taken[1]==0:
                failure_rate_2+=1
            if steps_taken[1]==-1:
                failure_rate_1+=1
            print("No of steps: ", steps_taken[0])
            print("Agent:", agent1.path)
            print("Prey:",prey.path)
            print("Predator:",predator.path)
            del prey
            del predator
            del agent1
            print("------------------------------------")

        del graph_1
        print("Success Rate for #",k," is: ", successRate)
        success_of_Agent+=successRate

    print("Final Success Rate: ",success_of_Agent)
    print("Marr Gaya Mai: ", failure_rate_1)
    print("Ghoom Gaya Mai: ", failure_rate_2)

    # graph_1 = Graph()
    #
    # prey = Prey(graph_1)
    # predator = Predator(graph_1)
    # print('Prey position: ', prey.currPos)
    # print('Predator position: ', predator.currPos)
    # agent1 = Agent1(prey, graph_1.graph)
    # agent1.initialize(predator)
    #
    # # change this with each agent
    # predator.initialize(agent1)
    # print('Agent location: ', agent1.currPos)
    # steps_taken = agent1.move_agent()
    # print("No of steps: ", steps_taken[0])
    #
    # print("Agent:", agent1.path)
    # print("Prey:",prey.path)
    # print("Predator:",predator.path)
    #
    #
    # visualize(graph_1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
