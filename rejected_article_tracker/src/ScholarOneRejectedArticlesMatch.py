from .RejectedArticlesMatch import RejectedArticlesMatch
from .ScholarOneArticleAdapter import ScholarOneArticleAdapter


class ScholarOneRejectedArticlesMatch:

    def __init__(self, articles: list, config, email: str, results: list):
        articles = list(map(ScholarOneArticleAdapter.adapt, articles))
        self.matcher = RejectedArticlesMatch(
            articles=articles,
            config=config,
            email=email,
            results=results
        )

    def match(self):
        return self.matcher.match()


