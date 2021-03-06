import os
import pickle
import sys
from threading import Lock

import numpy as np
import torch

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
            model_folder=os.path.join(os.path.dirname(__file__), 'GenSen', 'data', 'models'),
            filename_prefix='nli_large',
            pretrained_emb=os.path.join(os.path.dirname(__file__), 'GenSen', 'data', 'embedding', 'glove.840B.300d.h5')
        )

        with open(os.path.join(os.path.dirname(__file__), 'GenSen', 'data', 'models', 'senteval.pickle'), 'rb') as file:
            self.__evaluator = pickle.load(file)

        self.__mutex = Lock()

    def get_entailments_with_levels(self, sentence, sentences):
        """Analyzes relation between a sentence and all in a collection

        Args:
            sentence: a sentence
            sentences: a non-empty list of sentences

        Returns:
            entailment:
                0 if entailed, 1 if neutral, 2 if contradicting for each element in sentences
            level:
                a non-negative value of how much this sentence is entailed with each element in sentences
        """
        self.__mutex.acquire()
        _, encoded = self.__encoder.get_representation([sentence] + sentences, pool='last', return_numpy=True, tokenize=True)
        input = np.concatenate((
            np.repeat([encoded[0]], len(sentences), axis=0),
            encoded[1:],
            (np.repeat([encoded[0]], len(sentences), axis=0)) * encoded[1:]), axis=1)
        output = self.__model_predict(input)
        self.__mutex.release()

        entailment = np.argmax(output, axis=1)

        level = np.max(output, axis=1) - np.transpose(output)[1]

        for i, sent in enumerate(sentences):
            if sentence == sent:
                entailment[i] = 0
                level[i] = 1e10

        return entailment, level

    def get_entailment(self, sentence1, sentence2):
        """Analyzes relation between two sentences

        Args:
            sentence1: first sentence as a string
            sentence2: second sentence as a string

        Returns:
            0 if entailed, 1 if neutral, 2 if contradicting
        """

        if sentence1 == sentence2:
            return 0

        self.__mutex.acquire()
        _, encoded = self.__encoder.get_representation([sentence1, sentence2], pool='last', return_numpy=True, tokenize=True)
        input = np.concatenate((encoded[0], encoded[1], encoded[0] * encoded[1]))
        output = self.__model_predict(np.array([input]))
        self.__mutex.release()

        return np.argmax(output)

    def __model_predict(self, input):
        sentence_size = input.shape[1] // 3
        batch_size = input.shape[0]
        switched_input = np.hstack((input[:, sentence_size:2*sentence_size], input[:, 0:sentence_size], input[:, 2*sentence_size:3*sentence_size]))

        input = np.vstack((input, switched_input))
        
        self.__evaluator.model.eval()
        input = torch.FloatTensor(input).cuda()
        yhat = []
        with torch.no_grad():
            for i in range(0, len(input), self.__evaluator.batch_size):
                x = input[i:i + self.__evaluator.batch_size]
                output = self.__evaluator.model(x)
                yhat.append(output.data.cpu().numpy())
        yhat = np.vstack(yhat)
        yhat = (yhat[0:batch_size, :] + yhat[batch_size:2*batch_size, :]) / 2
        return yhat
