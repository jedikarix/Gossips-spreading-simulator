import networkx as nx


class SimulationGraph(nx.DiGraph()):

    def __init__(self, data=None, **attr):
        super().__init__(data, **attr)

    def add_edge(self, u: int, v: int, trust: float = 0, data_source=None):
        """
        Add connection between agents
        :param u: source agent
        :param v: target agent
        :param trust: level of trust (default 0)
        :param data_source: (optional)
        :return:
        """
        attr_dict = dict()
        attr_dict["trust"] = trust
        attr_dict["data_source"] = data_source
        super().add_edge(u_of_edge=u, v_of_edge=v, attr_dict=attr_dict)
