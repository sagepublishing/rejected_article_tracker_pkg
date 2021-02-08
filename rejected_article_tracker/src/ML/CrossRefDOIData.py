import json
import os
from tqdm import tqdm


from .config import Config as config

from .CrossRefUtils import CrossRefUtils

import logging
logger = logging.getLogger(__name__)

class CrossRefDOIData:
    """
    Relevant data from crossref
    """

    def works_from_dois_to_file(self,dois):
        # get local data first
        cr_data = self.crossref_from_local()
        logger.debug('Loaded {} DOI records from file.'.format(len(cr_data)))
        # then add API data
        remaining_dois = [doi for doi in dois if doi not in cr_data]
        cr_data_generator = CrossRefUtils().get_many_crossref(remaining_dois ) # ,retry_failures=True)
        for works_record in cr_data_generator:
            if works_record != None:
                # dois_found.add(works_record['DOI'])
                cr_data[works_record['DOI']] = works_record
                with open(config.crossref_doi_dataloc, 'a') as f:
                    f.write(json.dumps(works_record) + "\n")
            else:
                pass
                # logger.debug('Skipping works record. {}'.format(works_record))
        logger.info('Written CrossRef DOI results to file! Total: {}'.format(len(cr_data)))
        return cr_data

    def crossref_from_local(self):
        """
        Take CrossRef data acquired by crossref_from_dois and
        put it into one big JSON object. 
        """
        data_location = config.crossref_doi_dataloc
        cr_data = dict()
        if os.path.exists(data_location):
            with open(data_location, 'r') as f:
                for works_record in f:
                    works_record = json.loads(works_record)
                    cr_data[works_record['DOI']] = works_record
        return cr_data

