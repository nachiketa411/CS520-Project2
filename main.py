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

    print("*********************************")

    successRate=0
    for i in range(10):
        prey = Prey(graph_1)
        predator = Predator(graph_1)
        print('Prey position: ', prey.currPos)
        print('Predator position: ', predator.currPos)
        agent1 = Agent1(prey, graph_1.graph)
        agent1.initialize(predator)

        # change this with each agent
        predator.initialize(agent1)
        print('Agent location: ', agent1.currPos)
        steps_taken = agent1.move_agent()
        if steps_taken[1]==1:
            successRate+=1
        print("No of steps: ",steps_taken[0])
        print("------------------------------------")

    print("Success Rate is: ",successRate)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
