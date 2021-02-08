
from .CrossRefWorksRecord import CrossRefWorksRecord
from fuzzywuzzy import fuzz

class TrainingRow:
    def __init__(self, works_record:dict, query_article: dict):
        """
        :param works_record: Article works_record from search provider (e.g. CrossRef)
        :param query_article: The input article (e.g. from the user)
        :param clf: The classifier to score how similar the articles are.
        :param rank:
        """
        self.works_record = CrossRefWorksRecord(works_record, limit_cols=True).works_record #to_dict()
        self.query_article = query_article
        

    def to_dict(self) -> dict:
        training_row = self.works_record
        cr_title = self.works_record.get('full_title','')
        training_row['authors_list'] = self.authors_list(self.works_record.get('author', list()))
        training_row.update(self.match_names(query_authors=self.query_article['authors'], 
                                        authors=self.works_record['authors_list']))
        training_row['similarity'] = fuzz.ratio(self.query_article['title'],cr_title) 
        training_row['query_id'] = 'id:'+self.query_article['id']
        training_row['query_title'] = self.query_article['title']
        training_row['query_authors'] = self.query_article['authors']
        training_row['query_created'] = self.query_article['created']
        training_row['query_doi'] = self.query_article.get('doi','') # this should always be found
        # training_row['correct_yn'] = self.works_record['correct_yn']
        training_row['match_title'] = cr_title
        return training_row

    @staticmethod
    def authors_list(authors: list) -> list:
        query_authors = list()
        for author in authors:
            given = author.get('given', '')
            family = author.get('family', '')
            query_authors.append(given + '+' + family)
        return query_authors

    @staticmethod
    def match_names(query_authors, authors):
        names1 = [(name[0], name[name.rfind('+') + 1:]) for name in query_authors.split(', ')]
        names2 = [(name[0], name[name.rfind('+') + 1:]) for name in authors]
        return {
            'author_match_one': int(any(name in names2 for name in names1)),
            'author_match_all': int(all(name in names2 for name in names1)),
        }

