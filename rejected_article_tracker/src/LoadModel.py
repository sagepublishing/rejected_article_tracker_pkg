

from .ML.config import Config as mlconfig
import os, pickle

class LoadModel:

    def __init__(self):

        self.clf = self.load_model()
        
    def load_model(self):
        # if we have created a new model using the training functions
        # then this will pick that model instead of the standard one.
        new_model_path = mlconfig.new_logreg_model_loc
        old_model_path = mlconfig.old_logreg_model_loc
        if os.path.exists(new_model_path):
            with open(new_model_path, 'rb') as f:
                clf = pickle.load(f)
        else:
            with open(old_model_path, 'rb') as f:
                clf = pickle.load(f)
        return clf