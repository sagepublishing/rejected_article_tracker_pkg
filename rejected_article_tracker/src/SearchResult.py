from fuzzywuzzy import fuzz
import numpy as np


class SearchResult:
    def __init__(self, details, match_article: dict, clf, rank: int):
        """
        :param details: Article details from search provider (e.g. CrossRef)
        :param match_article: The input article (e.g. from the user)
        :param clf: The classifier to score how similar the articles are.
        :param rank:
        """
        self.details = details
        self.match_article = match_article
        self.clf = clf
        self.rank = rank

    def to_dict(self) -> dict:
        details = self.details
        details['authors_list'] = self.authors_list(details['author'])
        details.update(self.match_names(match_authors=self.match_article['authors'], authors=details['authors_list']))
        details['similarity'] = fuzz.ratio(self.match_article['manuscript_title'],
                                           details['title']) if 'title' in details else 0
        details['classifier_score'] = self.classify(details)
        details['rank'] = self.rank
        return details

    @staticmethod
    def authors_list(authors: list) -> list:
        match_authors = []
        for author in authors:
            given = author['given'] if 'given' in author else ''
            family = author['family'] if 'family' in author else ''
            match_authors.append(given + '+' + family)
        return match_authors

    @staticmethod
    def match_names(match_authors, authors):
        names1 = [(name[0], name[name.rfind('+') + 1:]) for name in match_authors.split(', ')]
        names2 = [(name[0], name[name.rfind('+') + 1:]) for name in authors]
        return {
            'author_match_one': any(name in names2 for name in names1),
            'author_match_all': all(name in names2 for name in names1),
        }

    def classify(self, details: dict):
        items = [
            details['similarity'],
            details['author_match_all'],
            details['score'],
            self.rank,
            len(self.match_article['authors'].split(', '))
        ]
        X = np.array([float(x) for x in items])
        clf_scores = self.clf.predict_proba(np.reshape(X, (1, 5)))
        score = clf_scores[0][1]
        return score
