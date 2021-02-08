
import xmltodict
import re

class ArXivOAIPMHRecord:
    # def __init__(self, xml_data):
    #     # self.xml_data = xml_data
    #     self.json_data = self.xml_to_json(xml_data)

    def xml_to_json(self, xml_data):
        json_data = xmltodict.parse(xml_data)
        json_data = json_data['arXiv']
        json_data = dict(json_data)
        json_data = self.process_json(json_data)
        if self.check_json(json_data)==True:
            return json_data

    def check_json(self,doc):
        """
        JSON schema should be coming out absolutely consistent.
        This function will break the procedure if a single doc is in wrong format.
        """
        # check object type
        assert type(doc)==dict
        
        # top level fields required
        required_fields = ['id','created','authors', 'title','abstract']        
        for req in required_fields:
            assert req in doc

        # optional fields = ['categories','doi','license',]
        
        # check that authors exist
        authors = doc['authors']
        assert len(authors)>0

        return True

    def convert_authors(self,authors:dict):
        authors = dict(authors)
        auths_str = ''
        if 'author' in authors:
            auths_ls = []
            auths = authors['author']

            # sometimes get a single author instead of a list
            if type(auths)!=list:
                auths = [auths]

            for auth in auths:
                if 'forenames' in auth:
                    auth_str = auth.get('forenames','') + '+' + auth.get('keyname','')
                else:
                    # sometimes we only get a keyname and no forenames
                    auth_str = auth.get('keyname','')
                auths_ls.append(auth_str)
            auths_str = ', '.join(auths_ls)
        return auths_str

    def quick_clean(self,text):
        """
        Simply remove line breaks and extraneous whitespace
        """
        text = text.replace('\n',' ')
        text = re.sub(' +', ' ', text)
        return text

    def process_json(self, json_doc):
        """
        Neatens up JSON document
        """
        dropkeys = ['@xsi:schemaLocation','@xmlns:xsi','@xmlns']
        for k in dropkeys:
            json_doc.pop(k,None)
        title = self.quick_clean(json_doc['title'])
        abstract = self.quick_clean(json_doc['abstract'])
        authors = json_doc['authors']
        json_doc['authors'] = self.convert_authors(authors)
        json_doc['title'] = title
        json_doc['abstract'] = abstract
        json_doc['query_id'] = json_doc['id']
        json_doc['doi'] = str(json_doc.get('doi','')).lower()
        # if there is no updated field, create it with the same value as 'created'
        json_doc['updated'] = json_doc.get('updated',json_doc['created'])
        return json_doc