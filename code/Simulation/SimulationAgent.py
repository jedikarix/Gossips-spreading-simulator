from spade.agent import Agent


class SimulationAgent(Agent):
    def __init__(self, jid, password, verify_security=False, neighbours=None):
        super().__init__(jid=jid, password=password, verify_security=verify_security)
        if neighbours is None:
            neighbours = list()
        self.neighbours = neighbours

    async def setup(self):
        print("hello, i'm {}. My neighbours: {}".format(self.jid, self.neighbours))
