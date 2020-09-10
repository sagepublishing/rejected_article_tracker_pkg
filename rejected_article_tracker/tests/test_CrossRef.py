import unittest
from ..src.CrossRef import CrossRef
from .Fakes import fake_http_client


class TestCrossRef(unittest.TestCase):
    def test__search(self):
        article = {
            'text_sub_date': 'Some Value',
            'manuscript_title': 'Some Value',
            'authors': 'Some+Value,Another+Value'
        }
        search_results = CrossRef(article=article, http_client=fake_http_client, sleep=None).search()
        self.assertTrue(len(search_results) > 2)
