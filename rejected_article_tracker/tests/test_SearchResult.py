import unittest


from ..src.SearchResult import SearchResult
from .Fakes import fake_classifier


def make_dummy_search_result():
    return SearchResult(
            query_article = {},
            match_article = {},
            clf = None,
            rank = 0
        )


class TestSearchResult(unittest.TestCase):

    
    def test__match_names__any(self):
        query_authors = 'Andy Carlos+Hails, Helen+King, Adam+Day, D+Harris'
        match_authors = ['Helen+King', 'Adam+Day', 'D+Harris']
        dummy_search_result = make_dummy_search_result()
        matches = dummy_search_result.match_names(match_authors=match_authors, 
                                                query_authors=query_authors)
        self.assertEqual(matches['author_match_one'],1)
        self.assertEqual(matches['author_match_all'],0)

    def test__match_names__all(self):
        query_authors = 'Andy Carlos+Hails, Helen+King, Adam+Day, D+Harris'
        match_authors = ['Helen+King', 'Adam+Day', 'D+Harris', 'Andy Carlos+Hails']
        dummy_search_result = make_dummy_search_result()
        matches = dummy_search_result.match_names(match_authors=match_authors, 
                                                 query_authors=query_authors)
        self.assertEqual(matches['author_match_one'],1)
        self.assertEqual(matches['author_match_all'],1)

    def test__match_names__none(self):
        query_authors = 'Simon+Jones'
        match_authors = ['Helen+King', 'Adam+Day', 'D+Harris']
        dummy_search_result = make_dummy_search_result()
        matches = dummy_search_result.match_names(match_authors=match_authors, 
                                                 query_authors=query_authors)
        self.assertEqual(matches['author_match_one'],0)
        self.assertEqual(matches['author_match_all'],0)

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
        query_article = {
            'manuscript_id':'fake_ms_id',
            'authors': 'Andy Carlos+Hails, Helen+King, Adam+Day, D+Harris',
            'manuscript_title': 'Some Manuscript title'
        }
        match_article = {
            'title': 'Some manuscript title',
            'author': [{
                'given': 'Andy',
                'family': 'Hails',
                'sequence': 'first',
                'affiliation': []
            }],
            'score': '76'
        }
        candidate = SearchResult(query_article=query_article, 
                                match_article=match_article, 
                                clf=fake_classifier, 
                                rank=10)
        res = candidate.to_dict()
        self.assertEqual(res['classifier_score'], 99.999)

