from .SearchProvider import SearchProvider

import json

class CrossRef(SearchProvider):
    def __init__(self, article: dict, http_client, sleep, email=''):
        self.article = article
        self.http_client = http_client
        self.sleep = sleep
        self.email = email

    def search(self) -> list:
        """
        Searches CrossRef for matching titles.
        """
        address = "https://api.crossref.org/works/"
        payload = {
            'filter': 'from-created-date:{}'.format(self.article['text_sub_date']),
            'query.bibliographic': self.article['manuscript_title'],
            'query.author': self.article['authors'].split(', '),
            'rows': 10
        }
        headers = {
            'User-Agent': "Adam Day's rejected article tracker",
            'mailto': self.email
        }

        response = self.http_client.get(address, params=payload, headers=headers)

        return response.json()['message']['items']
