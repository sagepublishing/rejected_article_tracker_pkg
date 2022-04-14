from .SearchProvider import SearchProvider
import json
import os
import time

class CrossRef(SearchProvider):
    def __init__(self, 
                article: dict, 
                
                http_client, 
                sleep, 
                article_types = [], 
                email='', 
                rows=10):
        self.article = article
        self.article_types = article_types
        self.http_client = http_client
        self.sleep = sleep
        self.email = email
        self.rows = rows

    def validate_response(self, response):

        good_response = False
        if response.status_code==200:
            good_response = True
        else:
            good_response = False

        try:
            js_resp = response.json()
            if type(js_resp)==dict and 'message' in response.json() and 'items' in js_resp['message']:
                good_response=True
            else:
                good_response = False
        except:
            good_response = False
        return good_response

    @staticmethod
    def validate_works_record(item):
        if 'DOI' in item:
            return True

    def make_filter(self):
        filter_arts_s = ','.join(['type:'+x for x in self.article_types])
        # optionally include a filter for created-date
        # this doesn't achieve much and slows the search down
        # worst case is we find an article from a long time ago with same
        # titles and author names
        # filter_dates_s = 'from-created-date:'+ self.article.get('text_sub_date','')
        # filter_s = ','.join([filter_arts_s,filter_dates_s])
        filter_s = filter_arts_s
        return filter_s

    def get_first_author_name(self):
        first_author_name = self.article['authors'].split(';')[0]
        return first_author_name

    def get_title_for_search(self):
        title_for_search = self.article.get('title_for_search','')
        if len(title_for_search)<10 or len(title_for_search.split())<=3:
            title_for_search = self.article.get('manuscript_title')
        return title_for_search


    def build_payload(self):
        payload = {
            'query.bibliographic': self.get_title_for_search(),
            'rows': self.rows
        }

        first_author_name = self.get_first_author_name()
        if len(first_author_name)>1:
            payload['query.author'] = first_author_name

        filter_s = self.make_filter()
        
        if len(filter_s)>0:
            payload['filter'] = filter_s
        return payload


    def search(self) -> list:
        """
        Searches CrossRef for matching titles.
        """
        address = "https://api.crossref.org/works/"

        payload = self.build_payload()

        headers = {
            'User-Agent': f"User {self.email}: SAGE RAT search",
            'mailto': os.environ.get('MY_EMAIL','')
        }
        response = self.http_client.get(address, 
                                        params=payload, 
                                        headers=headers)
        if self.validate_response(response)==True:
            items = response.json()['message']['items']
            items = [item for item in items if self.validate_works_record(item)]
            return items
        else:
            return None
