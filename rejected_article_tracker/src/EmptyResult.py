import pandas as pd


class EmptyResult:
    def __init__(self, original):
        self.original = original

    def to_dict(self):
        empty = {
            "submission_date": self.original["submission_date"].strftime("%Y-%m-%d"),
            "decision_date": self.decision_date(),
            "match_doi": "No Match",
            "match_type": "No Match",
            "match_title": "No Match",
            "match_authors": "No Match",
            "match_publisher": "No Match",
            "match_journal": "No Match",
            "match_pub_date": "No Match",
            "match_earliest_date": "No Match",
            "match_similarity": "No Match",
            "match_one": "No Match",
            "match_all": "No Match",
            "match_crossref_score": "No Match",
            "match_crossref_cites": "No Match",
            "match_rank": "No Match",
            "match_total_decision_days": "No Match",
            "match_journal_acronym": "No Match"
        }
        self.original.update(empty)
        return self.original

    def decision_date(self):
        if isinstance(self.original["decision_date"], pd.Timestamp):
            return self.original["decision_date"].strftime("%Y-%m-%d")
        return ""

