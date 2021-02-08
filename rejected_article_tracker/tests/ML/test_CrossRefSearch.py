import unittest
from ...src.ML.CrossRefSearch import CrossRefSearch

from ..Fakes.FakeOAIPMHData import FakeOAIPMHData

class TestCrossRefSearch(unittest.TestCase):

    def test_search_matches(self):
        items = [FakeOAIPMHData.fake_clean_json_record]
        results = CrossRefSearch(items=items).search_matches(items[0])
        self.assertTrue(type(results[0])==str)
        self.assertTrue(type(results[1])==list)

    def test_pre_process_items(self):
        items = [FakeOAIPMHData.fake_clean_record_long_authors]
        n_auths_start = len(items[0]['authors'])
        pre_items = CrossRefSearch(items=items).pre_process_items(items)
        n_auths_end = len(pre_items[0]['authors'].split(', '))
        self.assertTrue(n_auths_start>n_auths_end)
        self.assertEqual(n_auths_end,10)