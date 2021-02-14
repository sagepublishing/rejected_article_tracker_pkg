from multiprocessing import Pool, cpu_count

import pandas as pd
import time
import requests
import datetime
import json
from tqdm import tqdm

from .ArXivTrainingData import ArXivTrainingData
from .ArXivArticleItem import ArXivArticleItem
from .CrossRefUtils import CrossRefUtils
# from .RateLimiter import RateLimiter
from ..CrossRef import CrossRef

from .config import Config as config


import logging
logger = logging.getLogger(__name__)


class CrossRefSearch():
    """
    Given ArXiv OAI-PMH data, this class handles
    searches for similar articles in CrossRef
    """
    def __init__(self, items):
        """
        :param items: List of JSON ArXiv OAI-PMH records.
        """
        # self.api_rate_limiter = RateLimiter(1)
        self.items = items


    def pre_process_items(self, items):
        """
        CrossRef search fails with long author lists
        - limit author list length
        """
        allowed_length = 10
        pre_items = []
        for item in items:
            authors = item.get('authors','')
            # convert author list (str) to list type
            auth_ls = authors.split(', ')
            if type(auth_ls)==list and len(auth_ls)>allowed_length:
                auth_ls = auth_ls[:allowed_length]
            authors = ', '.join(auth_ls)
            item['authors'] = authors
            pre_items.append(item)
        return pre_items


    def search_items(self):
        """
        Multithread search function for batches
        Here we are searching for article metadata much like we would when
        doing a rejected article search. 
        """
        logger = logging.getLogger(__name__).getChild(self.__class__.__name__)
        # all_search_results = dict()
        chunk_size = 50

        for chunk in CrossRefUtils().chunks(self.items, chunk_size):
            # next(self.api_rate_limiter)
            chunk = self.pre_process_items(items=chunk)

            # handle failures
            # only retry once in case it's a nuisance to the API
            try:
                all_results = self.multi(self.search_matches, chunk)
            except ConnectionError:
                logger.debug('Connection Error in CrossRef search! Retrying...')
                time.sleep(10)
                all_results = self.multi(self.search_matches, chunk)

            for article_id, search_results in all_results:
                if article_id==None or search_results==None:
                    pass
                else:
                    yield article_id, search_results
        logger.info('Searches complete.')

    def search_and_write(self):
        logger = logging.getLogger(__name__).getChild(self.__class__.__name__)
        output = self.search_items()
        
        for i, (article_id, search_results) in enumerate(output):
            line = {article_id:search_results}
            with open(config.crossref_search_jsonl_dataloc, 'a') as f:
                f.write(json.dumps(line) + "\n")


    def multi(self,f,iterable):
        """
        General function for multithreading
        :iterable: must be an object like a list. Not a generator. 
        :f: a function which operates on items in the iterator
        """
        with Pool(50) as p:
            return p.map(f, iterable)

    def search_matches(self,article):
        """
        Given single arXiv OAI-PMH record as input
        - get all of the crossref search results
        """
        logger = logging.getLogger(__name__).getChild(self.__class__.__name__)
        article = ArXivArticleItem(article).to_dict()
        article_id = article['manuscript_id']
        
        email = config.myemail
        search_results = CrossRef(article=article,
                                http_client=requests,
                                sleep=time.sleep,
                                email=email,
                                rows=2).search()

        # results[article_id] = search_results
        if search_results!=None:
            return article_id, search_results
        else:
            logger.info('Failure for {}'.format(article_id))
            return None, None



