"""
Custom training data cleaner.
"""
import Levenshtein
import langdetect
from fuzzywuzzy import fuzz

from gensim.parsing.preprocessing import preprocess_string, strip_tags, strip_multiple_whitespaces
from gensim.utils import deaccent

import logging

logger = logging.getLogger(__name__)

class CleanTrainingData:

    def __init__(self, df):
        self.clean_df = self.clean_it(df)

    def clean_it(self,df):
        logger = logging.getLogger(__name__).getChild(self.__class__.__name__)
        logger.debug('Cleaning Dataframe input SHAPE {}'.format(df.shape))

        cleaning_fns = [
            self.set_min_length,
            self.drop_article_types,
            self.drop_test_accounts,
            self.remove_zero_auth_matches,
            self.pre_process_titles,
            self.english_only, ## very slow!
            self.remove_typo_candidates,
            self.add_auth_col,
            self.recalculate_levenshtein,
            self.add_n_auths
            ]
        for i,fn in enumerate(cleaning_fns):
            df = fn(df)
            logger.debug('Cleaning iteration # {} - DATAFRAME SHAPE {}'.format(i+1, df.shape))
        return df

    # TODO - should this be filtering on query_title rather than
    # full_title?
    def drop_article_types(self, df):
        """
        Note that we have 2 rows for every arXiv id. So we need to remove
        ALL rows where the article appears to be a non-research article. 
        """
        def identify_art_types_in_titles(title:str):
            out = True
            drop_words = ['preface','foreword','proceeding','editorial',
                        'conference', 'addendum','erratum', 'corrigendum', 'correction']
            if any(title.lower().startswith(y) for y in drop_words):
                out = False
            return out
        drop_col = df['query_title'].map(lambda x: identify_art_types_in_titles(x))
        drop_pids = set(df[~drop_col]['query_id'].values)
        df = df[~df['query_id'].isin(drop_pids)]
        return df

    def set_min_length(self, df):
        # logger.debug('match_title values: {}'.format( df['match_title'].head(3).values))
        # logger.debug('query_title values: {}'.format( df['query_title'].head(3).values))
        min_length = 7
        # get set of ids where title length is < min
        subset_ids =  df[df['query_title'].map(lambda x: len(str(x).split()) <= min_length)].query_id.values
        # limit data to those records where ids are NOT shared with that set
        df = df[~df['query_id'].isin(set(subset_ids))]

        # get set of ids where title length is < min
        # subset_ids =  df[df['match_title'].map(lambda x: len(str(x).split()) <= min_length)].query_id.values
        # # limit data to those records where ids are NOT shared with that set
        # df = df[~df['query_id'].isin(set(subset_ids))]
        return df
    

    def drop_test_accounts(self, df):
        
        subset_ids =  df[df['publisher']=='Test Accounts'].query_id.values
        df = df[~df['query_id'].isin(set(subset_ids))]
        return df

    def remove_zero_auth_matches(self, df):
        """
        If we don't even have 1 author match - drop the row. 
        """
        subset_ids =  df[(df['author_match_one']==0) & (df['correct_yn']==1)].query_id.values
        df = df[~df['query_id'].isin(set(subset_ids))]
        return df

    def english_only(self, df):
        
        df['query_lang'] = df['query_title'].map(lambda x:langdetect.detect(x))
        # df['match_lang'] = df['match_title'].map(lambda x:langdetect.detect(x))
        # df = df[(df['match_lang']=='en') & (df['query_lang']=='en')]
        df = df[df['query_lang']=='en']
        return df

    def remove_typo_candidates(self, df):
        """
        Attempts to identify and remove rows where DOI contains a typo
        """
        # NOTE - VS Code is showing an error on Levenshtein here, but it works
        df['doi_sim'] = [Levenshtein.distance(row['query_doi'],row['DOI']) for i,row in df.iterrows()]
        typo_candidates = df[(df['correct_yn']==0) & (df['doi_sim']<3)] 

        # hard to draw lines here. Erring on the side of caution
        # lets take only cases where it seems like a VERY high chance of being a typo
        # REMINDER: we are looking for rows labelled INCORRECT that are actually correct due to typos in DOIs
        typos = typo_candidates[(typo_candidates['author_match_all']==1) & (typo_candidates['similarity']>=85)
                            | (typo_candidates['author_match_one']==1) & (typo_candidates['similarity']>=95)]
        typo_ids = set(typos['query_id'].values)
        df = df[~df['query_id'].isin(typo_ids)]

        return df

    def add_auth_col(self, df):

        def pre_author_s(author_s):
            author_s = author_s.replace('.','').replace('-','').replace('+',' ')
            author_s = author_s.lower()
            author_s = deaccent(author_s)
            return author_s

        def convert_author(author_json):
            """
            Converts CrossRef authors entry from a works record into
            the same string format as we already have on ArXiv data.
            """
            # should always be a list.
            # occasionally pandas reads as str, but that shouldn't happen
            if type(author_json)!=list:
                author_json = eval(author_json) # in case you get a string
            auth_ls = list()
            for auth in author_json:
                auth_name = auth.get('given','') + ' '
                auth_name += auth.get('family','')
                auth_ls.append(auth_name)
            author_s = ', '.join(auth_ls)
            return author_s

        df['cr_author'] = df['author'].map(lambda x: pre_author_s(convert_author(x)) )
        df['query_authors'] = df['query_authors'].map(lambda x: pre_author_s(x))
        return df

    def pre_process_titles(self,df):

        # unused
        # CUSTOM_FILTERS = [strip_tags, deaccent, lambda x: x.lower(), ]

        def pre_process(s):
            s = str(s)
            s = strip_tags(s)
            s = deaccent(s)
            s = strip_multiple_whitespaces(s)
            s = s.lower()
            return s

        df['query_title'] = df['query_title'].map(lambda x: pre_process(x))
        df['match_title'] = df['match_title'].map(lambda x: pre_process(x))
        return df

    def recalculate_levenshtein(self, df):
        
        df['similarity'] = [fuzz.ratio(row['query_title'],row['match_title']) for i,row in df.iterrows()]
        return df

    def add_n_auths(self, df):
        def n_auths_from_col(s):
            s= str(s)
            return len(s.split(','))
        df['n_auths_query'] = df['query_authors'].map(lambda x: n_auths_from_col(x))
        df['n_auths_match'] = df['cr_author'].map(lambda x: n_auths_from_col(x))
        return df
    