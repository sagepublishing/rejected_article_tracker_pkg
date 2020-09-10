import unittest
import pandas as pd
from ..src.Result import Result


class TestResult(unittest.TestCase):
    def test__to_dict(self):
        original = {
            "manuscript_id": 'TVA-18-057',
            "decision_date": pd.to_datetime("2020-09-01", errors='coerce', utc=True),
            "submission_date": pd.to_datetime("2020-08-01", errors='coerce', utc=True),
        }

        winner = {
            'DOI': '10.1016/j.jnt.2017.08.038',
            'type': 'journal-article',
            'title': ['New data on the Opheliidae (Annelida) from Lizard Island (Great Barrier Reef, Australia)'],
            'authors_list': ['Andy Hails', 'Adam Day'],
            'publisher': 'SAGE',
            'issued': {'date-parts': [[2020, 4, 1]], 'timestamp': 1585730172000},
            'created': {'date-parts': [[2018, 4, 23]], 'timestamp': 1524472572000},
            'indexed': {'date-parts': [[2018, 9, 1]], 'timestamp': 1535790972000},
            'deposited': {'date-parts': [[2018, 9, 1]], 'timestamp': 1535790972000},
            'similarity': 97,
            'author_match_one': True,
            'author_match_all': True,
            'score': 95.2,
            'is-referenced-by-count': 3,
            'rank': 1,
            'container-title': [
                'Taxes and Taxation Trends'
            ]

        }

        res = Result(original=original, winner=winner).to_dict()
        self.assertEqual(res['manuscript_id'], original['manuscript_id'])
        self.assertEqual(res['decision_date'], '2020-09-01')
        self.assertEqual(res['submission_date'], '2020-08-01')
        self.assertEqual(res['match_doi'], winner['DOI'])
        self.assertEqual(res['match_type'], winner['type'])
        self.assertEqual(res['match_title'], winner['title'][0])
        self.assertEqual(res['match_authors'], 'Andy Hails, Adam Day')
        self.assertEqual(res['match_publisher'], 'SAGE')
        self.assertEqual(res['match_journal'], 'Taxes and Taxation Trends')
        self.assertEqual(res['match_pub_date'], '2020-4-1')
        self.assertEqual(res['match_earliest_date'], '2018-04-23')
        self.assertEqual(res['match_similarity'], 97)
        self.assertEqual(res['match_one'], True)
        self.assertEqual(res['match_all'], True)
        self.assertEqual(res['match_crossref_score'], 95.2)
        self.assertEqual(res['match_crossref_cites'], 3)
        self.assertEqual(res['match_rank'], 1)
        self.assertEqual(res['match_total_decision_days'], -862)
        self.assertEqual(res['match_journal_acronym'], 'TVA')

    def test__missing_values(self):
        original = {
            "manuscript_id": 'TVA-18-057',
            "decision_date": "2020-09-01",
            "submission_date": pd.to_datetime("2020-08-01", errors='coerce', utc=True),
        }

        winner = {
            'DOI': '10.1016/j.jnt.2017.08.038',
            'type': 'journal-article',
            'title': ['New data on the Opheliidae (Annelida) from Lizard Island (Great Barrier Reef, Australia)'],
            'authors_list': ['Andy Hails', 'Adam Day'],
            'publisher': 'SAGE',
            'issued': {'date-parts': [[2018, 9, 1]], 'timestamp': 1535790972000},
            'similarity': 97,
            'author_match_one': True,
            'author_match_all': True,
            'score': 95.2,
            'is-referenced-by-count': 3,
            'rank': 1,
            'container-title': [
                'Taxes and Taxation Trends'
            ]

        }

        res = Result(original=original, winner=winner).to_dict()
        self.assertEqual(res['decision_date'], '')

