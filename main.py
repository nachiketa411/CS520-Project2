# This is a sample Python script.

from Agent1 import Agent1
from Graph import Graph
from GraphVisualizer import visualize
from BiBFS import BidirectionalSearch
from Predator import Predator
from Prey import Prey

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    graph_1 = Graph()
    visualize(graph_1)

    prey = Prey(graph_1)
    predator = Predator(graph_1)
    print('Prey position: ', prey.currPos)
    agent1 = Agent1(prey, graph_1.graph)
    agent1.initialize(predator)

    # change this with each agent
    predator.initialize(agent1)
    print('Agent location: ', agent1.currPos)
    print('Prey location: ', agent1.prey.currPos)
    print('Predator Object agent location: ', agent1.predator.currPos)

    prey.take_next_move(graph_1)
    print('Updated Prey location: ', agent1.prey.currPos)

    predator.take_next_move()

    agent1.move_agent()
    agent1.take_next_move()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
