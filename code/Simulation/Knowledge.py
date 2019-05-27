from math import exp
from random import random
from typing import Union

from numpy.random import choice
from spade.message import Message


class KnowledgeInformation:
    def __init__(self, body, trust, sender=None):
        self.body = body
        self.sender = sender
        self.trust = trust


class Knowledge:
    def __init__(self, max_inf=0):
        self.max_inf = max_inf
        self.informations = list()
        self.agents_trust = dict()

    def add_message(self, message: Message) -> None:
        """
        Update knowledge based on received message
        :param message: received message
        """
        sender = message.sender
        sender_trust = self.agents_trust.get(sender, 0)
        info_trust = random() - 0.5  #
        self.add_information(KnowledgeInformation(message.body, sender_trust + info_trust, sender))
        self.agents_trust[sender] = info_trust

    def add_information(self, information: KnowledgeInformation) -> None:
        """
        Add information directly to knowledge
        :param information:
        """
        self.informations.append(information)

    def get_random_information(self) -> Union[KnowledgeInformation, None]:
        """
        Get random information from knowledge, where probability of draw is proportional to trust.
        :return: Drawn information
        """
        if len(self.informations) == 0:
            return None
        reliable_informations = [information for information in self.informations if information.trust > 0]
        trust_exps = [exp(information.trust) for information in reliable_informations]
        sum_trust_exp = sum(trust_exps)
        return choice(reliable_informations, p=[trust_exp/sum_trust_exp for trust_exp in trust_exps])
