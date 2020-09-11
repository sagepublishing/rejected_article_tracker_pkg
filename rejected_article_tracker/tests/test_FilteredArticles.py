import unittest
from ..src.FilteredArticles import FilteredArticles


class TestFilteredArticles(unittest.TestCase):

    def test_object_creation_with_valid_item(self):
        article_items = [{
            'manuscript_id': '1G',
            'journal_name': 'Some Journal',
            'manuscript_title': 'What is in a name?',
            'submission_date': '04-03-2019',
            'decision_date': '2020-05-12',
            'authors': 'Andy Hails; Adam Day',
            'text_sub_date': '',
            'final_decision': 'Approved'
        }]

        articles = FilteredArticles(articles=article_items)
        self.assertTrue(len(articles.to_dict()), 1)
