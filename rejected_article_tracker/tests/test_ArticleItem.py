import unittest
import pandas as pd

from ..src.ArticleItem import ArticleItem


class TestArticleItem(unittest.TestCase):

    def test_object_creation_with_required_fields(self):
        items = {
            'manuscript_id': '1',
            'journal_name': 'Some Journal;',
            'manuscript_title': 'What is in a name?',
            'submission_date': pd.to_datetime('2020-04-03'),
            'decision_date': pd.to_datetime('2020-05-12'),
            'authors': 'Hails,Andy;Day,Adam',
            'text_sub_date': '',
            'final_decision': 'Approved'
        }
        article = ArticleItem(items)
        res = article.to_dict()
        self.assertEqual(res['manuscript_id'], items['manuscript_id'])
        self.assertEqual(res['journal_name'], items['journal_name'])
        self.assertEqual(res['manuscript_title'], items['manuscript_title'])
        self.assertTrue(type(res['submission_date']) == pd._libs.tslibs.timestamps.Timestamp)
        self.assertTrue(type(res['decision_date']) == pd._libs.tslibs.timestamps.Timestamp)
        self.assertEqual(res['authors'], 'Andy+Hails, Adam+Day')
        self.assertEqual(res['text_sub_date'], '2020-04-03')
        self.assertEqual(res['final_decision'], items['final_decision'])


    def test_missing_required_field_raises_exception(self):
        with self.assertRaises(ValueError) as cm:
            ArticleItem({'manuscript_id': '', 'submission_date': pd.to_datetime('2020-03-04', utc=True)})
        the_exception = cm.exception
        self.assertEqual(str(the_exception), 'field "manuscript_id" required')


    def test_no_submission_date_raises_exception(self):
        items = {
            'manuscript_id': '1',
            'journal_name': 'Some Journal;',
            'manuscript_title': 'What is in a name?',
            'submission_date': '',
        }
        with self.assertRaises(ValueError) as cm:
            ArticleItem(items)
        the_exception = cm.exception
        self.assertEqual(str(the_exception), 'field "submission_date" required')


    def test_bad_submission_date_raises_exception(self):
        items = {
            'manuscript_id': '1',
            'journal_name': 'Some Journal;',
            'manuscript_title': 'What is in a name?',
            'submission_date': 'NOTADATE'
        }
        with self.assertRaises(ValueError) as cm:
            ArticleItem(items)

        the_exception = cm.exception
        self.assertEqual(str(the_exception), '"submission_date" needs to be a valid date')

