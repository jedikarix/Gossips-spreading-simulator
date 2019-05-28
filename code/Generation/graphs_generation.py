import networkx as nx
from random import choice
import numpy as np

from Simulation.SimulationGraph import SimulationGraph


def add_random_sources(G, sources, sources_prob):
    if len(sources) != len(sources_prob):
        raise ValueError(f"Length of sources ({len(sources)})and "
                         f"sources_prob ({len(sources_prob)}) must be same ")
    prob_sum = sum(sources_prob)
    if not 0 <= prob_sum <= 1:
        raise ValueError("Sum of given probabilities must be between 0 and 1")
    none_prob = 1 - prob_sum
    sources.append(None)
    sources_prob.append(none_prob)

    for node in G.nodes():
        source = np.random.choice(sources, p=sources_prob)
        if source is not None:
            G.set_information_source(node, source)


def connected_gnp_graph(n, completion=0.5, sources=None, sources_prob=None):
    G = nx.fast_gnp_random_graph(n, completion)
    components = [list(component) for component in nx.connected_components(G)]

    for comp_a, comp_b in zip(components[1:], components[:-1]):
        e = (choice(comp_a), choice(comp_b))
        G.add_edge(*e)

    G = SimulationGraph(G)

    if sources is not None and sources_prob is not None:
        add_random_sources(G, sources, sources_prob)

    return G


