import numpy as np


class BestCandidate():
    def __init__(self, candidates: list, threshold):
        self.candidates = candidates
        self.threshold = threshold

    def find(self) -> dict:
        return list(filter(self.__filter, self.candidates))

    def __filter(self, candidate: dict):

        filters = [

                ## In case you want to set a limit on fuzz.ratio
                # (candidate['similarity'] >= 70) , 

                candidate['classifier_score'] >=self.threshold,

                ## basically ALL correct results match one at least. 
                ## You don't really need this because the ML does this for you
                #  bool(candidate['author_match_one']) ,

                 ## this filter might be useful in tracking medrxiv etc
                 ## so we can set the DOI of the preprint to the manuscript_id
                 ## then this will filter it out.
                #  str(candidate['DOI'])!=str(candidate['manuscript_id']),
        ]

        return all(filters)
