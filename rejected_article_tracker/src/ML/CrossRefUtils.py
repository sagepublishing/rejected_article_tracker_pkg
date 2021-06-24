import urllib
import requests
import time
import re
from dateutil import parser
import datetime
from dateutil.tz import tzutc

from tqdm import tqdm

from .config import Config as config

from multiprocessing import Pool

import logging
logger = logging.getLogger(__name__)

class CrossRefUtils:

    def __init__(self):
        # setting a high batch size causes slow responses. 
        # max = 100
        self.batch_size = 10
        self.email = config.myemail or ''
        self.headers = {
                        'User-Agent': 'Rejected article tracking',
                        'mailto': self.email
                        }

    def chunks(self, l:int, n:list):
        '''
        converts a list into a list of lists each with max length == n
        '''
        # For item i in a range that is a length of l,
        for i in tqdm(list(range(0, len(l), n))):
            # Create an index range for l of n items:
            yield l[i:i+n]

    def validate_response(self,response):
        """
        Check that CrossRef response is valid JSON obj
        """
        try:
            data = response.json()
        except:
            return False

        # CrossRef returns status==False
        if data.get('status',None) == 'failed':
            return False

        # if response is for a list of DOIs there is an 'items' field
        elif 'message' in data and 'items' in data['message']:
            items = data['message']['items']
            if type(items) ==list and len(items)>0:
                return True
            else:
                return False

        # if response is for a single article there is no 'items'
        elif 'message' in data and 'DOI' in data['message']:
            return True
        else:
            return False

    def check_response_time(self, response):
        """
        Checks API response time and sleeps if it's longer than normal
        CrossRef API should be able to handle 50 requests per second,
        But adding some delay between requests seems to improve overall speed
        sometimes. 
        """
        # check response time.
        # Documentation recommends backing off if response time is too long.
        response_time = response.elapsed.total_seconds()
        # logger.debug('{} seconds for last request'.format(response_time))

        # responses are generally <1s.
        # simple rule for sleeping if responses are slow
        if response_time > 1.0:
            # logger.debug('CrossRef slow to respond. Sleep for a few seconds.')
            time.sleep(response_time//2)            

    def validate_doi(self, doi:str):
        """
        based on regexs given here: https://www.crossref.org/blog/dois-and-matching-regular-expressions/
        Note that those regexs include chars for start of line and end of line which I have removed
        - Returns True for a valid DOI
        - Returns False for an invalid DOI
        """
        if type(doi)!=str:
            return False
        else:
            # discard DOIs from other registrars
            inv_pats = [r'(?i)10\.13140/RG\.',
                        r'(?i)10\.5281/zenodo\.',
                        r'(?i)10\.6084/m9\.figshare\.c\.',
                        r'(?i)10\.17605/osf\.io']
            for pat in inv_pats:
                match = bool(re.match(pat,doi))
                if match==True:
                    return False
            
            pats = [r'(?i)10.\d{4,9}/[-._;()/:A-Z0-9]+',
                    r'(?i)10.1002/[^\s]+$/i',
                    r'(?i)10.\d{4}/\d+-\d+X?(\d+)\d+<[\d\w]+:[\d\w]*>\d+.\d+.\w+;\d',
                    r'(?i)10.1021/\w\w\d+',
                    r'(?i)10.1207/[\w\d]+\&\d+_\d+']
            for pat in pats:
                match = bool(re.match(pat,doi))
                if match==False:
                    pass
                else:
                    return True
            return False

    def get_one_crossref(self, doi):
        """
        Simply pull one CrossRef works record from a DOI.
        Returns record in a length==1 list
        or returns None
        """

        if self.validate_doi(doi)==True:
            # crossref docs recommend URL-encoding DOIs
            # this doesn't always work, though. 
            url = r'https://api.crossref.org/works/{}'.format(urllib.parse.quote(doi))
            r = requests.get(url, headers = self.headers)
            self.check_response_time(r)
            if self.validate_response(r) ==True:
                try:
                    if r.json()['status']!='failed':
                        return [r.json()['message']] # output should be a list for consistency
                    else:
                        logger.debug('failure for doi: {doi}')
                except:
                    # retry failures - doesn't add much consider commenting. 
                    logger.debug('Error in response.  Not interpretable as json? Searched for: {} Trying unescaped doi'.format(doi))
                    url = r'https://api.crossref.org/works/{}'.format(doi)
                    r = requests.get(url, headers = self.headers)
                    self.check_response_time(r)
                    if self.validate_response(r)==True:
                        return [r.json()['message']] # output should be a list for consistency
                    else:
                        logger.debug('Failure for doi: {} (skipping)'.format(doi))
        return None
                

    def get_doi_batch(self, doi_batch):
        
        dois_s = 'doi:' + ',doi:'.join(doi_batch)
        # Crossref documentation recommends %-encoding dois
        dois_s = urllib.parse.quote(dois_s)
        # build query url
        url = r'https://api.crossref.org/works/?filter={}&rows={}'.format(dois_s, self.batch_size)
        # make request
        r = requests.get(url, headers = self.headers)
        self.check_response_time(r)
        records = list()
        if self.validate_response(r)==True:
            data = r.json()
            records = data['message']['items']

        return records


    def get_many_crossref(self, dois, retry_failures=False):
        '''
        Pulls a list of CR DOIs all at once.
        Yields output json for each batch for analysis/caching.
        -- Note that batch_size==100 seems to be a limit --
        '''
        pool_size = 10
        valid_dois = [doi for doi in dois if self.validate_doi(doi)==True]
        dois_found = set()
        
        # create lists of len 100
        doi_batches = list(self.chunks(valid_dois,self.batch_size))

        logger.debug('Pulling data from DOIs in {} batches of size {} split into pools of size {}'.format(
                                                    len(doi_batches),
                                                    self.batch_size,
                                                    pool_size))

        # create lists of len 50 OF lists of len 100
        # chunked_doi_batches = list(self.chunks(doi_batches,pool_size))
        chunked_doi_batches = self.chunks(doi_batches,pool_size)
        
        for doi_batch_pool in chunked_doi_batches:
            cr_data_generator = self.multi(CrossRefUtils().get_doi_batch, 
                                            doi_batch_pool,
                                            pool_size)
            for works_record_batch in cr_data_generator:
                for works_record in works_record_batch:
                    dois_found.add(works_record['DOI'])
                    yield works_record

        # retry failures
        if retry_failures == True:
            logger.info('Retrying DOI-search failures.')
            pool_size = 50
            remaining_dois = [x for x in valid_dois if x not in dois_found]
            remaining_doi_pools = list(self.chunks(remaining_dois,pool_size))
            # recall that batches here are length==1
            for doi_pool in tqdm(remaining_doi_pools):
                cr_data_generator = self.multi(self.get_one_crossref, 
                                            doi_pool,
                                            pool_size)
                for works_record_batch in cr_data_generator:
                    if works_record_batch != None and type(works_record_batch)==list:
                        for works_record in works_record_batch:
                            dois_found.add(works_record['DOI'])
                            yield works_record
                else:
                    pass

    def multi(self,f,iterable, pool_size):
        """
        General function for multithreading
        :iterable: must be an object like a list. Not a generator. 
        :f: a function which operates on items in the list
        """
        # with get_context("spawn").Pool(2) as p:
        with Pool(pool_size) as p:
            return p.map(f, iterable)