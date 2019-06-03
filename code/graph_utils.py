from time import sleep

import matplotlib.pyplot as plt
import networkx as nx

from Simulation import SimulationGraph


def plot_graph(simulation_graph: SimulationGraph, label_font_size=7, label_position=0.1, float_precision=2, non_blocking_mode=False):
    """
    Plots simulation graph. It assumes that the graph has trust parameter in each edge.
    :param simulation_graph: the graph to plot
    :param label_font_size: font size of the labels (trust value)
    :param label_position: position of the label on the edge (closer to 0 - closer to the arrow)
    :param float_precision: precision of the trust label
    :param non_blocking_mode: whether to block instantaneously (to plot right away)
    """
    def gen_color(trust):
        color_value = int(round(min([255, 255*abs(trust)])))
        if trust >= 0:
            return "#%02X%02X%02X" % (0, color_value, 0)
        else:
            return "#%02X%02X%02X" % (color_value, 0, 0)

    trustiness_map = simulation_graph.get_trustiness_map()
    node_cmap =["#%02X%02X%02X" % (round(255*(1 - trustiness)), round(255*trustiness), 0) for node, trustiness in trustiness_map.items()]
    pos = nx.kamada_kawai_layout(simulation_graph)
    nx.draw(simulation_graph, pos, with_labels=True, font_weight='bold')
    nx.draw_networkx_nodes(simulation_graph, pos=pos, node_color=node_cmap, with_labels=True)
    edge_labels = dict([((u, v,), round(d.get('trust', 0), float_precision))
                        for u, v, d in simulation_graph.edges(data=True)])
    labels_colors = dict([((u, v,), gen_color(d.get('trust', 0)))
                          for u, v, d in simulation_graph.edges(data=True)])
    for edge, label in edge_labels.items():
        # manual loop is necessary as font_color can take only one arg
        nx.draw_networkx_edge_labels(simulation_graph, pos,
                                     edge_labels={edge: label},
                                     label_pos=label_position,
                                     font_size=label_font_size,
                                     font_color=labels_colors[edge])
    if not non_blocking_mode:
        plt.show()


def plot_graph_live(simulation_graph: SimulationGraph, refresh_period_s: float, label_font_size=7, label_position=0.1, float_precision=2):
    """
    Plots graph live with refresh some refresh rate.
    :param simulation_graph: the graph to plot
    :param refresh_period_s: delay between each plot. 0.0 to plot as fast as possible
    :param label_font_size: font size of the labels (trust value)
    :param label_position: position of the label on the edge (closer to 0 - closer to the arrow)
    :param float_precision: precision of the trust label
    """
    plt.ion()
    plt.show()
    while True:
        plot_graph(simulation_graph, label_font_size, label_position, float_precision, non_blocking_mode=True)
        plt.draw()
        plt.pause(0.001)
        sleep(refresh_period_s)
        plt.clf()


def serialize_graph(simulation_graph: SimulationGraph, path: str):
    """
    Serialize the graph to file.
    :param simulation_graph: graph to serialize
    :param path: path to the output file
    """
    nx.write_gpickle(simulation_graph, path)


def deserialize_graph(path: str) -> SimulationGraph:
    """
    Read graph from file.
    :param path: path to the file with the graph
    :return: deserialized graph
    """
    return nx.read_gpickle(path)
