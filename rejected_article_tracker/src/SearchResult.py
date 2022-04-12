from fuzzywuzzy import fuzz
import numpy as np
from gensim.parsing.preprocessing import preprocess_string, strip_tags
from gensim.utils import deaccent

from .ML.config import Config as mlconfig


class SearchResult:
    def __init__(self, match_article: dict, query_article: dict,  clf, rank: int):
        """
        :param match_article: Article details from search provider (e.g. CrossRef)
        :param query_article: The input article (e.g. from the user)
        :param clf: The classifier to score how similar the articles are.
        :param rank:
        """
        self.query_article = query_article
        self.match_article = match_article
        self.clf = clf
        self.rank = rank

    def to_dict(self) -> dict:
        match_article = self.match_article
        match_article['manuscript_id'] = self.query_article['manuscript_id']
        # add # of authors on the query article. This might affect model confidence?
        match_article['n_auths_query'] = len(self.query_article['authors'].split(','))
        match_article['authors_list'] = self.authors_list(match_article.get('author',''))
        match_article.update(self.match_names(
                                        query_authors=self.query_article['authors'], 
                                        match_authors=self.match_article['authors_list']
                                        )
                            )
        match_article['similarity'] = fuzz.ratio(self.query_article['manuscript_title'],
                                           match_article['title']) if 'title' in match_article else 0
        match_article['classifier_score'] = self.classify(match_article)
        match_article['rank'] = self.rank
        return match_article

    @staticmethod
    def authors_list(authors: list) -> list:
        match_authors = []
        for author in authors:
            given = author.get('given', '')
            family = author.get('family', '')
            match_authors.append(given + '+' + family)
        return match_authors

    def pre_process_name(self, name):
        """
        Takes a string as input, removes accents and 
        converts to lowercase
        """
        if type(name)==str and len(name)>0:
            name = deaccent(name)
            name = name.lower()
            first_name = name[0]
            if '+' in name:
                last_name = name[name.rfind('+') + 1:]
            else:
                last_name = name[1:]
            first_name = first_name.replace('.','').replace('-','').replace('\'','').replace(' ','')
            first_init = first_name[0] if len(first_name)>0 else ''
            last_name = last_name.replace('.','').replace('-','').replace('\'','').replace(' ','')
            name = (first_init, last_name)
            return name

    # @staticmethod
    def match_names(self, match_authors, query_authors):
        """
        Checks to see if one or all names in the query article are found
        in the match article returned by the search.
        """
        query_names = list()
        for query_name in query_authors.split(','):
            query_name = query_name.strip()
            query_name = self.pre_process_name(query_name)
            query_names.append(query_name)
        
        match_names = list()
        for match_name in match_authors:
            match_name = self.pre_process_name(match_name)
            match_names.append(match_name)
        
        match_names_set = set(match_names)

        return {
            'author_match_one': int(any(query_name in match_names_set for query_name in query_names)),
            'author_match_all': int(all(query_name in match_names_set for query_name in query_names)),
        }

    def classify(self, match_article: dict):
        predictor_cols = mlconfig.predictor_cols
        predictors = [match_article[x] for x in predictor_cols]
        X = np.array([float(x) for x in predictors])
        clf_scores = self.clf.predict_proba(np.reshape(X, (1, len(predictor_cols))))
        score = clf_scores[0][1]
        return score
