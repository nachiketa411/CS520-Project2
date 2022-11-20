# This is a sample Python script.
import json
from itertools import product
from multiprocessing import Pool, cpu_count

import numpy as np

from Agent1 import Agent1
from Agent2_1 import Agent2_1
from Agent2_2 import Agent2_2
from Agent3 import Agent3
from Agent4_1 import Agent4_1
from Agent5 import Agent5
from Agent6_1 import Agent6_1
from Agent7 import Agent7
from Agent7b import Agent7b
from Agent7c import Agent7c
from Agent8b import Agent8b
from Agent8c import Agent8c
from Agent9 import Agent9
from Agent8 import Agent8

from Constants import ENVIRONMENT_PATH, GRAPH_DIST_PATH
from Graph import Graph
from GraphVisualizer import visualize
from BiBFS import BidirectionalSearch
from Predator import Predator
from Prey import Prey

def simulate_agent(args):
    graph_1, graph_distances = args
    # graph_1 = Graph()
    # visualize(graph_1)

    # graph_1 = converted_graph[k]
    # graph_distances = converted_distances[k]

    transition_matrix = []
    for node in range(len(graph_1)):
        transition_matrix.append([0] * 50)
        neighbours = graph_1[node]
        prob = 1 / (len(neighbours) + 1)
        transition_matrix[node][node] = prob
        for neighbor in neighbours:
            transition_matrix[node][neighbor] = prob

    successRate = 0
    prey = Prey(graph_1)
    predator = Predator(graph_1)

    # change this with each agent
    # agent1 = Agent1(prey, graph_1)
    # agent1 = Agent2_1(prey, graph_1)
    # agent1 = Agent2_2(prey, graph_1)
    # agent1 = Agent3(prey, graph_1)
    # agent1 = Agent4_1(prey, graph_1)
    # agent1 = Agent5(prey, graph_1)
    # agent1 = Agent6_1(prey, graph_1)
    agent1 = Agent7(prey, graph_1)
    # agent1 = Agent7b(prey, graph_1)
    # agent1 = Agent7c(prey, graph_1)
    # agent1 = Agent8(prey, graph_1)
    # agent1 = Agent8b(prey, graph_1)
    # agent1 = Agent8c(prey, graph_1)
    # agent1 = Agent9(prey, graph_1)

    agent1.initialize(predator)
    predator.initialize(agent1)

    # print('Agent location: ', agent1.currPos)
    # for Agents: 1
    # steps_taken = agent1.move_agent()

    # for Agents: 2.1, 4.1
    # steps_taken = agent1.move_agent(transition_matrix, graph_distances)

    # for Agents: 2.2, 3
    # steps_taken = agent1.move_agent(transition_matrix)

    # for Agents: 5, 6
    # steps_taken = agent1.move_agent(graph_distances)

    # for Agent 7, 8 full
    steps_taken = agent1.move_agent(graph_distances, transition_matrix)

    del graph_1

    return steps_taken

# Press the green button in the gutter to run the script.
def main():

    success_of_Agent = 0
    failure_rate_1 = 0
    failure_rate_2 = 0

    # # # ---------------------Write to JSON-------------------
    # # graphs = {}
    # # graph_distance = {}
    # # for k in range(100):
    # #     graph = Graph()
    # #     graphs[k] = graph.graph
    # #     graph_distance[k] = graph.distance_from_each_node
    # #
    # # json_object = json.dumps(graphs, indent=4)
    # # json_object_2 = json.dumps(graph_distance, indent=4)
    # # with open(ENVIRONMENT_PATH, "w") as outfile:
    # #     outfile.write(json_object)
    # #
    # # with open(GRAPH_DIST_PATH, "w") as outfile2:
    # #     outfile2.write(json_object_2)
    # # # ----------------------------------------------------
    #
    # ---------------------Read from JSON-------------------
    with open(ENVIRONMENT_PATH, "r") as env_file:
        json_object = json.load(env_file)

    with open(GRAPH_DIST_PATH, "r") as node_dist:
        json_object_2 = json.load(node_dist)

    converted_graph = {}
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
    all_possible_combinations = product(range(100), range(30))
    all_possible_graph_combs = [(converted_graph[k], converted_distances[k]) for (k, i) in all_possible_combinations]
    with Pool(cpu_count() -1) as p:
        stats = p.map(simulate_agent, all_possible_graph_combs)

    total_sum_of_steps = 0
    total_no_of_times_prey_found_and_WON = 0
    total_no_of_times_prey_found_and_LOST = 0
    total_no_of_times_prey_found_and_HUNG = 0
    total_no_of_times_predator_found_and_WON = 0
    total_no_of_times_predator_found_and_LOST = 0
    total_no_of_times_predator_found_and_HUNG = 0

    for i in range(len(stats)):
        total_sum_of_steps += stats[i][0]

    for i in range(len(stats)):
        if stats[i][1] == -1:
            total_no_of_times_prey_found_and_WON += stats[i][2]
            total_no_of_times_predator_found_and_WON += stats[i][3]

        if stats[i][1] == -2:
            total_no_of_times_prey_found_and_LOST += stats[i][2]
            total_no_of_times_predator_found_and_LOST += stats[i][3]

        if stats[i][1] == -3:
            total_no_of_times_prey_found_and_HUNG += stats[i][2]
            total_no_of_times_predator_found_and_HUNG += stats[i][3]

    avg_steps_taken = total_sum_of_steps / len(stats)
    avg_times_prey_found_and_won = total_no_of_times_prey_found_and_WON / len(stats)
    avg_times_prey_found_and_lost = total_no_of_times_prey_found_and_LOST / len(stats)
    avg_times_prey_found_and_hung = total_no_of_times_prey_found_and_HUNG / len(stats)
    avg_times_predator_found_and_won = total_no_of_times_predator_found_and_WON / len(stats)
    avg_times_predator_found_and_lost = total_no_of_times_predator_found_and_LOST / len(stats)
    avg_times_predator_found_and_hung = total_no_of_times_predator_found_and_HUNG / len(stats)

    print('Average Number of Steps taken: ', avg_steps_taken)

    print('Average Number of Prey found and won: ', avg_times_prey_found_and_won)
    print('Average Number of Prey found and lost: ', avg_times_prey_found_and_lost)
    print('Average Number of Prey found and hung: ', avg_times_prey_found_and_hung)
    print('Average Number of Predator found and won: ', avg_times_predator_found_and_won)
    print('Average Number of Predator found and lost: ', avg_times_predator_found_and_lost)
    print('Average Number of Predator found and hung: ', avg_times_predator_found_and_hung)
    stats = np.array(stats)
    print("Final Success Rate: ", len(np.where(stats == -1)[0]))
    print("Marr Gaya Mai: ", len(np.where(stats == -2)[0]))
    print("Ghoom Gaya Mai: ", len(np.where(stats == -3)[0]))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

main()