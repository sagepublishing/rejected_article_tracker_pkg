#!/usr/bin/env python
import sys
import os

from rejected_article_tracker.src.RejectedArticlesMatch import RejectedArticlesMatch
from rejected_article_tracker.src.ScholarOneRejectedArticlesMatch import ScholarOneRejectedArticlesMatch

sys.path.append(os.path.abspath("."))

# check models are where they are supposed to be
from .src.ML.ArXivOAIPMH import ArXivOAIPMH
ArXivOAIPMH().ensure_dirs()
from .src.ML.config import Config as config
import shutil
lr_model_path = os.path.join(os.path.dirname(__file__),
                            'src','ML','small_models','lr_model')
dest_model_path = config.old_logreg_model_loc

# and then move the models there.
if not os.path.exists(config.ml_model_dir):
    os.mkdir(config.ml_model_dir)
shutil.copy(lr_model_path, dest_model_path)
