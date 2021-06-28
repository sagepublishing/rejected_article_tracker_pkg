from .SearchProvider import SearchProvider
import json
import os
import time

class CrossRef(SearchProvider):
    def __init__(self, article: dict, http_client, sleep, email='', rows=10):
        self.article = article
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

    def search(self) -> list:
        """
        Searches CrossRef for matching titles.
        """
        address = "https://api.crossref.org/works/"
        payload = {
            'filter': 'from-created-date:{}'.format(self.article['text_sub_date']),
            'query.bibliographic': self.article['manuscript_title'],
            'query.author': self.article['authors'],#.split(', '),
            'rows': self.rows
        }

        headers = {
            'User-Agent': "User {}: SAGE article lookup for article {}".format(self.email, self.article['manuscript_id']),
            'mailto': os.environ.get('MY_EMAIL','')
        }
        response = self.http_client.get(address, 
                                        params=payload, 
                                        headers=headers)
        
        if self.validate_response(response)==True:
            items = response.json()['message']['items']
            return items
        else:
            return None
