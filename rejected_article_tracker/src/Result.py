import pandas as pd


class Result:
    def __init__(self, original, winner):
        self.original = original
        self.winner = winner

    def to_dict(self):
        earliest_date = self.earliest_date()
        n_days = self.n_days_for_decision(earliest_date, self.original['decision_date'])
        result = {
            "submission_date": self.original["submission_date"].strftime("%Y-%m-%d"),
            "decision_date": self.decision_date(),
            "match_doi": self.winner['DOI'] if 'DOI' in self.winner else '',
            "match_type": self.winner['type'].strip() if 'type' in self.winner else '',
            "match_title": self.winner['title'][0].strip(),
            "match_authors": ", ".join(self.winner['authors_list']),
            "match_publisher": self.winner["publisher"],
            "match_journal": self.journal_title(),
            "match_pub_date": '-'.join(str(x) for x in self.winner['issued']['date-parts'][0]),
            "match_earliest_date": earliest_date.strftime("%Y-%m-%d"),
            "match_similarity": self.winner["similarity"],
            "match_one": self.winner['author_match_one'],
            "match_all": self.winner['author_match_all'],
            "match_crossref_score": self.winner['score'],
            "match_crossref_cites": self.winner['is-referenced-by-count'],
            "match_rank": self.winner['rank'],
            "match_total_decision_days": n_days.days if hasattr(n_days, 'days') else 0,
            "match_journal_acronym": self.journal_acronym(self.original['manuscript_id'])
        }
        self.original.update(result)
        return self.original

    def decision_date(self):
        if isinstance(self.original["decision_date"], pd.Timestamp):
            return self.original["decision_date"].strftime("%Y-%m-%d")
        return ""

    def journal_title(self):
        return self.winner['container-title'][0].strip() if 'container-title' in self.winner else ''

    def earliest_date(self) -> pd.Timestamp:
        """
        Given a crossref works record, find the earliest date.
        """
        tags = ['issued', 'created', 'indexed', 'deposited']
        stamps = []
        for tag in tags:
            if tag in self.winner and 'timestamp' in self.winner[tag]:
                stamps.append(int(self.winner[tag]['timestamp']))

        t_stamp = min(stamps)
        return pd.to_datetime(t_stamp, unit='ms', utc=True)

    @staticmethod
    def n_days_for_decision(earliest_date, decision_date):
        return earliest_date - decision_date if isinstance(decision_date, pd.Timestamp) else ''

    @staticmethod
    def journal_acronym(journal_id):
        return journal_id[:journal_id.find('-')]
