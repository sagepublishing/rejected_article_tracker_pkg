import logging
logging.basicConfig(filename='test_deleteme.log', filemode='w', level=logging.DEBUG)

"""
Acquire data for training a Machine-Learning algorithm
"""


        
import pandas as pd
from .ArXivTrainingData import ArXivTrainingData
from .CrossRefTrainingData import CrossRefTrainingData
from .TrainingRow import TrainingRow
from .config import Config as config
from .CleanTrainingData import CleanTrainingData


import os
import sys

import logging
logger = logging.getLogger(__name__)


class TrainingData():
    """
    Given that we have CrossRef and ArXiv API data, combine
    to make a training dataset.
    """

    def knit_training_dataframe(self, arx_training_data, cr_training_data):
        training_data = []
        logger.info('ArXiv training data, shape:{}'.format(arx_training_data.shape))
        logger.info('CrossRef training data, length {}'.format(len(cr_training_data)))
        # now splice the arxiv data AND the CrossRef search results
        # into 1 dataframe
        k=0
        for i,row in arx_training_data.iterrows():
            # doi = row['doi']
            pid = row['id']
            works_records = cr_training_data.get(pid,None)
            if works_records!=None:
                query_article = dict(row)
                for works_record in works_records:
                    # print('DETAILS:',details)
                    # print('Match article:',match_article)
                    training_row = TrainingRow(works_record=works_record,
                                            query_article=query_article
                                            ).to_dict()
                    training_data.append(training_row)
                    k+=1
                    if k>0 and k%1000==0:
                        logger.info(f'{k} rows of data knitted together.')
        return pd.DataFrame(training_data)


    def load_gen_training_df(self):
        if os.path.exists(config.training_dataloc):
            df = pd.read_csv(config.training_dataloc, error_bad_lines=False) #, dtype=str)
            logger.debug('Training data found. Shape:{}'.format(df.shape))
        else:
            logger.debug('Training data not found. Generating from available data.')
            df = self.gen_training_df()
            df.to_csv(config.training_dataloc, index=False, encoding = 'utf-8-sig')
        return df

    def load_gen_clean_training_df(self):
        if os.path.exists(config.clean_training_dataloc):
            df = pd.read_csv(config.clean_training_dataloc, error_bad_lines=False) #, dtype=str)
            logger.debug('Clean training data found. Shape:{}'.format(df.shape))
        else:
            logger.debug('Clean training data not found. Generating from available data.')
            df = self.load_gen_training_df()
            df = CleanTrainingData(df).clean_df
            df.to_csv(config.clean_training_dataloc, index=False, encoding = 'utf-8-sig')
            logger.debug('Clean training data shape:{}'.format(df.shape))
        return df


    def gen_training_df(self):
        logger.info('Acquiring ArXiv data.')
        arx_training_data = ArXivTrainingData().oai_to_df()

        # print('Acquiring CrossRef training data')
        logger.info('Acquiring CrossRef training data')
        cr_training_data = CrossRefTrainingData().build_json_training_data(arx_training_data)
        logger.info('Done.')
        
        return self.knit_training_dataframe(arx_training_data, cr_training_data)