import asyncio
from random import sample, randint

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


def prepare_gossip_message(receiver, gossip):
    msg = Message(to=receiver)
    msg.body = gossip
    return msg


class SimulationAgent(Agent):

    class PropagateGossipBehaviour(CyclicBehaviour):
        async def run(self):
            if len(self.agent.neighbours) == 0:
                await asyncio.sleep(100)
            receiver = sample(self.agent.neighbours, 1)[0]
            message = prepare_gossip_message(receiver, "pst")
            await self.send(message)
            print("{}: I send message to {}".format(self.agent.jid, receiver))
            await asyncio.sleep(randint(3, 10))

    class ReceiveGossipBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print("{}: I received message \"{}\" from {}".format(self.agent.jid, msg.body, msg.sender))
            else:
                print("{}: I did not received any message".format(self.agent.jid))

    def __init__(self, jid, password, verify_security=False, neighbours=None):
        super().__init__(jid=jid, password=password, verify_security=verify_security)
        if neighbours is None:
            neighbours = list()
        self.neighbours = neighbours
        self.propagate_behav = None
        self.listen_behav = None

    async def setup(self):
        print("hello, i'm {}. My neighbours: {}".format(self.jid, self.neighbours))
        self.propagate_behav = self.PropagateGossipBehaviour()
        self.listen_behav = self.ReceiveGossipBehaviour()

        self.add_behaviour(self.propagate_behav)
        self.add_behaviour(self.listen_behav)
