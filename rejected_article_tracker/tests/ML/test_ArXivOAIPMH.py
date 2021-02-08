import unittest
import os
import shutil
import glob

from ...src.ML.ArXivOAIPMH import ArXivOAIPMH


class TestArXivOAIPMH(unittest.TestCase):

    def test_get_xml_filepaths(self):
        """
        Check to see that we are indeed yielding XML filepaths
        """
        
        xml_filepaths = ArXivOAIPMH().get_xml_filepaths()
        if len(xml_filepaths)>0:
            self.assertTrue(all(xml_filepath[-4:]=='.xml' for xml_filepath in xml_filepaths))

    # def test_acquire_oai_pmh(self):
    #     """
    #     This test works ok, but I'm not comfortable with automating
    #     file-deletion, so commenting out. 
    #     """

    #     user_home_dir = os.path.expanduser('~')
    #     datadir = os.path.join(user_home_dir,'tmp_oai_data_deleteme')
    #     if not os.path.exists(datadir):
    #         os.mkdir(datadir)
    #     nRecs = 10

    #     result = ArXivOAIPMH().acquire_oai_pmh( 
    #                             datadir = datadir, 
    #                             nRecs = nRecs)

    #     contents = glob.glob(datadir+'/*')
        
    #     self.assertEqual(len(contents),nRecs)
    #     shutil.rmtree(datadir)
    #     self.assertFalse(os.path.exists(datadir))


    def test_yield_xml(self):
        """
        Check that XML docs are being yielded
        """
        xml_filepaths = ArXivOAIPMH().get_xml_filepaths()
        # first check that we actually have data in the directory. 
        if len(xml_filepaths)>0:
            xml_generator = ArXivOAIPMH().yield_xml()

            first3 = []
            for i, doc in enumerate(xml_generator):
                first3.append(doc)
                if i>=2:
                    break
            self.assertTrue(type(doc)==str
                            and '<id>' in doc 
                            and '</arXiv>' in doc 
                            for doc in first3)

    def test_yield_json(self):
        """
        Check that XML docs are being converted to dicts with an 'id' field
        """
        xml_filepaths = ArXivOAIPMH().get_xml_filepaths()
        # first check that we actually have data in the directory. 
        if len(xml_filepaths)>0:
            json_generator = ArXivOAIPMH().yield_json()

            first3 = []
            for i, doc in enumerate(json_generator):
                first3.append(doc)
                if i>=2:
                    break
            self.assertTrue(type(doc)==dict and 'id' in doc for doc in first3)
                