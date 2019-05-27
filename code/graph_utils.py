import networkx as nx
import matplotlib.pyplot as plt


def plot_graph(simulation_graph, label_font_size=7, label_position=0.1):
    """
    Plots simulation graph. It assumes that the graph has trust parameter in each edge.
    """
    def gen_color(trust):
        color_value = int(round(min([255, 255*abs(trust)])))
        if trust >= 0:
            return "#%02X%02X%02X" % (0, color_value, 0)
        else:
            return "#%02X%02X%02X" % (color_value, 0, 0)
    pos = nx.shell_layout(simulation_graph)
    nx.draw(simulation_graph, pos, with_labels=True, font_weight='bold')
    edge_labels = dict([((u, v,), d['trust'])
                        for u, v, d in simulation_graph.edges(data=True)])
    labels_colors = dict([((u, v,), gen_color(d['trust']))
                          for u, v, d in simulation_graph.edges(data=True)])
    for edge, label in edge_labels.items():
        # manual loop is necessary as font_color can take only one arg
        nx.draw_networkx_edge_labels(simulation_graph, pos,
                                     edge_labels={edge: label},
                                     label_pos=label_position,
                                     font_size=label_font_size,
                                     font_color=labels_colors[edge])
    plt.show()

def serialize_graph(G, path):
    nx.write_gpickle(G, path)


def deserialize_graph(path):
    return nx.read_gpickle(path)