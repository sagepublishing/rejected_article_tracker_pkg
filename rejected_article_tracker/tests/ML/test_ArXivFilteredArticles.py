import unittest
from rejected_article_tracker.src.ML.ArXivFilteredArticles import ArXivFilteredArticles


class ArXivTestFilteredArticles(unittest.TestCase):

    def test_object_creation_with_valid_item(self):
        article_items = [{
            'id': '1234.0012v2',
            'title': 'What is in a name?',
            'created': '04-03-2019',
            'submission_date': '2020-05-12',
            'decision_date': '2020-05-12',
            'authors': 'Andy Hails; Adam Day',
            'text_sub_date': '',
            'final_decision':''
        }]

        articles = ArXivFilteredArticles(articles=article_items)
        self.assertTrue(len(articles.to_dict()), 1)
