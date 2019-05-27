import os
import pickle
import sys
from multithreading import Lock

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), 'GenSen'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'SentEval'))

from gensen import GenSenSingle


class SemanticAnalyser(object):
    """Class for comparing sentences for entailment
    """
    def __init__(self):
        """Initalizes object
        """
        self.__encoder = GenSenSingle(
            model_folder=os.path.join('GenSen', 'data', 'models'),
            filename_prefix='nli_large',
            pretrained_emb=os.path.join('GenSen', 'data', 'embedding', 'glove.840B.300d.h5')
        )

        with open(os.path.join('GenSen', 'data', 'models', 'senteval.pickle'), 'rb') as file:
            self.__evaluator = pickle.load(model_file)

        self.__mutex = Lock()

    def get_entailment(sentence1, sentence2):
        """Analyzes relation between two sentences

        Args:
            sentence1: first sentence as a string
            sentence2: second sentence as a string

        Returns:
            0 if entailed, 1 if neutral, 2 if contradicting
        """
        self.__mutex.acquire()
        _, encoded = self.__encoder.get_representation([sentence1, sentence2], pool='last', return_numpy=True, tokenize=True)
        input = np.concatenate((encoded[0], encoded[1], encoded[0] * encoded[1]))
        output = self.__evaluator.predict([input])
        self.__mutex.release()

        return output[0]
