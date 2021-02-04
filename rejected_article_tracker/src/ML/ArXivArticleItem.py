import pandas as pd
from .ArXivAuthorNames import ArXivAuthorNames
from .ArXivManuscriptIdRaw import ArXivManuscriptIdRaw


class ArXivArticleItem:

    def __init__(self, items):
        """
        :param items: dict
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
        created_date = self.__required(items, 'created')
        created_date = pd.Timestamp(created_date)
        if not isinstance(created_date, pd.Timestamp):
            raise ValueError('"created" needs to be a valid date')

        self.items = {
            'manuscript_id': self.__required(items, 'id'),
            'raw_manuscript_id': ArXivManuscriptIdRaw(items['id']).id(),
            # 'journal_name': self.__required(items, 'journal_name'),
            'manuscript_title': self.__required(items, 'title'),
            'submission_date': created_date,
            'decision_date': created_date,
            'authors': items['authors'],
            'text_sub_date': created_date.strftime("%Y-%m-%d"),
            'final_decision': created_date
            }

    def to_dict(self):
        return self.items

    @staticmethod
    def __required(items, name):
        if not items[name]:
            raise ValueError('field "' + name + '" required')
        return items[name]

