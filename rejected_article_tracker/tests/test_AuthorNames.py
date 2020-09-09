import unittest
from .src.AuthorNames import AuthorNames


class TestAuthorNames(unittest.TestCase):

    def test_convert_names_with_valid_items(self):
        names = AuthorNames(names_string='Hails, Andy Carlos;King, Helen;Day, Adam;Harris, D')
        self.assertEqual(names.names(), 'Andy Carlos+Hails, Helen+King, Adam+Day, D+Harris')

    def test_convert_names_with_one_item(self):
        names = AuthorNames(names_string='Andy Hails')
        self.assertEqual(names.names(), 'Andy Hails')

    def test_convert_names_fixes_too_many_whitespaces(self):
        names = AuthorNames(names_string='Hails,Andy Carlos ;   King,Helen ;Day,Adam ;Harris,D')
        self.assertEqual(names.names(), 'Andy Carlos+Hails, Helen+King, Adam+Day, D+Harris')

    def test_object_no_name_raises_error(self):
        with self.assertRaises(ValueError) as cm:
            AuthorNames('')
        the_exception = cm.exception
        self.assertEqual(str(the_exception), 'field "authors" is required')



