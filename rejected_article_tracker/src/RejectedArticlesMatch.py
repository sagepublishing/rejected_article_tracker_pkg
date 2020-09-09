import os
import requests as http_client
import time
import pickle


from .FilteredArticles import FilteredArticles
from .CrossRef import CrossRef
from .SearchResult import SearchResult
from .BestCandidate import BestCandidate
from .Result import Result
from .EmptyResult import EmptyResult


class RejectedArticlesMatch:

    def __init__(self, articles: list, config, email: str, results: list):
        self.articles = FilteredArticles(articles=articles, filter_dates=config.filter_dates)
        self.email = email
        self.config = config
        self.results = results

        with open(os.path.join(os.path.dirname(__file__)) + '/lr_model', 'rb') as f:
            self.clf = pickle.load(f)

    def match(self):
        return list(map(self.__match_article, self.articles.to_dict()))

    def __match_article(self, article):
        search_results = CrossRef(article=article,
                                  http_client=http_client,
                                  sleep=time.sleep,
                                  email=self.email).search()

        search_results = [SearchResult(details=search_results[i],
                                       match_article=article,
                                       clf=self.clf,
                                       rank=i + 1).to_dict() for i in range(len(search_results))]

        winner = BestCandidate(candidates=search_results, threshold=self.config.threshold).find()

        if winner is None:
            self.results.append(EmptyResult(original=article).to_dict())
        else:
            self.results.append(Result(original=article, winner=winner).to_dict())
