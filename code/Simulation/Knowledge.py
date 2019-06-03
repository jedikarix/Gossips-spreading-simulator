from math import exp
from random import random
from typing import Union

import numpy as np
from numpy.random import choice
from spade.message import Message

from SemanticAnalysis.SemanticAnalyser import SemanticAnalyser


class KnowledgeInformation:
    """
    The smallest portion of the information. Represents the gossip itself with some additional parameters.
    """
    def __init__(self, body: str, trust: float, information_id: int, sender=None) -> None:
        self.body = body
        self.id = information_id
        self.last_sender = sender
        self.trust = trust


class Knowledge:
    def __init__(self, semantic_analyser: SemanticAnalyser, max_knowledge_size: int = 0,
                 trustiness: float = 1, trust_change_callback=lambda sender, trust: None):
        """
        Initialize the knowledge.
        :param semantic_analyser: semantic analyzer to use for information comparison
        :param max_knowledge_size: maximum knowledge size (not implemented yet)
        :param trustiness: factor describing how much the trust to some other agent influence the received message
        rating
        :param trust_change_callback: function to call after each trust change to some sender
        """
        self.max_knowledge_size = max_knowledge_size
        self.informations = list()
        self.agents_trust = dict()
        self.trust_change_callback = trust_change_callback
        self.semantic_analyser = semantic_analyser
        self.trustiness = trustiness

    def add_message(self, message: Message) -> None:
        """
        Update knowledge based on received message
        :param message: received message
        """
        sender = message.sender
        sender_trust = self.agents_trust.get(sender, 0)
        information_id = message.metadata["gossip_id"]
        info_trust = exp(self.trustiness * sender_trust) / (1 + exp(self.trustiness * sender_trust))

        if self.informations:
            most_entailed, entailment = self._get_most_entailed_information(message)

            if entailment == 0:  # if message is entailed to current knowledge
                most_entailed.trust += info_trust
                if most_entailed.last_sender:
                    self._add_agent_trust(most_entailed.last_sender, info_trust)
                most_entailed.last_sender = sender
                return

            elif entailment == 2:  # if message is contradicting our current knowledge
                most_entailed.trust -= info_trust
                if most_entailed.last_sender:
                    self._add_agent_trust(most_entailed.last_sender, -info_trust)
                if most_entailed.trust < 0:  # we lost trust to the previous message
                    new_info = KnowledgeInformation(message.body, sender, -most_entailed.trust, information_id)
                    self.informations[self.informations.index(most_entailed)] = new_info  # replace
                return

        # first information or not entailed with any that we currently have
        self.add_information(KnowledgeInformation(message.body, sender_trust + info_trust,
                                                  information_id, sender))

    def _add_agent_trust(self, sender, trust):
        self.agents_trust[sender] = self.agents_trust.get(sender, 0) + trust
        self.trust_change_callback(sender, self.agents_trust[sender])

    def add_information(self, information: KnowledgeInformation) -> None:
        """
        Add information directly to knowledge
        :param information: information to inject
        """
        self.informations.append(information)

    def get_random_information(self) -> Union[KnowledgeInformation, None]:
        """
        Get random information from knowledge, where probability of draw is proportional to trust.
        :return: drawn information
        """
        reliable_informations = [information for information in self.informations if information.trust > 0]
        if len(reliable_informations) == 0:
            return None
        trust_exps = [exp(information.trust) for information in reliable_informations]
        sum_trust_exp = sum(trust_exps)
        return choice(reliable_informations, p=[trust_exp/sum_trust_exp for trust_exp in trust_exps])

    def _get_most_entailed_information(self, message: Message):
        sentence = message.body
        sentences = [i.body for i in self.informations]
        entailments, levels = self.semantic_analyser.get_entailments_with_levels(sentence, sentences)
        max_id = np.where(max(levels) == levels)[0][0]

        return self.informations[max_id], entailments[max_id]
