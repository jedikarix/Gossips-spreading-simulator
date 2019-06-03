from random import choice
from typing import List

import newspaper

from Simulation.Knowledge import KnowledgeInformation


class InformationSource:
    """
    Base class for all information sources.
    """
    _info_id = 0

    def get_information(self, trust: float = 1) -> List[KnowledgeInformation]:
        """
        Retrieve one quaint of the available information. Information consists of multiple
        :class:`~Simulation.Knowledge.KnowledgeInformation`
        :param trust: trust of the every returned :class:`~Simulation.Knowledge.KnowledgeInformation`
        :return: list of :class:`~Simulation.Knowledge.KnowledgeInformation`
        """
        raise NotImplementedError("get_information is virtual")

    @staticmethod
    def _get_information_impl(summaries, trust: float = 1) -> List[KnowledgeInformation]:
        return [KnowledgeInformation(sentence, trust, sentence_id) for sentence_id, sentence in
                choice(summaries).items()]


class PredefinedInformationSource(InformationSource):
    """
    Information source with predefined sentences.
    """
    def __init__(self, filename):
        """
        Initialize information source from file. File should contain one sentence per line. Each sentence will be
        treated as individual sentence belonging to one information (:method:`~get_information` always return same list
        containing all the sentences from file).
        :param filename: path to file with sentences
        """
        with open(filename) as file:
            summary = file.read().split('\n')

        self.summaries = list()
        sentence_to_id = dict(zip(range(InformationSource._info_id, InformationSource._info_id + len(summary)), summary))
        InformationSource._info_id += len(summary)
        self.summaries.append(sentence_to_id)

    def get_information(self, trust: float = 1) -> List[KnowledgeInformation]:
        """
        Return same list each time containing all the sentences from file.
        :param trust: trust of the every returned :class:`~Simulation.Knowledge.KnowledgeInformation`
        :return: list of :class:`~Simulation.Knowledge.KnowledgeInformation`
        """
        return InformationSource._get_information_impl(self.summaries, trust)


class OnlineInformationSource(InformationSource):
    """
    Information source based on real news website.
    """
    def __init__(self, url: str, articles_limit=100, summary_sentences=5):
        """
        Initializes the information source with summaries of the articles_limit articles. Each summary will have
        summary_sentences number of sentences.
        :param url: news website URL, e.g. "https://www.bbc.co.uk/"
        :param articles_limit: limit number of articles to fetch
        :param summary_sentences: number of sentences in each summary
        """
        config = newspaper.Config()
        config.MAX_SUMMARY_SENT = summary_sentences
        config.memoize_articles = False
        config.fetch_images = False

        self.paper = newspaper.build(url, config=config)
        summaries_list = list()

        i = 0
        while len(summaries_list) < articles_limit and i < len(self.paper.articles):
            article = self.paper.articles[i]
            i += 1
            try:
                article.download()
                article.parse()
                article.nlp()
            except newspaper.article.ArticleException:
                continue
            if article.summary != str():
                summaries_list.append(article.summary.split('\n'))

        self.summaries = list()
        for summary in summaries_list:
            sentence_to_id = dict(
                zip(range(InformationSource._info_id, InformationSource._info_id + len(summary)), summary))
            InformationSource._info_id += len(summary)
            self.summaries.append(sentence_to_id)

    def get_information(self, trust: float = 1) -> List[KnowledgeInformation]:
        """
        Return one of the article's summaries as list of KnowledgeInformation, each contains one sentence of the summary
        :param trust: trust of the every returned :class:`~Simulation.Knowledge.KnowledgeInformation`
        :return: list of :class:`~Simulation.Knowledge.KnowledgeInformation`
        """
        return InformationSource._get_information_impl(self.summaries, trust)
