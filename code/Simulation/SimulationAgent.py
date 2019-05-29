import asyncio
from random import sample, randint

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Simulation import SimulationGraph
from Simulation.InformationSource import InformationSource
from Simulation.Knowledge import Knowledge


def prepare_gossip_message(receiver, gossip):
    msg = Message(to=receiver)
    msg.body = gossip
    return msg


class SimulationAgent(Agent):

    class PropagateGossipBehaviour(CyclicBehaviour):
        async def run(self):
            if len(self.agent.neighbours) == 0:
                await asyncio.sleep(100)

            information = self.agent.knowledge.get_random_information()

            if information is not None:
                receiver = sample(self.agent.neighbours, 1)[0]
                message = prepare_gossip_message(receiver, information.body)
                await self.send(message)
                print("{}: I send message to {}".format(self.agent.jid, receiver))
            await asyncio.sleep(randint(3, 10))

    class ReceiveGossipBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                self.agent.knowledge.add_message(msg)
                print("{}: I received message \"{}\" from {}".format(self.agent.jid, msg.body, msg.sender))
            else:
                print("{}: I did not received any message".format(self.agent.jid))

    def __init__(self, jid, password, verify_security=False,
                 neighbours=None, information_source: InformationSource = None, agent_username_to_id=None,
                 trust_change_callback=lambda edge, trust: None):
        super().__init__(jid=jid, password=password, verify_security=verify_security)
        if neighbours is None:
            neighbours = list()
        self.neighbours = neighbours
        self.propagate_behav = None
        self.listen_behav = None
        self.information_source = information_source
        self.agent_username_to_id = agent_username_to_id
        self.knowledge = Knowledge(trust_change_callback=self.trust_changed_in_agent)
        self.trust_change_callback = trust_change_callback

    def trust_changed_in_agent(self, sender, trust):
        sender_id = self.agent_username_to_id[str(sender)]
        agent_id = self.agent_username_to_id[str(self.jid)]
        edge = (sender_id, agent_id)
        self.trust_change_callback(edge, trust)

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

