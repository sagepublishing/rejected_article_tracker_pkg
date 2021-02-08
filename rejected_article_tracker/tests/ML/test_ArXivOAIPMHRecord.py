import unittest
import os
import shutil
import glob

from ...src.ML.ArXivOAIPMHRecord import ArXivOAIPMHRecord

from ..Fakes.FakeOAIPMHData import FakeOAIPMHData



class TestArXivOAIPMHRecord(unittest.TestCase):

    def test_xml_to_json(self):
        
        json_data = ArXivOAIPMHRecord().xml_to_json(FakeOAIPMHData.fake_xml_record)
        self.assertTrue(type(json_data)==dict)
        required_fields = ['id','created','updated','authors', 'title','abstract']        
        for required_field in required_fields:
            self.assertTrue(required_field in json_data)

        # check the bad inputs
        # for bad_record in FakeOAIPMHData.fake_bad_xml_records:
        #     self.assertRaises(ValueError,ArXivOAIPMHRecord().xml_to_json(bad_record))
        
    def test_process_json(self):

        json_data = ArXivOAIPMHRecord().process_json(FakeOAIPMHData.fake_json_record)
        required_fields = ['id','created','authors', 'title','abstract']        
        for required_field in required_fields:
            self.assertTrue(required_field in json_data)

        # check the bad inputs
        # for bad_record in FakeOAIPMHData.fake_bad_json_records:
        #     self.assertRaises(ValueError, ArXivOAIPMHRecord().process_json(bad_record))

    def test_check_json(self):

        # json_data = ArXivOAIPMHRecord(xml_data).xml_to_json(xml_data)
        json_doc = FakeOAIPMHData.fake_json_record
        self.assertTrue(ArXivOAIPMHRecord().check_json(json_doc))

        for bad_record in FakeOAIPMHData.fake_bad_json_records:
            with self.assertRaises(AssertionError) as cm:
                ArXivOAIPMHRecord().check_json(bad_record)
            
            the_exception = cm.exception
            self.assertEqual(str(the_exception), '')
            

        

    def test_convert_authors(self):
        author_data = FakeOAIPMHData().fake_good_author_data
        converted_author_data = ArXivOAIPMHRecord().convert_authors(author_data)
        expected_output = 'Albert+Einstein, Marie+Curie, Ada Lovelace'
        self.assertEqual(converted_author_data,expected_output)