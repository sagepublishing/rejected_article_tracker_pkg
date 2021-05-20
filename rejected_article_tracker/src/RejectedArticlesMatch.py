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

from .ML.config import Config as mlconfig

from .LoadModel import LoadModel

class RejectedArticlesMatch:

    def __init__(self, articles: list, config: dict, email: str, results: list):
        """
        :rtype: RejectedArticlesMatch
        :param articles: dict   A dictionary of articles. @see ArticleItem for required fields
        :param config: dict     Some app configuration. @see docs
        :param email: str       CrossRef API requires email address
        :param results: list    A list to populate after each result is processed.
                                By injecting results we can grab the already processed results in case off failiure.
        """
        self.articles = FilteredArticles(articles=articles)
        self.email = email
        self.config = config
        self.results = results
        self.clf = LoadModel().clf


    def match(self) -> list:
        """
        :return: list
        """
        return list(map(self.__match_article, self.articles.to_dict()))

    def __match_article(self, article):
        """
        Mapper method to process each article which then appends to the results variable.

        :param article:
        :return: None
        """
        search_results = CrossRef(article=article,
                                  http_client=http_client,
                                  sleep=time.sleep,
                                  email=self.email).search()

        if search_results!=None and len(search_results)>0:
            search_results = [SearchResult(match_article=search_results[i],
                                        query_article=article,
                                        clf=self.clf,
                                        rank=i + 1).to_dict() for i in range(len(search_results))]

            winner = BestCandidate(candidates=search_results, threshold=self.config['threshold']).find()
        else:
            winner = None

        if winner == None:
            self.results.append(EmptyResult(original=article).to_dict())
        else:
            self.results.append(Result(original=article, winner=winner).to_dict())
