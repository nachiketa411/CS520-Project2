import networkx as nx
import matplotlib.pyplot as plt


def visualize(graph_dict):
    print(type(graph_dict))
    temp_graph = nx.DiGraph(graph_dict.graph)
    # nx.draw_networkx(temp_graph)
    # plt.show()
    pos = nx.circular_layout(temp_graph)
    nx.draw(temp_graph, pos=pos, with_labels=True)
    plt.show()