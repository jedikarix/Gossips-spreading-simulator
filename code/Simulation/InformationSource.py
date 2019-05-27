from random import choice

import newspaper


class InformationSource:

    def __init__(self, url: str):
        self.paper = newspaper.build(url)
        self.articles = [article for article in self.paper.articles]
        for article in self.articles:
            article.nlp()
        self.summaries = [article.summary for article in self.articles]

    def get_information(self):
        return choice(self.summaries)
