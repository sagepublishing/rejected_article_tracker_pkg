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
        winners = BestCandidate(candidates=candidates, threshold=.5).find()
        for winner in winners:
            self.assertTrue(winner['id'], 2)

    def test__low_score_candidate_removed(self):
        candidates = [
            {
                'id': 1,
                'similarity': 99,
                'classifier_score': .49,
                'author_match_one': 1
            },
            {
                'id': 2,
                'similarity': 99,
                'classifier_score': .5,
                'author_match_one': 1
            }
        ]
        winners = BestCandidate(candidates=candidates, threshold=.5).find()
        self.assertTrue(len(winners)==1, f"{winners}")

    # def test___no_matching_author_candidate_removed(self):
    #     candidates = [
    #         {
    #             'id': 1,
    #             'similarity': 80,
    #             'classifier_score': .9,
    #             'author_match_one': 0
    #         },
    #         {
    #             'id': 2,
    #             'similarity': 95,
    #             'classifier_score': .9,
    #             'author_match_one': 1
    #         }
    #     ]
    #     winners = BestCandidate(candidates=candidates, threshold=.5).find()
    #     self.assertTrue(len(winners)==1, f"{winners}")
