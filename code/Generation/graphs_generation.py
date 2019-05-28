import networkx as nx
from random import choice

from Simulation.SimulationGraph import SimulationGraph


def connected_gnp_graph(n: int, completion: float = 0.5) -> SimulationGraph:
    """
    Generates a random simulation graph with n nodes, where every edge from complete graph is added with givem probability
    :param n: number of nodes
    :param completion: edge creation probability
    :return: generated SimulationGraph
    """
    G = nx.fast_gnp_random_graph(n, completion)
    components = [list(component) for component in nx.connected_components(G)]

    for comp_a, comp_b in zip(components[1:], components[:-1]):
        e = (choice(comp_a), choice(comp_b))
        G.add_edge(*e)

    return SimulationGraph(G)


def barabasi_albert_graph(n: int, m: int) -> SimulationGraph:
    """
    Generates a random simulation graph according to the Barabási–Albert preferential attachment model
    :param n: number of nodes
    :param m: number of edges to attach from new node to existing node
    :return: Generated SimulationGraph
    """
    return SimulationGraph(nx.barabasi_albert_graph(n, m))


