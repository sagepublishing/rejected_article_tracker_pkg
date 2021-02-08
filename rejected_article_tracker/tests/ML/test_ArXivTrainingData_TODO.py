import unittest
import os
import shutil
import glob

from ...src.ML.ArXivTrainingData import ArXivTrainingData

# not sure if there's a need to test these fns.
# they are simple fns

class TestArXivTrainingData(unittest.TestCase):

    def test_clean_df(self):
        pass