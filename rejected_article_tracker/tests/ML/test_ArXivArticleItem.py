import unittest
import pandas as pd

from rejected_article_tracker.src.ML.ArXivArticleItem import ArXivArticleItem


class TestArXivArticleItem(unittest.TestCase):

    def test_object_creation_with_required_fields(self):
        items = {
            'id': '0606.1234v2',
            'raw_manuscript_id': '0606.1234',
            'title': 'What is in a name?',
            'created': pd.to_datetime('2020-04-03'),
            'authors': 'Hails,Andy;Day,Adam',
            'text_sub_date': pd.to_datetime('2020-04-03').strftime("%Y-%m-%d"),
            'final_decision': pd.to_datetime('2020-04-03')
        }
        article = ArXivArticleItem(items)
        res = article.to_dict()
        self.assertEqual(res['manuscript_id'], items['id'])
        self.assertEqual(res['manuscript_title'], items['title'])
        self.assertTrue(type(res['submission_date']) == pd._libs.tslibs.timestamps.Timestamp)
        self.assertTrue(type(res['decision_date']) == pd._libs.tslibs.timestamps.Timestamp)
        self.assertEqual(res['authors'], 'Hails,Andy;Day,Adam')
        self.assertEqual(res['text_sub_date'], '2020-04-03')
        self.assertEqual(res['final_decision'], items['final_decision'])


    def test_missing_required_field_raises_exception(self):
        with self.assertRaises(ValueError) as cm:
            items = {'id': '', 
                    'created': pd.to_datetime('2020-03-04', utc=True)}
            ArXivArticleItem(items)
        the_exception = cm.exception
        self.assertEqual(str(the_exception), 'field "id" required')


    def test_no_submission_date_raises_exception(self):
        items = {
            'id': '1',
            'title': 'What is in a name?',
            'created': '',
        }
        with self.assertRaises(ValueError) as cm:
            ArXivArticleItem(items)
        the_exception = cm.exception
        self.assertEqual(str(the_exception), 'field "created" required')


    def test_bad_submission_date_raises_exception(self):
        items = {
            'id': '1',
            'title': 'What is in a name?',
            'created': 'NOTADATE'
        }
        with self.assertRaises(ValueError) as cm:
            ArXivArticleItem(items)

        the_exception = cm.exception
        self.assertEqual(str(the_exception), 'could not convert string to Timestamp') #"created" needs to be a valid date')

