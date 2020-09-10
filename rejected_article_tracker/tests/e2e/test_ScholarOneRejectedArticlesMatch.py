import unittest
from rejected_article_tracker.src.ScholarOneRejectedArticlesMatch import ScholarOneRejectedArticlesMatch


class TestScholarOneRejectedArticlesMatch(unittest.TestCase):
    def test_valid_lookup(self):
        print('This might take a while. Doing a lookup to crossref...')
        articles = [{
            "Manuscript Title": "The Impact of Childhood Abuse on the Commercial Sexual Exploitation of Youth. A Systematic Review and Meta-Analysis ",
            "Author Names": "De Vries, Ieke; Goggin, Kelly",
            "Manuscript ID": "TVA-18-057",
            "Submission Date": "2018-07-20T13:29:58.999Z",
            "Decision Date": "1899-12-30T00:00:00.000Z",
            "Journal Name": "Trauma, Violence, & Abuse",
            "Accept or Reject Final Decision": ""
        }]

        config = {
            "filter_dates": {'from': '2007-01-01', 'to': '2020-07-01'},
            "threshold": 70,
        }

        results = []
        ScholarOneRejectedArticlesMatch(
            articles=articles,
            config=config,
            email="andy.hails@sagepub.co.uk",
            results=results
        ).match()

        self.assertTrue(len(results), 1)
        self.assertNotEqual(results[0]['match_doi'], "No Match")

