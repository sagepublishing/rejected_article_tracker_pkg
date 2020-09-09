import pandas as pd
from .ArticleItem import ArticleItem
from .ManuscriptIdRaw import ManuscriptIdRaw


class FilteredArticles:
    def __init__(self, articles: list, filter_dates: dict):
        self.filter_dates = filter_dates
        self.articles = [ArticleItem(a) for a in self.__filter(articles)]

    def to_dict(self):
        return [a.to_dict() for a in self.articles]

    def __filter(self, articles):
        """
            Gets a dictionary of the appropriate articles.
            NOTE: Normally we wouldn't do such heavy CPU work on a constructor,
            but in this case we run the search straight away anyway and
            it's best to get the records filtered out of the way.
        """
        df = pd.DataFrame(articles)
        df = df[df['manuscript_id'] != 'draft']

        df['raw_manuscript_id'] = df['manuscript_id'].map(lambda x: ManuscriptIdRaw(x).id())
        df['submission_date'] = df['submission_date'].map(lambda x: pd.to_datetime(x, errors='raise', utc=True))
        df['decision_date'] = df['decision_date'].map(lambda x: pd.to_datetime(x, errors='coerce', utc=True))
        df = df.dropna(subset=['manuscript_title', 'authors'])
        df = df.drop_duplicates(subset=['raw_manuscript_id'], keep='last')
        df = df[
            (df['submission_date'] >= self.filter_dates['from']) &
            (df['submission_date'] <= self.filter_dates['to'])
            ]
        df = df[df['final_decision'] != 'Accept']

        return df.to_dict('records')
