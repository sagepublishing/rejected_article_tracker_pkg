import unittest
from ..src.FilteredArticles import FilteredArticles


class TestFilteredArticles(unittest.TestCase):

    def test_object_creation_with_valid_item(self):
        articleItems = [{
            'manuscript_id': '1G',
            'journal_name': 'Some Journal',
            'manuscript_title': 'What is in a name?',
            'submission_date': '04-03-2019',
            'decision_date': '2020-05-12',
            'authors': 'Andy Hails; Adam Day',
            'text_sub_date': '',
            'final_decision': 'Approved'
        }]

        filter_dates = {'from': '2007-01-01', 'to': '2020-07-07'}
        articles = FilteredArticles(articles=articleItems, filter_dates=filter_dates)
        self.assertTrue(len(articles.to_dict()), 1)

    def test_object_creation_with_invalid_item(self):
        articleItems = [{
            'manuscript_id': '1G',
            'journal_name': 'Some Journal',
            'manuscript_title': 'What is in a name?',
            'submission_date': '04-03-1999',
            'decision_date': '2001-05-12',
            'authors': 'Andy Hails; Adam Day',
            'text_sub_date': '',
            'final_decision': 'Approved'
        }]

        filter_dates = {'from': '2007-01-01', 'to': '2020-07-07'}
        articles = FilteredArticles(articles=articleItems, filter_dates=filter_dates)
        self.assertTrue(len(articles.to_dict()) == 0)
