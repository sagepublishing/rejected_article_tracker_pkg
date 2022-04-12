import unittest
from rejected_article_tracker.src.RejectedArticlesMatch import RejectedArticlesMatch

config = {
    "threshold": 0.5,
    "max_results_per_article":10
}


class TestRejectedArticlesMatch(unittest.TestCase):

    def test_valid_lookup(self):
        print('test_valid_lookup')
        print('This might take a while. Doing a lookup to crossref...')
        articles = [{
            "manuscript_title": """Rural Business Hub: Framework for a New Rural Development Approach in Rain-Fed Areas of Pakistan—A Case of Punjab Province """,
            'title_for_search': """Rural Business Hub: Framework for a New Rural Development Approach in Rain-Fed Areas of Pakistan—A Case of Punjab Province """,
            "authors": "Baig, Irfan Ahmad; Ahmad, Rai Niaz; Baig, Sajjad Ahmad; Asghar Ali",
            "manuscript_id": "ABC-12-0987",
            "submission_date": "2018-07-02T00:00:00Z",
            "decision_date": "1899-12-30T00:00:00.000Z",
            "journal_name": "SAGE Open",
            "final_decision": ""
        }]

        results = []
        RejectedArticlesMatch(
            articles=articles,
            config=config,
            email="andy.hails@sagepub.co.uk",
            results=results
        ).match()

        self.assertTrue(len(results)==1, 1)
        self.assertNotEqual(results[0]['match_doi'], "No Match")

    def test_no_match_lookup(self):
        print('test_no_match_lookup')
        print('This might take a while. Doing a lookup to crossref...')
        articles = [{
            'manuscript_id': '1G--CI_TEST_ENV',
            'journal_name': 'Some Journal',
            'manuscript_title': 'What is in a name?',
            'title_for_search':'what name?',
            'submission_date': '04-03-2019',
            'decision_date': '2020-05-12',
            'authors': 'Andy Hails',
            'text_sub_date': '',
            'final_decision': 'Approved'
        }]

        results = []
        RejectedArticlesMatch(
            articles=articles,
            config=config,
            email="andy.hails@sagepub.co.uk",
            results=results
        ).match()
        self.assertTrue(len(results)==1, f"{results}")
        self.assertEqual(results[0]['match_doi'], "No Match")
