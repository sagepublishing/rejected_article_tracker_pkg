import os
import pandas as pd
# import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import GridSearchCV
import pickle
import multiprocessing

from .TrainingData import TrainingData

from .config import Config as config

import logging
logger = logging.getLogger(__name__)

class LogReg:

    def get_data(self, df):
        
        predictor_cols = config.predictor_cols
        target_col = config.target_col
        all_cols = predictor_cols+[target_col]
        dfnum = df[all_cols].apply(pd.to_numeric, args=('coerce',)).dropna()
        y = dfnum.pop(target_col).apply(pd.to_numeric, args=('coerce',)).values
        X = dfnum.values
        return X, y

    def split_data(self,X,y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        test_size=0.2, 
                                                        random_state=100)
        return X_train, X_test, y_train, y_test


    def train_model(self, X, y):
        X_train, X_test, y_train, y_test = self.split_data(X,y)
        clf = LogisticRegression(random_state=0)
        clf.fit(X_train,y_train)

        # return train and test scores
        return clf.score(X_train,y_train),clf.score(X_test,y_test)

    def grid_search(self, X, y):

        n_cpus = multiprocessing.cpu_count()
        param_grid = {'solver':['liblinear'],
                    'penalty': ['l1','l2'], 
                    # 'class_weight':[None,'balanced'],
                    'C': [0.001,0.01,0.1,1,10],
                    'tol':[0.00001,0.0001,0.001,0.01],
                    'max_iter':[10000]
                    }

        gs = GridSearchCV(LogisticRegression(), 
                            param_grid=param_grid,
                            n_jobs = n_cpus-1, 
                            cv = 5,
                            verbose = 1)
        X_train, X_test, y_train, y_test = self.split_data(X,y)
        gs.fit(X_train,y_train)
        
        return gs.best_estimator_

    def best_model_to_file(self):
        # TODO - train on the split data
        # so that you can still test the model on unseen. 
        df = TrainingData().load_gen_clean_training_df()
        logger.info('Model training beginning with dataframe shape: {}'.format(df.shape))
        X,y = self.get_data(df)
        logger.info('X shape: {} | y shape: {}'.format(X.shape, y.shape))
        best_model = self.grid_search(X, y)
        
        # ensure location exists
        if not os.path.exists(config.ml_model_dir):
            os.mkdir(config.ml_model_dir)

        with open(config.new_logreg_model_loc,'wb') as f:
            pickle.dump(best_model,f)
        logger.info('Several models built and tested. Now written to file.')
        self.test_best_model()

    def test_best_model(self):

        if os.path.exists(config.new_logreg_model_loc):
            with open(config.new_logreg_model_loc, 'rb') as f:
                clf = pickle.load(f)
        else:
            with open(config.old_logreg_model_loc, 'rb') as f:
                clf = pickle.load(f)

        df = TrainingData().load_gen_clean_training_df()
        X,y = self.get_data(df)
        X_train, X_test, y_train, y_test = self.split_data(X,y)

        y_pred = clf.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        logger.info('Model scoring:')
        logger.info('accuracy: {}'.format(accuracy))
        logger.info('precision: {}'.format(precision))
        logger.info('recall: {}'.format(recall))
        logger.info('f1_score: {}'.format(f1))
        print('CONFUSION MATRIX')
        print(confusion_matrix(y_test, y_pred))

# TODO - visualise a permutation test. Seems like a good way to measure success: https://scikit-learn.org/stable/auto_examples/feature_selection/plot_permutation_test_for_classification.html#sphx-glr-auto-examples-feature-selection-plot-permutation-test-for-classification-py
# save the model automatically. User can delete if it's no good
