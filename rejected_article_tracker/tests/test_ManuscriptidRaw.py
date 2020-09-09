import unittest
from .src.ManuscriptIdRaw import ManuscriptIdRaw


class TestManuscriptIdRaw(unittest.TestCase):
    def test__id_split(self):
        id = ManuscriptIdRaw('Dave.RGrohl').id()
        self.assertEqual(id, 'Dave')


    def test__id_no_split(self):
        id = ManuscriptIdRaw('DaveG.3rohl').id()
        self.assertEqual(id, 'DaveG.3rohl')
