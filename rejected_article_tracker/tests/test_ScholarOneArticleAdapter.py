import unittest
from ..src.ScholarOneArticleAdapter import ScholarOneArticleAdapter


class TestScholarOneArticleAdapter(unittest.TestCase):

    def test_adapter_adapts(self):
        article = {
            "Manuscript Title": 'What is in a name?',
            "Author Names": 'Andy Hails; Adam Day',
            "Manuscript ID": "1G",
            "Submission Date": '04-03-2019',
            "Decision Date": '2020-05-12',
            "Journal Name": "Some Journal",
            "Accept or Reject Final Decision": "Approved",
        }

        res = ScholarOneArticleAdapter.adapt(article=article)
        self.assertEqual(res["manuscript_title"], article["Manuscript Title"])
        self.assertEqual(res["authors"], article["Author Names"])
        self.assertEqual(res["manuscript_id"], article['Manuscript ID'])
        self.assertEqual(res["submission_date"], article['Submission Date'])
        self.assertEqual(res["decision_date"], article['Decision Date'])
        self.assertEqual(res["journal_name"], article['Journal Name'])
        self.assertEqual(res["final_decision"], article['Accept or Reject Final Decision'])

