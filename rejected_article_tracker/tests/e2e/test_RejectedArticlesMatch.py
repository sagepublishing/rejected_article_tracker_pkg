import unittest
from rejected_article_tracker.src.RejectedArticlesMatch import RejectedArticlesMatch


class TestRejectedArticlesMatch(unittest.TestCase):

    def test_valid_lookup(self):
        print('This might take a while. Doing a lookup to crossref...')
        articles = [{
            "manuscript_title": "The Impact of Childhood Abuse on the Commercial Sexual Exploitation of Youth. A Systematic Review and Meta-Analysis ",
            "authors": "De Vries, Ieke; Goggin, Kelly",
            "manuscript_id": "TVA-18-057",
            "submission_date": "2018-07-20T13:29:58.999Z",
            "decision_date": "1899-12-30T00:00:00.000Z",
            "journal_name": "Trauma, Violence, & Abuse",
            "final_decision": ""
        }]

        config = {
            "filter_dates": {'from': '2007-01-01', 'to': '2020-07-01'},
            "threshold": 70,
        }

        results = []
        RejectedArticlesMatch(
            articles=articles,
            config=config,
            email="andy.hails@sagepub.co.uk",
            results=results
        ).match()

        self.assertTrue(len(results), 1)
        self.assertNotEqual(results[0]['match_doi'], "No Match")

    def test_no_match_lookup(self):
        print('This might take a while. Doing a lookup to crossref...')
        articles = [{
            'manuscript_id': '1G',
            'journal_name': 'Some Journal',
            'manuscript_title': 'What is in a name?',
            'submission_date': '04-03-2019',
            'decision_date': '2020-05-12',
            'authors': 'Andy Hails',
            'text_sub_date': '',
            'final_decision': 'Approved'
        }]

        config = {
            "filter_dates": {'from': '2007-01-01', 'to': '2020-07-01'},
            "threshold": 70,
        }

        results = []
        RejectedArticlesMatch(
            articles=articles,
            config=config,
            email="andy.hails@sagepub.co.uk",
            results=results
        ).match()
        self.assertTrue(len(results), 1)
        self.assertEqual(results[0]['match_doi'], "No Match")

