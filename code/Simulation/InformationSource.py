from random import choice

import newspaper

from Simulation.Knowledge import KnowledgeInformation


class InformationSource:

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
        self.summaries = dict(enumerate(summaries_list))

    def get_information(self, trust=1):
        return [KnowledgeInformation(sentence, trust, id) for id, sentence in choice(list(self.summaries.items()))]
