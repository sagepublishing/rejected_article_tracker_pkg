import os
import xmltodict
import pandas as pd
from tqdm import tqdm

from .ArXivOAIPMH import ArXivOAIPMH
from .CrossRefUtils import CrossRefUtils
from .config import Config as config

import logging
logger = logging.getLogger(__name__)


class ArXivTrainingData:
    """
    Clean data from arXiv for training the RAT
    """
    def oai_data_generator(self):
        """
        Acquire ArXiv OAI-PMH data in JSON format
        """
        oai_data_generator = ArXivOAIPMH().yield_json()
        return oai_data_generator

    def oai_to_df(self):
        """
        convert the oai JSON data to a pandas dataframe
        """
        logger = logging.getLogger(__name__).getChild(self.__class__.__name__)

        # limit the data to articles from the selected  year in config
        yr_string = str(config.start_year_for_training)[-2:]
        oai_data = [x for x in self.oai_data_generator()
                            if x['id'][:2]==yr_string]

        logger.info('OAI-PMH data loaded from {} files'.format(len(oai_data)))
        df = pd.DataFrame(oai_data)
        logger.debug('Initial OAI-PMH dataframe shape: {}'.format(df.shape))
        df = self.clean_df(df)
        return df

    def clean_df(self, df):
        """
        Limit to a specific timeframe
        Remove invalid DOIs
        ensure DOIs are lowercase
        """
        logger = logging.getLogger(__name__).getChild(self.__class__.__name__)

        # limit to 1 year - oai-harvest tends to acquire content outside this range
        # yr_string = str(config.start_year_for_training)[-2:]
        # df = df[df['id'].map(lambda x: str(x)[:2] in {yr_string})]
        logger.debug('Found total of {} articles from {}'.format(df.shape[0],config.start_year_for_training))

        # never work with upper-case characters in DOIs!
        df.loc[:,'doi'] = df['doi'].map(lambda x: str(x).lower())

        # note that some dois are bad dois, let's try and drop those
        df.loc[:,'valid_doi'] = df['doi'].map(lambda x: CrossRefUtils().validate_doi(x))
        df = df[df['valid_doi']==True]
        logger.debug('Found total of {} articles from {} WITH VALID DOIs'.format(df.shape[0], config.start_year_for_training))
        return df