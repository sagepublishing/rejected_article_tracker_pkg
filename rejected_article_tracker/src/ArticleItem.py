import pandas as pd
from .AuthorNames import AuthorNames
from .ManuscriptIdRaw import ManuscriptIdRaw


class ArticleItem:

    def __init__(self, article_dict):
        """
        :param article_dict: dict
            manuscript_id: str
            journal_name: str
            manuscript_title: str
            submission_date: str    Most date formats will work.
            decision_date: str      Most date formats will work.
            authors: str            Semi-colon-separated list of names in the format:
                                    "{last name}, {first_names}; {last name}, {first_names}"
                                    e.g.  "De Vries, Ieke; Goggin, Kelly"
            final_decision: str
        """
        submission_date = self.__required(article_dict, 'submission_date')

        if not isinstance(submission_date, pd.Timestamp):
            raise ValueError('"submission_date" needs to be a valid date')

        self.article_dict = {
            'manuscript_id': self.__required(article_dict, 'manuscript_id'),
            'raw_manuscript_id': ManuscriptIdRaw(article_dict['manuscript_id']).id(),
            'journal_name': self.__required(article_dict, 'journal_name'),
            'manuscript_title': self.__required(article_dict, 'manuscript_title'),
            'submission_date': submission_date,
            'decision_date': article_dict['decision_date'],
            'authors': AuthorNames(article_dict['authors']).names(),
            'text_sub_date': article_dict['submission_date'].strftime("%Y-%m-%d"),
            'final_decision': article_dict['final_decision']
        }

    def to_dict(self):
        return self.article_dict

    @staticmethod
    def __required(article_dict, name):
        if not article_dict[name]:
            raise ValueError('field "' + name + '" required')
        return article_dict[name]

