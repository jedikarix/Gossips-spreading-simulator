from Simulation.SimulationAgent import SimulationAgent
from Simulation.SimulationGraph import SimulationGraph


def initialize_agents(agent_ids, neighbours_lists, basename="agent", hostname="localhost"):
    agent_usernames = dict([(agent_id, "{}_{}@{}".format(basename, agent_id, hostname))
                            for agent_id in agent_ids])
    neighbours = dict([(agent_usernames[agent_id],
                        [agent_usernames[neighbour_id] for neighbour_id in neighbours_lists[agent_id]])
                       for agent_id in agent_ids])
    agents = dict()
    for agent_id in agent_ids:
            username = agent_usernames[agent_id]
            agents[agent_id] = SimulationAgent(username, username, neighbours=neighbours[username])
    return agents


def initialize_simulation(graph: SimulationGraph, hostname="localhost"):
    agents_ids = graph.nodes()
    neighbours = dict([(agent_id, list(graph.neighbors(agent_id))) for agent_id in agents_ids])
    agents = initialize_agents(agents_ids, neighbours, hostname=hostname)
    for agent in agents.values():
        agent.start()

    for agent in agents.values():
        agent.stop()
