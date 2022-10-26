import random
import networkx as nx

from Constants import NO_OF_NODES


class Graph:
    def __init__(self):
        self.graph = {}
        self.generate_graph(NO_OF_NODES)

    def generate_graph(self, no_of_nodes):
        for i in range(no_of_nodes):
            # this will create a circular graph
            if i == 0:
                self.graph[i] = [no_of_nodes - 1, i + 1]
            elif i == no_of_nodes - 1:
                self.graph[i] = [i - 1, 0]
            else:
                self.graph[i] = [i - 1 % no_of_nodes, i + 1 % no_of_nodes]
        # we need to add the remaining edges according to the conditions given for the environment
        set_of_nodes_with_degree_2 = set(self.graph.keys())
        print('degree 2: ', set_of_nodes_with_degree_2)
        while len(set_of_nodes_with_degree_2) > 0:
            random_node_choice = random.choice(list(set_of_nodes_with_degree_2))
            list_of_possible_connections = [random_node_choice - 2 % no_of_nodes, random_node_choice - 3 % no_of_nodes,
                                            random_node_choice - 4 % no_of_nodes, random_node_choice - 5 % no_of_nodes,
                                            random_node_choice + 2 % no_of_nodes, random_node_choice + 3 % no_of_nodes,
                                            random_node_choice + 4 % no_of_nodes, random_node_choice + 5 % no_of_nodes]

            print('list_of_possible_connections: ', list_of_possible_connections)
            # filter out invalid points i.e. points which are not in the set anymore
            filtered_list = list(filter(lambda a: a in set_of_nodes_with_degree_2, list_of_possible_connections))
            print('filtered_list: ', filtered_list)
            if len(filtered_list) == 0:
                print(self.graph)
                return self.graph
            random_node_connection_choice = random.choice(filtered_list)
            self.graph[random_node_choice].append(random_node_connection_choice)
            self.graph[random_node_connection_choice].append(random_node_choice)
            set_of_nodes_with_degree_2.remove(random_node_choice)
            set_of_nodes_with_degree_2.remove(random_node_connection_choice)
            print('Updated degree 2: ', set_of_nodes_with_degree_2)
