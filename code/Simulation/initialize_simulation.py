from typing import Dict

from Simulation.SimulationAgent import SimulationAgent
from Simulation.SimulationGraph import SimulationGraph
from SemanticAnalysis.SemanticAnalyser import SemanticAnalyser
from Simulation.initialize_logger import initialize_logger


def initialize_simulation(graph: SimulationGraph, hostname: str = "localhost") -> Dict[int, SimulationAgent]:
    """
    Initialize simulation for some graph.
    :param graph: graph representing connections and trust between agents (as edge parameter 'trust')
    :param hostname: hostname of the nodes in spade
    :return: dictionary with (node_id, SimulationAgent) mapping
    """
    def update_trust(edge, trust):
        graph.edges[edge]['trust'] = trust

    agents_ids = graph.nodes()
    neighbours = dict([(agent_id, list(graph.neighbors(agent_id))) for agent_id in agents_ids])
    agents = _initialize_agents(agents_ids, neighbours, info_sources=graph.get_information_sources(),
                                trustiness=graph.get_trustiness_map(), hostname=hostname,
                                trust_change_callback=update_trust)
    initialize_logger()
    for agent in agents.values():
        agent.start()

    for agent in agents.values():
        agent.stop()

    return agents


def _initialize_agents(agent_ids, neighbours_lists, info_sources, trustiness,
                       basename="agent", hostname="localhost", trust_change_callback=lambda edge, trust: None):
    agent_usernames = dict([(agent_id, "{}_{}@{}".format(basename, agent_id, hostname))
                            for agent_id in agent_ids])
    agent_username_to_id = {v: k for k, v in agent_usernames.items()}
    SimulationAgent.agent_username_to_id = agent_username_to_id

    neighbours = dict([(agent_usernames[agent_id],
                        [agent_usernames[neighbour_id] for neighbour_id in neighbours_lists[agent_id]])
                       for agent_id in agent_ids])
    agents = dict()
    sem_anal = SemanticAnalyser()
    for agent_id in agent_ids:
            username = agent_usernames[agent_id]
            agents[agent_id] = SimulationAgent(username, username,
                                               neighbours=neighbours[username],
                                               trustiness=trustiness[agent_id],
                                               information_source=info_sources.get(agent_id, None),
                                               agent_username_to_id=agent_username_to_id,
                                               trust_change_callback=trust_change_callback,
                                               semantic_analyser=sem_anal)
    return agents
