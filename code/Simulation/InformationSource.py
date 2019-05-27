from random import choice

import newspaper

from Simulation.Knowledge import KnowledgeInformation


class InformationSource:

    def __init__(self, url: str, articles_limit=100, summary_sentences=5):

        self.paper = newspaper.build(url)
        self.articles = [article for article in self.paper.articles[:min(len(self.paper.articles), articles_limit)]]
        self.summaries = list()
        for article in self.articles:
            try:
                article.download()
                article.parse()
                article.nlp()
            except newspaper.article.ArticleException:
                continue
            if article.summary != str():
                self.summaries.append(article.summary.split('\n')[-1])

    def get_information(self, trust=1):
        return [KnowledgeInformation(sentence, trust) for sentence in choice(self.summaries)]
