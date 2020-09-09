import unittest
import pandas as pd
from .src.EmptyResult import EmptyResult


class TestEmptyResult(unittest.TestCase):
    def test__to_dict(self):
        original = {
            "manuscript_id": 'TVA-18-057',
            "decision_date": pd.to_datetime("2020-09-01", errors='coerce', utc=True),
            "submission_date": pd.to_datetime("2020-08-01", errors='coerce', utc=True),
        }

        res = EmptyResult(original=original).to_dict()
        self.assertEqual(res['manuscript_id'], original['manuscript_id'])
        self.assertEqual(res['decision_date'], '2020-09-01')
        self.assertEqual(res['submission_date'], '2020-08-01')
        self.assertEqual(res['match_doi'], 'No Match')
        self.assertEqual(res['match_type'], 'No Match')
        self.assertEqual(res['match_title'], 'No Match')
        self.assertEqual(res['match_authors'], 'No Match')
        self.assertEqual(res['match_publisher'], 'No Match')
        self.assertEqual(res['match_journal'], 'No Match')
        self.assertEqual(res['match_pub_date'], 'No Match')
        self.assertEqual(res['match_earliest_date'], 'No Match')
        self.assertEqual(res['match_similarity'], 'No Match')
        self.assertEqual(res['match_one'], 'No Match')
        self.assertEqual(res['match_all'], 'No Match')
        self.assertEqual(res['match_crossref_score'], 'No Match')
        self.assertEqual(res['match_crossref_cites'], 'No Match')
        self.assertEqual(res['match_rank'], 'No Match')
        self.assertEqual(res['match_total_decision_days'], 'No Match')
        self.assertEqual(res['match_journal_acronym'], 'No Match')

    def test__empty_Decision(self):
        original = {
            "decision_date": '',
            "submission_date": pd.to_datetime("2020-08-01", errors='coerce', utc=True),
        }

        res = EmptyResult(original=original).to_dict()
        self.assertEqual(res['decision_date'], '')
