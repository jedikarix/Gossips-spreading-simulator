import asyncio
import logging
import traceback
from random import sample, randint

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from SemanticAnalysis.SemanticAnalyser import SemanticAnalyser
from Simulation.InformationSource import InformationSource
from Simulation.Knowledge import Knowledge


def _prepare_gossip_message(receiver, information):
    msg = Message(to=receiver)
    msg.body = information.body
    msg.metadata = dict(gossip_id=information.id)
    return msg


class SimulationAgent(Agent):
    """
    Spade agent of the simulation process.
    """
    logger = logging.getLogger("gossip")
    agent_username_to_id = dict()

    @classmethod
    def _log(cls, message: dict):
        cls.logger.debug(message)

    class PropagateGossipBehaviour(CyclicBehaviour):
        """
        Gossip propagator behaviour as spade CyclicBehaviour.
        """
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            if len(self.agent.neighbours) == 0:
                await asyncio.sleep(100)

            information = self.agent.knowledge.get_random_information()

            if information is not None:
                receiver = sample(self.agent.neighbours, 1)[0]
                message = _prepare_gossip_message(receiver, information)
                await self.send(message)

                receiver_id = SimulationAgent.agent_username_to_id[str(receiver)]
                agent_id = SimulationAgent.agent_username_to_id[str(self.jid)]
                SimulationAgent._log(
                    dict(msg_type="send", msg_id=message.metadata["gossip_id"], sender=agent_id, receiver=receiver_id,
                         body=message.body))

            await asyncio.sleep(randint(3, 10))

    class ReceiveGossipBehaviour(CyclicBehaviour):
        """
        Gossip receiver behaviour as spade CyclicBehaviour.
        """
        def __init__(self, jid):
            super().__init__()
            self.jid = jid

        async def run(self):
            try:
                msg = await self.receive(timeout=10)
                agent_id = SimulationAgent.agent_username_to_id[str(self.jid)]
                if msg is not None:
                    sender_id = SimulationAgent.agent_username_to_id[str(msg.sender)]
                    self.agent.knowledge.add_message(msg)
                    SimulationAgent._log(
                        dict(msg_type="receive", msg_id=msg.metadata["gossip_id"], sender=sender_id, receiver=agent_id,
                             body=msg.body))
                else:
                    print("{}: I did not received any message".format(agent_id))
            except Exception as e:
                traceback.print_exc(e)

    def __init__(self, jid, password, semantic_analyser: SemanticAnalyser, verify_security=False,
                 neighbours=None, information_source: InformationSource = None,
                 trust_change_callback=lambda edge, trust: None, trustiness: float = 1):
        """
        Simulation agent initializer.
        :param jid: agent username in XMPP server, e.g. 'agent 0'
        :param password: agent password in XMPP server, e.g. 'agent 0'
        :param semantic_analyser: semantic analyzer to use during Knowledge processing
        :param verify_security: XMPP server parameter - whether agents should be verified or not
        :param neighbours: list of agents' username (e.g. 'agent 0') being the agent neighbours (for whom the agent can
        sent a message)
        :param information_source: information source of the agent
        :param trust_change_callback: function to call when trust on some edge has changed (the edge parameter has
        layout as (sender, receiver))
        :param trustiness: factor describing how much the trust to some other agent influence the received message
        rating
        """
        super().__init__(jid=jid, password=password, verify_security=verify_security)
        if neighbours is None:
            neighbours = list()
        self.neighbours = neighbours
        self.propagate_behav = None
        self.listen_behav = None
        self.information_source = information_source
        self.knowledge = Knowledge(
            trust_change_callback=self._trust_changed_in_agent,
            semantic_analyser=semantic_analyser,
            trustiness=trustiness)
        self.trust_change_callback = trust_change_callback

    def _trust_changed_in_agent(self, sender, trust):
        sender_id = SimulationAgent.agent_username_to_id[str(sender)]
        agent_id = SimulationAgent.agent_username_to_id[str(self.jid)]
        edge = (sender_id, agent_id)
        self.trust_change_callback(edge, trust)
        SimulationAgent._log(dict(msg_type="trust_change", sender=agent_id, receiver=agent_id, trust_change=trust))

    async def setup(self):
        print("hello, i'm {}. My neighbours: {}".format(self.jid, self.neighbours))
        self.propagate_behav = self.PropagateGossipBehaviour(self.jid)
        self.listen_behav = self.ReceiveGossipBehaviour(self.jid)

        self.add_behaviour(self.propagate_behav)
        self.add_behaviour(self.listen_behav)

        if self.information_source is not None:
            self._read_source()

    def _read_source(self, k=1):
        if self.information_source is None:
            return
        else:
            for i in range(k):
                for information in self.information_source.get_information():
                    print(self.jid, information)
                    self.knowledge.add_information(information)
