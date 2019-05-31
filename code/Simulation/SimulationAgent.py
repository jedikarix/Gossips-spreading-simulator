import asyncio
import logging
import json
from random import sample, randint

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Simulation.InformationSource import InformationSource
from Simulation.Knowledge import Knowledge

from SemanticAnalysis.SemanticAnalyser import SemanticAnalyser


def prepare_gossip_message(receiver, information):
    msg = Message(to=receiver)
    msg.body = information.body
    msg.metadata = dict(gossip_id=information.id)
    return msg


class SimulationAgent(Agent):

    class PropagateGossipBehaviour(CyclicBehaviour):
        async def run(self):
            if len(self.agent.neighbours) == 0:
                await asyncio.sleep(100)

            information = self.agent.knowledge.get_random_information()

            if information is not None:
                receiver = sample(self.agent.neighbours, 1)[0]
                message = prepare_gossip_message(receiver, information)
                await self.send(message)

                receiver_id = self.agent_username_to_id[str(receiver)]
                agent_id = self.agent_username_to_id[str(self.jid)]
                self.log(dict(msg_type="send", msg_id=message.metadata["gossip_id"], sender=agent_id, receiver=receiver_id, body=message.body))

            await asyncio.sleep(randint(3, 10))

    class ReceiveGossipBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            sender_id = self.agent_username_to_id[str(msg.sender)]
            agent_id = self.agent_username_to_id[str(self.jid)]
            if msg:
                self.agent.knowledge.add_message(msg)
                self.log(dict(msg_type="receive", msg_id=msg.metadata["gossip_id"], sender=sender_id, receiver=agent_id, body=msg.body))
            else:
                print("{}: I did not received any message".format(agent_id))

    def __init__(self, jid, password, semantic_analyser: SemanticAnalyser, verify_security=False,
                 neighbours=None, information_source: InformationSource = None, agent_username_to_id=None,
                 trust_change_callback=lambda edge, trust: None, trustiness: float = 1):
        super().__init__(jid=jid, password=password, verify_security=verify_security)
        if neighbours is None:
            neighbours = list()
        self.neighbours = neighbours
        self.propagate_behav = None
        self.listen_behav = None
        self.information_source = information_source
        self.agent_username_to_id = agent_username_to_id
        self.knowledge = Knowledge(
            trust_change_callback=self.trust_changed_in_agent,
            semantic_analyser=semantic_analyser,
            trustiness=trustiness)
        self.trust_change_callback = trust_change_callback
        self.logger = logging.getLogger()

    def trust_changed_in_agent(self, sender, trust):
        sender_id = self.agent_username_to_id[str(sender)]
        agent_id = self.agent_username_to_id[str(self.jid)]
        edge = (sender_id, agent_id)
        self.trust_change_callback(edge, trust)
        self.log(dict(msg_type="trust_change", sender=agent_id, receiver=agent_id, trust_change=trust))

    async def setup(self):
        print("hello, i'm {}. My neighbours: {}".format(self.jid, self.neighbours))
        self.propagate_behav = self.PropagateGossipBehaviour()
        self.listen_behav = self.ReceiveGossipBehaviour()

        self.add_behaviour(self.propagate_behav)
        self.add_behaviour(self.listen_behav)

        if self.information_source is not None:
            self.read_source()

    def read_source(self, k=1):
        if self.information_source is None:
            return
        else:
            for i in range(k):
                for information in self.information_source.get_information():
                    print(self.jid, information)
                    self.knowledge.add_information(information)

    def log(self, message):
        self.logger.debug(message)