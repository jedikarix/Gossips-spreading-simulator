from typing import Tuple, Union

import networkx as nx

from Simulation.InformationSource import InformationSource


class SimulationGraph(nx.DiGraph):

    def __init__(self, data=None, **attr):
        super().__init__(data, **attr)

    def add_edge(self, u: int, v: int, trust: float = 0) -> None:
        """
        Add connection from agent u to agent v
        :param u: source agent ID
        :param v: target agent ID
        :param trust: level of trust (default 0)
        """
        super().add_edge(u_of_edge=u, v_of_edge=v, trust=trust)

    def add_bidirectional_edge(self, u: int, v: int,
                               trust: Union[Tuple[float, float], float] = (0, 0)) -> None:
        """
        Add bidirectional connection between u and v agents
        :param u: agent ID
        :param v: agent ID
        :param trust: Pair (trust u in v, trust v in u) or single value if trust equal
        """
        u_trust, v_trust = trust if isinstance(trust, tuple) else (trust, trust)
        self.add_edge(u, v, u_trust)
        self.add_edge(v, u, v_trust)

    def set_information_source(self, u: int, source: InformationSource):
        self.nodes[u]['source'] = source

    def get_information_sources(self):
        return nx.get_node_attributes(self, "source")


def read_simulation_graph(filename):
    return SimulationGraph(nx.read_edgelist(filename, nodetype=int))
