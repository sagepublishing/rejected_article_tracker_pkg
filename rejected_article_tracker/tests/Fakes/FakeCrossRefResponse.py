class FakeGoodListCrossRefResponse:

    def __init__(self):
        self.success_response_obj1 = {'status': 'succeeded',
        'message':{'items':[{"indexed": {"date-parts": [[2020, 4, 15]], "date-time": "2020-04-15T03:22:44Z", "timestamp": 1586920964026}, 
        "publisher-location": "New York, New York, USA", 
        "reference-count": 18, 
        "publisher": "ACM Press", 
        "isbn-type": [{"value": "9781450366748", "type": "print"}], 
        "license": [{"URL": "http://www.acm.org/publications/policies/copyright_policy#Background", 
        "start": {"date-parts": [[2019, 5, 13]], "date-time": "2019-05-13T00:00:00Z", "timestamp": 1557705600000}, 
        "delay-in-days": 132, "content-version": "vor"}], 
        "content-domain": {"domain": [], "crossmark-restriction": False}, 
        "published-print": {"date-parts": [[2019]]}, 
        "DOI": "10.1145/3308558.3313535", 
        "type": "proceedings-article", 
        "created": {"date-parts": [[2019, 5, 13]], "date-time": "2019-05-13T12:17:59Z", "timestamp": 1557749879000}, 
        "source": "Crossref", "is-referenced-by-count": 0, 
        "title": ["Estimating the Total Volume of Queries to Google"], 
        "prefix": "10.1145", 
        "author": [{"given": "Fabrizio", "family": "Lillo", "sequence": "first", "affiliation": [{"name": "University of Bologna, Italy"}]}, {"given": "Salvatore", "family": "Ruggieri", "sequence": "additional", "affiliation": [{"name": "University of Pisa, Italy"}]}], 
        "member": "320", 
        "reference": [{"key": "key-10.1145/3308558.3313535-1", "unstructured": "L.A. Adamic and B.A. Huberman. 2002. Zipf's law and the Internet. Glottometrics3(2002), 143-150."}, {"key": "key-10.1145/3308558.3313535-2", "unstructured": "R. A. Baeza-Yates, A. Gionis, F. Junqueira, V. Murdock, V. Plachouras, and F. Silvestri. 2007. The impact of caching on search engines. In SIGIR. ACM, 183-190."}, {"key": "key-10.1145/3308558.3313535-3", "unstructured": "R. A. Baeza-Yates and A. Tiberi. 2007. Extracting semantic relations from query logs. In KDD. ACM, 76-85."}, {"key": "key-10.1145/3308558.3313535-4", "unstructured": "A. Bookstein. 1990. Informetric distributions, part I: Unified overview. JASIS41, 5 (1990), 368-375."}, {"key": "key-10.1145/3308558.3313535-5", "unstructured": "A. Clauset, C. R. Shalizi, and M. E. J. Newman. 2009. Power-Law Distributions in Empirical Data. SIAM Rev.51, 4 (2009), 661-703.", "DOI": "10.1137/070710111", "doi-asserted-by": "crossref"}, {"key": "key-10.1145/3308558.3313535-6", "unstructured": "G. Cormode, M. N. Garofalakis, P. J. Haas, and C. Jermaine. 2012. Synopses for Massive Data: Samples, Histograms, Wavelets, Sketches. Foundations and Trends in Databases4, 1-3 (2012), 1-294."}, {"key": "key-10.1145/3308558.3313535-7", "unstructured": "G. Cormode, T. Kulkarni, and D. Srivastava. 2018. Constrained Private Mechanisms for Count Data. In ICDE. IEEE, 845-856."}, {"key": "key-10.1145/3308558.3313535-8", "unstructured": "G. Cormode and S. Muthukrishnan. 2005. An improved data stream summary: the count-min sketch and its applications. J. Algorithms55, 1 (2005), 58-75."}, {"key": "key-10.1145/3308558.3313535-9", "unstructured": "M. Cristelli, M. Batty, and L. Pietronero. 2012. There is More than a Power Law in Zipf. Scientific Reports2(2012), 812."}, {"key": "key-10.1145/3308558.3313535-10", "unstructured": "S. Ding, J. Attenberg, R. A. Baeza-Yates, and T. Suel. 2011. Batch query processing for web search engines. In WSDM. ACM, 137-146."}, {"key": "key-10.1145/3308558.3313535-11", "unstructured": "C. Gillespie. 2015. Fitting Heavy Tailed Distributions: The poweRlaw Package. J. of Stat. Software64, 2 (2015), 1-16."}, {"key": "key-10.1145/3308558.3313535-12", "unstructured": "M.L. Goldstein, S.A. Morris, and G.G. Yena. 2004. Problems with fitting to the power-law distribution. European Physical Journal B41 (2004), 255-258."}, {"key": "key-10.1145/3308558.3313535-13", "unstructured": "L. Melis, G. Danezis, and E. De Cristofaro. 2016. Efficient Private Statistics with Succinct Sketches. In NDSS. The Internet Society.", "DOI": "10.14722/ndss.2016.23175", "doi-asserted-by": "crossref"}, {"key": "key-10.1145/3308558.3313535-14", "unstructured": "M.E.J. Newman. 2005. Power laws, Pareto distributions and Zipf's law. Contemporary Physics46, 5 (2005), 323-351."}, {"key": "key-10.1145/3308558.3313535-15", "unstructured": "A. Orlitskya, A.T. Sureshb, and Y. Wuc. 2016. Optimal prediction of the number of unseen species. Proceedings of the National Academy of Sciences USA113 (2016), 13283-13288."}, {"key": "key-10.1145/3308558.3313535-16", "unstructured": "C. Petersen, J. Grue Simonsen, and C. Lioma. 2016. Power Law Distributions in Information Retrieval. ACM Trans. Inf. Syst.34, 2 (2016), 8:1-8:37."}, {"key": "key-10.1145/3308558.3313535-17", "unstructured": "L. Vaughan and Y. Chen. 2015. Data mining from web search queries: A comparison of Google Trends and Baidu Index. JASIST66, 1 (2015), 13-22."}, {"key": "key-10.1145/3308558.3313535-18", "unstructured": "Y. Virkar and A. Clauset. 2014. Power-Law Distributions in Binned Empirical Data. The Annals of Applied Statistics8, 1 (2014), 89-119."}], "event": {"name": "The World Wide Web Conference", "location": "San Francisco, CA, USA", "sponsor": ["IW3C2, International World Wide Web Conference Committee"], "acronym": "WWW '19", "start": {"date-parts": [[2019, 5, 13]]}, "end": {"date-parts": [[2019, 5, 17]]}}, "container-title": ["The World Wide Web Conference on   - WWW '19"], "link": [{"URL": "http://dl.acm.org/ft_gateway.cfm?id=3313535&ftid=2057046&dwn=1", "content-type": "unspecified", "content-version": "vor", "intended-application": "similarity-checking"}], "deposited": {"date-parts": [[2019, 7, 1]], "date-time": "2019-07-01T19:41:34Z", "timestamp": 1562010094000}, "score": 19.355684, "issued": {"date-parts": [[2019]]}, "ISBN": ["9781450366748"], "references-count": 18, "URL": "http://dx.doi.org/10.1145/3308558.3313535", "relation": {"cites": []}}, {"indexed": {"date-parts": [[2020, 4, 10]], "date-time": "2020-04-10T21:58:57Z", "timestamp": 1586555937525}, "publisher-location": "Cham", "reference-count": 0, "publisher": "Springer International Publishing", "isbn-type": [{"value": "9783319165738", "type": "print"}, {"value": "9783319165745", "type": "electronic"}], "content-domain": {"domain": [], "crossmark-restriction": False}, "published-print": {"date-parts": [[2015]]}, "DOI": "10.1007/978-3-319-16574-5_2", "type": "book-chapter", "created": {"date-parts": [[2015, 4, 1]], "date-time": "2015-04-01T17:37:04Z", "timestamp": 1427909824000}, "page": "47-95", "source": "Crossref", "is-referenced-by-count": 0, "title": ["Properties of Plane Electromagnetic Waves"], "prefix": "10.1007", "author": [{"given": "Fabrizio", "family": "Frezza", "sequence": "first", "affiliation": []}], "member": "297", "published-online": {"date-parts": [[2015, 4, 2]]}, "container-title": ["A Primer on Electromagnetic Fields"], "link": [{"URL": "http://link.springer.com/content/pdf/10.1007/978-3-319-16574-5_2", "content-type": "unspecified", "content-version": "vor", "intended-application": "similarity-checking"}], 
        "deposited": {"date-parts": [[2015, 4, 1]], "date-time": "2015-04-01T17:37:06Z", "timestamp": 1427909826000}, 
        "score": 18.084425, 
        "issued": {"date-parts": [[2015]]}, 
        "ISBN": ["9783319165738", "9783319165745"], 
        "references-count": 0, 
        "URL": "http://dx.doi.org/10.1007/978-3-319-16574-5_2"}]
                    }}

    def json(self):
        if type(self.success_response_obj1)==dict:
            return self.success_response_obj1
        else:
            raise TypeError

class FakeGoodSingleCrossRefResponse:

    def __init__(self):
        
        self.success_response_obj2 = {'status': 'succeeded',
                                    'message':{'DOI':'fake_doi',
                                                'earliest_date': {},
                                                "created": {"date-parts": [[2019, 5, 13]], "date-time": "2019-05-13T12:17:59Z", "timestamp": 1557749879000}, 
                                                "deposited": {"date-parts": [[2015, 4, 1]], "date-time": "2015-04-01T17:37:06Z", "timestamp": 1427909826000}, 
                                                }}

    def json(self):
        if type(self.success_response_obj2)==dict:
            return self.success_response_obj2
        else:
            raise TypeError

class FakeBadCrossRefResponse1:

    def __init__(self):
        
        self.fail_response_obj1 = {'status':'failed'}

    def json(self):
        if type(self.fail_response_obj1)==dict:
            return self.fail_response_obj1
        else:
            raise TypeError

class FakeBadCrossRefResponse2:

    def __init__(self):
        
        self.fail_response_obj2 = 'string not json!!'

    def json(self):
        if type(self.fail_response_obj2)==dict:
            return self.fail_response_obj2
        else:
            raise TypeError