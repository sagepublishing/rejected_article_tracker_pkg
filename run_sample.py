from rejected_article_tracker import ScholarOneRejectedArticlesMatch
import os
import pandas as pd


def run():
    filepath = os.path.abspath(r'rejected_article_tracker/data/fake_rejected_articles.xlsx')
    # read in the sample file
    data = pd.read_excel(filepath)
    # set parameters
    config = {
                # from 0.0 - 1.0 
                # Set higher for better precision, lower for better recall
                "threshold": 0.5, 
                # any number from 1 - 10. If there are multiple versions of the article out there, it's worth picking  number >1
                "max_results_per_article":10, 
                # limit results to these types see: https://api.crossref.org/types
                "article_types":['journal-article',
                                'posted-content',
                                'book-chapter',
                                'proceedings-article'], 
            }
    # convert dataframe to a list of dicts
    articles = data.T.to_dict().values()
    # The CrossRef API requires an email address for lookups.
    # add MY_EMAIL as an environment variable,
    # or simply set `email = YOUR EMAIL ADDRESS`
    email = os.getenv('MY_EMAIL','')
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