import unittest
from .src import SearchResult
from .Fakes import fake_classifier


class TestSearchResult(unittest.TestCase):

    def test__match_names__any(self):
        match_authors = 'Andy Carlos+Hails, Helen+King, Adam+Day, D+Harris'
        authors = ['Helen+King', 'Adam+Day', 'D+Harris']
        matches = SearchResult.match_names(match_authors=match_authors, authors=authors)
        self.assertTrue(matches['author_match_one'])
        self.assertFalse(matches['author_match_all'])

    def test__match_names__all(self):
        match_authors = 'Andy Carlos+Hails, Helen+King, Adam+Day, D+Harris'
        authors = ['Helen+King', 'Adam+Day', 'D+Harris', 'Andy Carlos+Hails']
        matches = SearchResult.match_names(match_authors=match_authors, authors=authors)
        self.assertTrue(matches['author_match_one'])
        self.assertTrue(matches['author_match_all'])

    def test__match_names__none(self):
        match_authors = 'Simon+Jones'
        authors = ['Helen+King', 'Adam+Day', 'D+Harris']
        matches = SearchResult.match_names(match_authors=match_authors, authors=authors)
        self.assertFalse(matches['author_match_one'])
        self.assertFalse(matches['author_match_all'])

    def test__match_names__fuzy(self):
        match_authors = "Ieke+De Vries; Kelly+Goggin"
        authors = ['Ieke+De Vries', 'Kelly E.+Goggin']

    def test__authors_list(self):
        authors = [
            {
                'given': 'Andy',
                'family': 'Hails',
                'sequence': 'first',
                'affiliation': []
            },
            {
                'given': 'Jim',
                'family': 'Bo',
                'sequence': 'additional',
                'affiliation': []
            },
            {
                'given': 'Sarah',
                'family': '',
                'sequence': 'additional',
                'affiliation': []
            },
            {
                'given': '',
                'family': 'Connery',
                'sequence': 'additional',
                'affiliation': []
            }
        ]
        res = SearchResult.authors_list(authors=authors)
        self.assertTrue(res[0], 'Andy+Hails')
        self.assertTrue(res[1], 'Jim+Bo')
        self.assertTrue(res[1], 'Sarah+')
        self.assertTrue(res[1], '+Connery')

    def test__classifier(self):
        match_article = {
            'authors': 'Andy Carlos+Hails, Helen+King, Adam+Day, D+Harris',
            'manuscript_title': 'Some Manuscript title'
        }
        details = {
            'title': 'Some manuscript title',
            'author': [{
                'given': 'Andy',
                'family': 'Hails',
                'sequence': 'first',
                'affiliation': []
            }],
            'score': '76'
        }
        candidate = SearchResult(details=details, match_article=match_article, clf=fake_classifier, rank=10)
        res = candidate.to_dict()
        self.assertEqual(res['classifier_score'], 99.999)