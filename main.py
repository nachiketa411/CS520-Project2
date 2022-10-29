# This is a sample Python script.
from Graph import Graph
from GraphVisualizer import visualize
from BiBFS import BidirectionalSearch



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    graph_1 = Graph()

    temp=BidirectionalSearch(graph_1.graph)
    out=temp.bidirectional_search(49,32)
    print(out)
    visualize(graph_1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
