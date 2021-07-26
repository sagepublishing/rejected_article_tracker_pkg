from rejected_article_tracker import ScholarOneRejectedArticlesMatch
import os
import pandas as pd


def run():
    filepath = os.path.abspath(r'rejected_article_tracker/data/fake_rejected_articles.xlsx')
    # read in the sample file
    data = pd.read_excel(filepath)
    # set parameters
    config = {
    "threshold": 70, # Filters out matches which are less than this nubmer  
        }
    articles = data.T.to_dict().values()
    # The CrossRef API requires an email address for lookups.    
    email = ""
    # Define a 'results' list.
    results = []

    # Run match
    ScholarOneRejectedArticlesMatch(
        articles=articles,
        config=config,
        email=email,
        results=results
    ).match()

    result_df = pd.DataFrame(results)


    print('FOUND RESULTS:')
    print(result_df)
    output_path = os.path.abspath('output.xlsx')
    print(f'output written to {output_path}' )
    result_df.to_excel(output_path)



if __name__ == '__main__':
    run()