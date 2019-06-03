from Simulation.initialize_simulation import *
from Simulation.initialize_logger import initialize_logger
from graph_utils import *
from Simulation.InformationSource import *
from Generation.graphs_generation import *

import sys


def get_test_graph(test_id):
    graph = None
    group_pred_info_1 = []
    group_pred_info_2 = []
    group_pred_info_neutral = []

    if test_id == "1":
        graph = SimulationGraph.SimulationGraph()
        graph.add_bidirectional_edge(0, 1, 0)
        graph.add_bidirectional_edge(1, 2, 0)
        graph.add_bidirectional_edge(2, 0, 0)
        group_pred_info_1 = [0]
        group_pred_info_2 = [1]
        group_pred_info_neutral = [2]
    if test_id == "2":
        graph = SimulationGraph.SimulationGraph()
        graph.add_bidirectional_edge(0, 1, 0)
        graph.add_bidirectional_edge(1, 2, 0)
        graph.add_bidirectional_edge(2, 0, 0)
        group_pred_info_1 = [0]
        group_pred_info_2 = [1]
    if test_id == "3":
        graph = SimulationGraph.SimulationGraph()
        graph.add_bidirectional_edge(0, 1, 0)
        graph.add_bidirectional_edge(1, 2, 0)
        graph.add_bidirectional_edge(2, 0, 0)
        group_pred_info_1 = [0, 1]
        group_pred_info_2 = [2]
    if test_id == "4":
        graph, (group_pred_info_1, group_pred_info_2, group_pred_info_neutral) = groups_graph([4, 4, 4], 1, 2)
    if test_id == "5":
        graph, (group_pred_info_1, group_pred_info_2, _) = groups_graph([4, 4, 4], 1, 2)
    if test_id == "6":
        graph, (group_pred_info_1, group_pred_info_2) = groups_graph([4, 4], 1, 2)
    if test_id == "7":
        graph, (group_pred_info_1, group_pred_info_2) = groups_graph([8, 4], 1, 2)
    if test_id == "8":
        graph, (group_pred_info_1, group_pred_info_2, e) = groups_graph([4, 4, 1], 1, 0)

        graph.add_bidirectional_edge(choice(group_pred_info_1), e[0], 0)
        graph.add_bidirectional_edge(choice(group_pred_info_1), e[0], 0)
        graph.add_bidirectional_edge(choice(group_pred_info_2), e[0], 0)
        graph.add_bidirectional_edge(choice(group_pred_info_2), e[0], 0)

    for g in group_pred_info_1:
        graph.set_information_source(g, PredefinedInformationSource('..\\data\\sentence.txt'))
    for g in group_pred_info_2:
        graph.set_information_source(g, PredefinedInformationSource('..\\data\\opposite.txt'))
    for g in group_pred_info_neutral:
        graph.set_information_source(g, PredefinedInformationSource('..\\data\\neutral.txt'))

    return graph


def main():
    if len(sys.argv) != 2:
        print("Invalid number of arguments, expected test id")
        exit(1)

    graph = get_test_graph(sys.argv[1])

    if not graph:
        print("Invalid test id")
        exit(2)

    initialize_simulation(graph)
    plot_graph_live(graph, 1)


if __name__ == "__main__":
    main()
