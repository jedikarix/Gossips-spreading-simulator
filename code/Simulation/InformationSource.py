from random import choice
from typing import List

import newspaper

from Simulation.Knowledge import KnowledgeInformation


class InformationSource:
    def get_information(self, trust: float = 1) -> List[KnowledgeInformation]:
        raise NotImplementedError("get_information is virtual")

    @staticmethod
    def _get_information_impl(summaries, trust: float = 1) -> List[KnowledgeInformation]:
        return [KnowledgeInformation(sentence, trust, sentence_id) for sentence_id, sentence in
                choice(summaries).items()]


class PredefinedInformationSource(InformationSource):
    def __init__(self, filename):
        sentences = []
        with open(filename) as file:
            sentences = [[sentence] for sentence in file.read().split('\n')]

        self.summaries = list()
        idx = 0
        for summary in sentences:
            sentence_to_id = dict([(i, sentence) for sentence in summary for i in range(idx, idx + len(summary))])
            idx += len(summary)
            self.summaries.append(sentence_to_id)
        print(self.summaries)

    def get_information(self, trust: float = 1) -> List[KnowledgeInformation]:
        return InformationSource._get_information_impl(self.summaries, trust)


class OnlineInformationSource(InformationSource):
    def __init__(self, url: str, articles_limit=100, summary_sentences=5):
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
        idx = 0
        for summary in summaries_list:
            sentence_to_id = dict([(i, sentence) for sentence in summary for i in range(idx, idx + len(summary))])
            idx += len(summary)
            self.summaries.append(sentence_to_id)

    def get_information(self, trust: float = 1) -> List[KnowledgeInformation]:
        return InformationSource._get_information_impl(self.summaries, trust)
