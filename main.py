# This is a sample Python script.

from Agent1 import Agent1
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

    for k in range(100):

        graph_1 = Graph()
        #visualize(graph_1)
        print("*********************************")

        successRate = 0
        for i in range(30):

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
    print("Marr Gaya Mai: ",failure_rate_1)
    print("Ghoom Gaya Mai: ",failure_rate_2)

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
