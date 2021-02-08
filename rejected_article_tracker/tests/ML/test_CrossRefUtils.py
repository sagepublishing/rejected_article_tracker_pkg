import unittest
from rejected_article_tracker.src.ML.CrossRefUtils import CrossRefUtils

from rejected_article_tracker.tests.Fakes.FakeCrossRefResponse import FakeGoodListCrossRefResponse, FakeGoodSingleCrossRefResponse, FakeBadCrossRefResponse2, FakeBadCrossRefResponse1




class TestCrossRefUtils(unittest.TestCase):

    def test_chunks(self):
        l = list(range(1,223))
        max_size = 100
        for x in CrossRefUtils().chunks(l,max_size):
            assert type(x)==list
            assert len(x)<=max_size

    def test_validate_response(self):
        doc1 = FakeGoodListCrossRefResponse()
        doc2 = FakeGoodSingleCrossRefResponse()
        doc3 = FakeBadCrossRefResponse1()
        doc4 = FakeBadCrossRefResponse2()

        self.assertTrue(CrossRefUtils().validate_response(doc1))
        self.assertTrue(CrossRefUtils().validate_response(doc2))
        self.assertFalse(CrossRefUtils().validate_response(doc3))
        self.assertFalse(CrossRefUtils().validate_response(doc4))

        # should check for typeError?
        # with self.assertRaises(TypeError) as x:
        #     CrossRefUtils().validate_response(doc4)
        # exception = 