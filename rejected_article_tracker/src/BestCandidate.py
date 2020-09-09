import numpy as np


class BestCandidate():
    def __init__(self, candidates: list, threshold):
        self.candidates = candidates
        self.threshold = threshold

    def find(self) -> dict:
        candidates = list(filter(self.__filter, self.candidates))
        result_scores = list(map(lambda c: c['classifier_score'], candidates))
        return candidates[np.argmax(result_scores)] if len(candidates) > 0 else None

    def __filter(self, candidate: dict):
        return (candidate['similarity'] >= self.threshold) & \
               candidate['author_match_one']
