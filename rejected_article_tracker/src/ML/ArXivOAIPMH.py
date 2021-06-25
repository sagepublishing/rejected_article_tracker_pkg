import os 
import glob
import datetime
from tqdm import tqdm

from oaiharvest.harvest import DirectoryOAIHarvester
from oaiharvest.metadata import DefaultingMetadataRegistry, XMLMetadataReader
from oaipmh.error import NoRecordsMatchError

import logging


from .ArXivOAIPMHRecord import ArXivOAIPMHRecord

from .config import Config as config

class ArXivOAIPMH:
    """
    Class for acquiring and accessing OAI-PMH data
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__).getChild(self.__class__.__name__)
        self.ensure_dirs()
        self.data_location = config.oai_pmh_dataloc
        self.xml_filepaths = self.get_xml_filepaths()
        
            
    def get_xml_filepaths(self):
        """
        This will recognise the filenames of ArXiv XML files and make a list
        of all those that fit our dataset parameters. 
        """
        xml_filepaths = glob.glob(config.oai_pmh_dataloc+'/*')
        yr_string = str(config.start_year_for_training)[-2:]
        file_name_start = os.path.join(config.oai_pmh_dataloc,'oai%3AarXiv.org%3A' + yr_string)
        xml_filepaths = [x for x in xml_filepaths if x>file_name_start]
        return xml_filepaths

    def ensure_dirs(self):
        """
        Ensures that the correct directories exist for the ML data
        """
        data_dirs=[config.main_data_dir,
                    config.ml_data_dir,
                    config.oai_pmh_dataloc]
        for data_dir in data_dirs:
            if not os.path.exists(data_dir):
                os.mkdir(data_dir)       

    def acquire_oai_pmh(self, datadir = config.oai_pmh_dataloc, nRecs = config.n_recs_from_oai_pmh):
        """
        Adapted functions from within OAI-Harvest in order to call
        the API. This is fiddly because the package is intended
        to simply maintain a copy of the full data and not pick subsets
        """
        
        logger = logging.getLogger(__name__).getChild(self.__class__.__name__)
        logger.info('Pulling data from ArXiv OAI-PMH. This may take some time.')
        
        # Set up metadata registry
        xmlReader = XMLMetadataReader()
        metadata_registry = DefaultingMetadataRegistry(defaultReader=xmlReader)
        # create an API harvester object
        harvester = DirectoryOAIHarvester(
            mdRegistry=metadata_registry,
            directory = datadir,
            nRecs = nRecs
        )

        baseUrl = "http://export.arxiv.org/oai2"
        completed = False

        # set the 'from' date where out training data starts
        start_year_str = str(config.start_year_for_training)
        start_date_str = start_year_str + '-01-01'
        from_= datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        until = 'NULL'
        metadataPrefix = 'arXiv'
        try:
            kwargs = {"from_" : from_}
            completed = harvester.harvest(baseUrl, 
                                            metadataPrefix = metadataPrefix, 
                                            **kwargs)
        except NoRecordsMatchError:
            # Nothing to harvest
            completed = True
            logger.info("0 records to harvest")
            logger.debug(
                "The combination of the values of the from={}, "
                "until={}, set=(N/A) and metadataPrefix={} "
                "arguments results in an empty list."
                "".format(from_, until, metadataPrefix)
            )
        except Exception as e:
            # Log error
            logger.error(str(e), exc_info=True)
            # Continue to next provide without updating database lastHarvest
        return completed

    def yield_xml(self):
        """
        Yield OAI-PMH XML data from file. 
        Acquire if directory empty
        """
        if len(self.xml_filepaths)<config.max_training_docs:
            self.logger.warning('Insufficient training data from ArXiv. Pulling data again according to parameters in config.')
            self.acquire_oai_pmh()
        else:
            self.logger.debug('Sufficient OAI-PMH data found. Loading from files.')
        for xml_filepath in tqdm(self.xml_filepaths):
            with open(xml_filepath,'r') as f:
                xml_data = f.read()
                yield xml_data

    def yield_json(self):
        """
        Yield OAI-PMH XML data as JSON. 
        """
        xml_data_generator = self.yield_xml()
        for xml_data in xml_data_generator:
            json_record = ArXivOAIPMHRecord().xml_to_json(xml_data)
            if json_record!=None:
                yield json_record