import pandas as pd
from .ArticleItem import ArticleItem
from .ManuscriptIdRaw import ManuscriptIdRaw

from gensim.parsing.preprocessing import remove_stopwords

class FilteredArticles:
    def __init__(self, articles: list):
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
        # optionally remove drafts from scholarone data
        # consider that drafts all have the same id unless you change it in advance
        # df = df[df['manuscript_id'] != 'draft']

        df.loc[:,'raw_manuscript_id'] = df['manuscript_id'].map(lambda x: ManuscriptIdRaw(x).id())
        df.loc[:,'submission_date'] = df['submission_date'].map(lambda x: pd.to_datetime(x, errors='raise', utc=True))
        
        # TODO - get to the bottom of this. Received wisdom is that column updates should
        # be in the style above: df.loc[:,'column_name']. However, this breaks
        # unit tests at the next line. So switched to df['column_name'] here
        df['decision_date'] = df['decision_date'].map(lambda x: pd.to_datetime(x, errors='coerce', utc=True))
        
        df = df.dropna(subset=['manuscript_title', 'authors'])
        # df = df.drop_duplicates(subset=['raw_manuscript_id'], keep='last')

        ## remove accepted articles. You might want to keep these in order to confirm
        ## the accuracy of the RAT
        # df = df[df['final_decision'] != 'Accept']

        df['title_for_search'] = df['manuscript_title'].map(lambda x: self.pre_process_for_search(x))

        return df.to_dict('records')

    def pre_process_for_search(self,title:str) -> str: 
        return remove_stopwords(title)