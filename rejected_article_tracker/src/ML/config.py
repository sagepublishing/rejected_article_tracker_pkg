import os
import datetime


class Config:
    myemail = os.getenv('MY_EMAIL', '')
    user_home_dir = os.path.expanduser('~')
    
    # ml code location
    

    ml_dir = os.path.abspath('.rejected_article_tracker/src/ML')

    # data_locations
    main_data_dir = os.path.join(user_home_dir,'rejected_article_tracker')
    ml_data_dir = os.path.join(main_data_dir,'data')
    oai_pmh_dataloc = os.path.join(ml_data_dir,'oai_pmh_data')
    crossref_doi_dataloc = os.path.join(ml_data_dir,'cr_doi_results.jsonl')
    crossref_search_dataloc = os.path.join(ml_data_dir,'cr_search_results.json')
    crossref_search_jsonl_dataloc = os.path.join(ml_data_dir,'cr_search_results.jsonl')
    training_dataloc = os.path.join(ml_data_dir,'training_dataframe.csv')
    clean_training_dataloc = os.path.join(ml_data_dir,'clean_training_dataframe.csv')


    # model locations
    # file_dir = os.path.dirname(__file__)
    ml_model_dir = os.path.join(user_home_dir,'rejected_article_tracker','models')
    old_logreg_model_loc = os.path.join(ml_model_dir, 'lr_model')
    new_logreg_model_loc = os.path.join(ml_model_dir, 'lr_model_new')
     
    # training data parameters
    # CARE with these. 
    # the API reader will pull everything UPDATED after the start year
    # It will stop when it reaches n_recs_from_oai_pmh
    # if the number of docs at that point is < max_training_docs,
    # the process will repeat. 
    start_year_for_training = 2012
    current_year = int(datetime.datetime.now().year)
    allowed_values = list(range(2007,current_year+1))
    if start_year_for_training not in allowed_values:
        raise ValueError('Invalid value for start_year_for_training. Must be between 2007 and current year.')

    # If using 2012, we get around 80k docs (with ~50% having DOIs)
    # So this number is actually double the number of training docs we will use
    # We will check the total before processing any data
    max_training_docs = 90000

    # here 200000 works for 2012, but if you want to try a different year
    # you will need to figure out the right number of docs to acquire
    # this will be approximately the number of preprints added to arXiv
    # since 2007.
    n_recs_from_oai_pmh = 200000


    predictor_cols = [
        
        'similarity',
        'author_match_all',
        # NOTE - you can't use score because the
        # DOI lookups all default to score ==1.0
        # potentially limit data to results where we have a score!=1?
        # 'score',
        # 'rank',
        'n_auths_query'
        
    ]

    target_col = 'correct_yn'
