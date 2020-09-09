

class ScholarOneArticleAdapter:

    @staticmethod
    def adapt(article):
        return {
            "manuscript_title": article["Manuscript Title"],
            "authors": article["Author Names"],
            "manuscript_id": article["Manuscript ID"],
            "submission_date": article["Submission Date"],
            "decision_date": article["Decision Date"],
            "journal_name": article["Journal Name"],
            "final_decision": article["Accept or Reject Final Decision"],
        }