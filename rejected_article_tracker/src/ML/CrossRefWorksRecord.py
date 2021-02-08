
from .CrossRefUtils import CrossRefUtils
from .CrossRefEarliestDate import CrossRefEarliestDate

import logging
logger = logging.getLogger(__name__)

class CrossRefWorksRecord:
    def __init__(self, works_record:dict, limit_cols=False):
        """
        Input is a JSON API response object
        """
        self.works_record = self.pre_process(works_record)
        if limit_cols == True:
            self.works_record = self.limit_columns(self.works_record)
        # logger.debug('Preprocessed Works Rec: {}'.format(self.works_record))

    def pre_process(self, works_record:dict):
        # logger = logging.getLogger(__name__).getChild(self.__class__.__name__)
        earliest_date = CrossRefEarliestDate(works_record).earliest_date
        works_record['earliest_date'] = earliest_date
        works_record = self.ensure_doi_lower(works_record)
        works_record['full_title'] = works_record.get('full_title',self.extract_full_title(works_record))
        works_record['normalised_container_title'] = self.normalise_container_title(works_record)
        return works_record
        

    def str_entity_from_ls(self, works_record:dict, entity_name:str):
        """
        Some CR fields seem to be lists of strings, strings, or empty lists
        Universal fn to extract whatever text there is from such fields.
        """
        ent = works_record.get(entity_name,None)
        if type(ent)==list and len(ent)>0:
            ent = '. '.join(ent)
        if type(ent)==str:
            return ent
        else:
            return ''

    def limit_columns(self,works_record):
        """
        (Optional?) step to remove useless columns from our data. 
        """
        allowed_cols = [
                'DOI',
                'publisher', 
                'normalised_container_title', 
                'container-title',
                'earliest_date',
                'full_title',
                'author',
                'author_ls',
                'is-referenced-by-count', 
                'score', 
                'rank',
                'correct_yn',
        ]
        cols_in_works_rec = list(works_record)
        for col in cols_in_works_rec:
            if col not in allowed_cols:
                works_record.pop(col)
        return works_record


    def extract_full_title(self, works_record:dict):
        subtitle = self.str_entity_from_ls(works_record, 'subtitle')
        title = self.str_entity_from_ls(works_record, 'title')
        title = title.rstrip('.')
        if subtitle!='':
            full_title = '. '.join([title, subtitle]).strip()
        else:
            full_title = title
        return full_title
        
        

    def normalise_container_title(self, works_record:dict):
        container_name = self.str_entity_from_ls(works_record, 'container-title')
        return container_name.lower()


    def ensure_doi_lower(self,works_record:dict):
        doi = works_record.get('DOI','').lower()
        works_record['DOI'] = doi
        return works_record

    def to_dict(self) -> dict:
        return self.works_record