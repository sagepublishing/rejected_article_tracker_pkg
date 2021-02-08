
import os
import json
import requests
import time
import datetime 
from tqdm import tqdm

from ..CrossRef import CrossRef
from ..SearchResult import SearchResult

from .CrossRefUtils import CrossRefUtils
from .CrossRefSearch import CrossRefSearch
from .CrossRefDOIData import CrossRefDOIData 
from .ArXivTrainingData import ArXivTrainingData
from .ArXivArticleItem import ArXivArticleItem

from .config import Config as config

import logging
logger = logging.getLogger(__name__)

# TODO build a separate crossref record class

class CrossRefTrainingData:
    """
    Given arXiv DOIs
    - get all the CrossRef records
    Given arXiv titles and authors
    - get all the CrossRef search results
    """

    def acquire_crossref(self, dois=[]):
        """
        Download CrossRef Works API data for your OAI-PMH dataset
        - this is where we get the results directly from the DOI. 
        """
        # get data from DOIs        
        cr_data = CrossRefDOIData().works_from_dois_to_file(dois)
        return cr_data   

    def search_matches(self, items):
        """
        Given arXiv OAI-PMH records as input
        - get all of the crossref search results
        """
        logger = logging.getLogger(__name__).getChild(self.__class__.__name__)
        self.email = config.myemail
        
        if os.path.exists(config.crossref_search_jsonl_dataloc):
            results_gen = self.generate_jsonl_data(
                                config.crossref_search_jsonl_dataloc
                                ) 
        else:
            results_gen=[]
        
        results = dict()
        # each row in our jsonl is {id: search_results}
        for i,id_to_search_doc in tqdm(enumerate(results_gen)):
            # get the id from id_to_search_results
            art_id = list(id_to_search_doc)[0]
            # get the correcponding search results
            search_results = list(id_to_search_doc.values())[0]
            # add to a big dict
            results[art_id] = search_results
            
        
        # list of ArXiv OAI-PMH data
        items = [item for item in items if item['id'] not in results]
        logger.info('Found {} results. Searching for remaining {} items.'.format(len(results), len(items)))
        CrossRefSearch(items=items).search_and_write()
        return results

    def generate_jsonl_data(self, data_path):
        """
        Load from a jsonl file
        """
        with open(data_path, 'r') as f:
            for line in f:
                yield json.loads(line)
            

    def load_json_data(self, data_path):
        """
        Allows periodic save/load of data in case we need to restart
        CrossRef searches
        """
        with open(data_path, 'r') as f:
            json_data = json.load(f)
        return json_data

    def write_out_json_data(self, json_data, data_path):
        """
        Allows periodic save/load of data in case we need to restart
        CrossRef searches
        """
        with open(data_path, 'w') as f:
            json.dump(json_data,f)

    def training_data_to_file(self, dois = [], items= []):
        """
        Acquires training data and saves to file.
        """
        doi_results = self.acquire_crossref(dois)
        search_results = self.search_matches(items)
        return doi_results, search_results
    
    def load_data(self, df):
        logger = logging.getLogger(__name__).getChild(self.__class__.__name__)

        doi_results = dict()
        search_results = dict()
        dois = df.doi.values
        doi_results = self.acquire_crossref(dois = dois)
        logger.info('Loaded {} DOI results from file'.format(len(doi_results)))

        # if os.path.exists(search_results_path):
        items = self.create_items(df)
        search_results = self.search_matches(items)
            
        return doi_results, search_results
            

    def build_json_training_data(self, df):
        doi_results, search_results = self.load_data(df)
        logger.debug('DOI results: {} Search results: {}'.format(len(doi_results), len(search_results)))
        # training data
        # form = {doi : [{correct},{incorrect}]}
        training_data = dict()
        for i, row in df.iterrows():
            doi = row['doi']
            pid = row['id']
            if pid in search_results and doi in doi_results:
                correct_result = doi_results[doi]
                correct_result['rank'] = 3 # should maybe be np.nan
                correct_result['correct_yn'] = 1
                correct_result['row_doi'] = doi
                doi_search_results = search_results[pid]
                correct_doi_found = False
                best_incorrect_result_found = False
                for i,result in enumerate(doi_search_results):
                    result_doi = result['DOI']
                    if result_doi==doi and correct_doi_found==False:
                        correct_result['rank']=i
                        correct_result['score']=result['score']
                        correct_doi_found = True
                    elif result_doi!=doi and best_incorrect_result_found == False:
                        best_incorrect_result_found = True
                        result['rank'] = i
                        result['row_doi'] = result_doi
                        result['correct_yn'] = 0
                        incorrect_result = result
                    elif correct_doi_found==True and best_incorrect_result_found==True:
                        break
                    else:
                        pass
                training_data[pid] = [correct_result, incorrect_result]


        logger.info('CrossRef Training dataset built. Length: {}'.format(len(training_data)))
        return training_data
                
    def create_items(self, df):
        """ gives a list of dicts for the rows of the df"""
        return list(df.T.to_dict().values()) 