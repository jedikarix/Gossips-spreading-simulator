from math import exp
from random import random

from numpy.random import choice
from spade.message import Message


class KnowledgeInformation:
    def __init__(self, body, trust, sender):
        self.body = body
        self.sender = sender
        self.trust = trust


class Knowledge:
    def __init__(self, max_inf=0):
        self.max_inf = max_inf
        self.informations = list()
        self.agents_trust = dict()

    def add_information(self, message: Message):
        sender = message.sender
        sender_trust = self.agents_trust.get(sender, 0)
        info_trust = random() - 0.5  #
        self.informations.append(KnowledgeInformation(message.body, sender_trust + info_trust, sender))
        self.agents_trust[sender] = info_trust

    def get_random_information(self):
        reliable_informations = [information for information in self.informations if information.trust > 0]
        trust_exps = [exp(information.trust) for information in reliable_informations]
        sum_trust_exp = sum(trust_exps)
        return choice(reliable_informations, 1, p=[trust_exp/sum_trust_exp for trust_exp in trust_exps])
