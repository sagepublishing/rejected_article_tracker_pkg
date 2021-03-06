import unittest
from ..src.BestCandidate import BestCandidate


class TestBestCandidate(unittest.TestCase):

    def test__find_best_candidate(self):
        candidates = [
            {
                'id': 1,
                'similarity': 90,
                'classifier_score': 85,
                'author_match_one': 1
            },
            {
                'id': 2,
                'similarity': 95,
                'classifier_score': 95,
                'author_match_one': 1
            }
        ]
        winner = BestCandidate(candidates=candidates, threshold=70).find()
        self.assertTrue(winner['id'], 2)

    def test__low_score_candidate_removed(self):
        candidates = [
            {
                'id': 1,
                'similarity': 40,
                'classifier_score': 60,
                'author_match_one': 1
            },
            {
                'id': 2,
                'similarity': 55,
                'classifier_score': 50,
                'author_match_one': 1
            }
        ]
        winner = BestCandidate(candidates=candidates, threshold=70).find()
        self.assertIsNone(winner)

    def test___no_matching_author_candidate_removed(self):
        candidates = [
            {
                'id': 1,
                'similarity': 80,
                'classifier_score': 90,
                'author_match_one': 0
            },
            {
                'id': 2,
                'similarity': 95,
                'classifier_score': 95,
                'author_match_one': 0
            }
        ]
        winner = BestCandidate(candidates=candidates, threshold=70).find()
        self.assertIsNone(winner)
