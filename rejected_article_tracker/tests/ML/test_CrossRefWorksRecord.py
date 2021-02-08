import unittest
from ...src.ML.CrossRefWorksRecord import CrossRefWorksRecord

from ..Fakes.FakeCrossRefResponse import FakeGoodListCrossRefResponse, FakeGoodSingleCrossRefResponse, FakeBadCrossRefResponse2, FakeBadCrossRefResponse1

class TestCrossRefWorksRecord(unittest.TestCase):

    def testGoodListResp(self):
        response = FakeGoodListCrossRefResponse()
        works_record = response.json()['message']['items'][0]
        self.assertEqual(type(CrossRefWorksRecord(works_record).works_record),dict)
        
    def testGoodSingleResp(self):
        response = FakeGoodSingleCrossRefResponse()
        works_record = response.json()['message']
        self.assertEqual(type(CrossRefWorksRecord(works_record).works_record),dict)

    # tests for bad docs required? 
    # these should be filtered out?
    # def testBadResp1(self):
    #     response = FakeBadCrossRefResponse1
    #     works_record = response().json()
    #     self.AssertEqual(type(CrossRefWorksRecord(works_record).works_record)==dict)

    # def testBadResp2(self):
    #     response = FakeBadCrossRefResponse2
    #     works_record = response().json()
        
            