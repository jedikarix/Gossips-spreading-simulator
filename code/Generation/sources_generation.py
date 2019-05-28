from typing import List, Union

import numpy as np

from Simulation.SimulationGraph import SimulationGraph
from Simulation.InformationSource import InformationSource


def add_random_sources(G: SimulationGraph,
                       sources: Union[List[InformationSource], InformationSource],
                       sources_prob: Union[List[float], float], nodes: List[int] = None) -> SimulationGraph:
    """
    Adds random sources from given list with given probabilities.
    If probabilities don't sum to 1 there will be probability (1 - sum) for no assigning any source.
    :param G: Base SimulationGraph
    :param sources: List of information sources or single information source
    :param sources_prob: List of probabilities for every source in sources or single probability for every source.
    Sum of sources must be between 0 and 1.
    :param nodes: subset of G nodes to set source (optional)
    :return: SimulationGraph with assigned information sources
    """
    if not isinstance(sources, list):
        sources = [sources]
    if not isinstance(sources_prob, list):
        sources_prob = [sources_prob] * len(sources)

    if len(sources) != len(sources_prob):
        raise ValueError(f"Length of sources ({len(sources)})and "
                         f"sources_prob ({len(sources_prob)}) must be same ")
    prob_sum = sum(sources_prob)
    if not 0 <= prob_sum <= 1:
        raise ValueError("Sum of given probabilities must be between 0 and 1")
    none_prob = 1 - prob_sum
    sources.append(None)
    sources_prob.append(none_prob)

    if nodes is None:
        nodes = G.nodes()

    for node in nodes:
        source = np.random.choice(sources, p=sources_prob)
        if source is not None:
            G.set_information_source(node, source)

    return G


def add_sources_to_groups(G: SimulationGraph, groups: List[List[int]],
                          sources: List[InformationSource],
                          groups_sources_prob: Union[List[float], float]) -> SimulationGraph:
    """
    Adds different sources to consecutive groups of nodes in graph
    :param G: Base SimulationGraph
    :param groups: List of lists of nodes in groups
    :param sources: List of sources for every group
    :param groups_sources_prob: List of probabilities of assigning source to node for every group or single probability
    for every group
    :return: SimulationGraph with assigned information sources
    """

    if not isinstance(groups_sources_prob, list):
        groups_sources_prob = [groups_sources_prob] * len(groups)

    if len(groups) != len(sources) != len(groups_sources_prob):
        raise ValueError(f"Length of groups ({len(groups)}), sources ({len(sources)}) "
                         f"and groups_sources_prob ({len(groups_sources_prob)}) must be same ")

    for group, source, prob in zip(groups, sources, groups_sources_prob):
        G = add_random_sources(G, sources=source, sources_prob=prob, nodes=group)

    return G
