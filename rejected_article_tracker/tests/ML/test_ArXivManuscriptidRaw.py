import unittest
from ...src.ML.ArXivManuscriptIdRaw import ArXivManuscriptIdRaw


class TestArXivManuscriptIdRaw(unittest.TestCase):
    def test__id_split(self):
        _id = ArXivManuscriptIdRaw('1201.0001v3').id()
        self.assertEqual(_id, '1201.0001')


    def test__id_no_split(self):
        _id = ArXivManuscriptIdRaw('1201.0001').id()
        self.assertEqual(_id, '1201.0001')
