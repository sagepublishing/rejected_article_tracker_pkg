
# this might be nicer as a dataclass

allowed_types = {'book', 'book-chapter', 'book-part', 'book-section', 
            'book-series', 'book-set', 'book-track', 'component',
            'dataset', 'dissertation', 'edited-book', 'grant',
             'journal', 'journal-article', 'journal-issue', 'journal-volume',
              'monograph', 'other', 'peer-review', 'posted-content',
               'proceedings', 'proceedings-article', 'proceedings-series',
                'reference-book', 'reference-entry', 'report', 'report-series',
                 'standard', 'standard-series'}

class ConfigChecker:

    def __init__(self, config:dict):

        self.config = self.check(config)
    
    def check(self,config):
        config = self.check_type(config)
        config = self.check_values(config)
        return config

    def check_type(self, config:dict):
        default = {
                "threshold": 0.5, 
                "max_results_per_article":10, 
                "article_types":[], 
        }

        if not isinstance(config,dict):
            config = default

        thresh = config.get('threshold')
        if not isinstance(thresh,float):
            config['threshold']=0.5

        max_results = config.get('max_results_per_article')
        if not isinstance(max_results,int):
            config['max_results_per_article']=10
        
        article_types = config.get('article_types')
        if not isinstance(article_types,list):
            config['article_types']=[]
        
        return config

    def check_values(self,config:dict):
        if config['threshold']<0.0 or config['threshold']>1.0:
            config['threshold'] = 0.5

        if config['max_results_per_article']<1 or config['max_results_per_article']>10:
            config['max_results_per_article'] = 10

        article_types = []
        for article_type in config['article_types']:
            if isinstance(article_type,str) and article_type in allowed_types:
                article_types.append(article_type)
            
        config['article_types'] = article_types
        return config