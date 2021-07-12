
# SAGE Rejected Article Tracker: Check if an article has been published elsewhere.

## What is it?

The SAGE rejected article tracker
This package will take metadata(title, authors etc...) for research articles ("query articles") and will find the published versions in CrossRef ("match articles"). 

The published versions are selected using very simple machine-learning. 
1. Numerical values are calculated for the difference in the titles of each query article and each candidate match article returned by CrossRef.
2. ArXiv preprints with known DOIs are used to train a simple logistic regression to find the correct candidate for each query. 

This process is approximately 95% accurate. However, the package includes code to recreate the training dataset using the ArXiv and CrossRef APIs. This training dataset can be used to test other approaches to this problem and similar problems (such as detecting duplicate articles).

Presently, the package takes JSON input, but using a library such as [pandas](https://github.com/pandas-dev/pandas) to convert it, spreadsheet data can be used.  

If you are a ScholarOne user, you can produce this easily. More detailed instructions are below. 

## Where to get it?

Although the source code is on Github, the latest release is always published to the [Python package index](https://pypi.org/project/rejected-article-tracker).

```
pip install rejected_article_tracker
```

## Dependencies
- [pandas](https://pypi.org/project/pandas)
- [openpyxl](https://pypi.org/project/openpyxl)
- [xlsxwriter](https://pypi.org/project/xlsxwriter)
- [fuzzywuzzy](https://pypi.org/project/fuzzywuzzy)
- [requests](https://pypi.org/project/requests)
- [sklearn](https://pypi.org/project/sklearn)
- [numpy](https://pypi.org/project/numpy)


## Typical Usage

```python
# Import package
from rejected_article_tracker import RejectedArticlesMatch

# Create a list of article data dicts.
# PLEASE NOTE: Due to reliance on 3rd party APIs, the more articles the longer it takes.
 
articles = [ # some values fabricated for the example
{
      "Journal Name": "The International Journal of Robotics Research",
      "Manuscript Title": "Learning hand-eye coordination for robotic grasping with deep learning and large-scale data collection ",
      "Author Names": "Levine, Sergey; Pastor, Peter; Krizhevsky, Alex; Ibarz, Julian; Quillen, Deirdre",
      "Accept or Reject Final Decision": "",
      "Decision Date": "2019-01-01T13:29:58.999Z", 
      "Submission Date": "2018-10-01T13:29:58.999Z",
      "Manuscript ID": "ABC-18-070",
    }
]

# @see below for configuration details.
config = {
    "threshold": 70, # Filters out matches which have a fuzz.ratio below this value (fuzz.ratio is a normalised form of Levenshtein distance)
}


# The CrossRef API requires an email address for lookups.    
email = "someome@example.com"


# Define a 'results' list. 
# This is a little unconventional and not great practice. 
# However, injecting a results variable, allows us grab already processed articles
# in case of an issue with 3rd party APIs. 
# This would then mean only the remaining articles would need to be rerun.
results = []

# Run match
RejectedArticlesMatch(
            articles=articles,
            config=config,
            email=email,
            results=results
        ).match()

print(results)
```
---
### Article format 
This is how each article should be structured:

| Property | Contents |
| --- | --- |
| `journal_name` | Simply the name of the journal e.g. ‘Proceedings of mysociety’ |
| `manuscript_title` | The text of the title of the manuscript you are looking for. The article will not be found without this. |
| `authors` | This is a critical part of the input data and MUST be formatted ‘LastName1, FirstName1; LastName2, FirstName2 …’ So note that authors names appear with their lastname first and then a comma, followed by the first name. Then, when we have multiple authors on a paper, we separate them with semicolons. |
| `final_decision` | E.g. ‘Accept’ or ‘Reject’ (the application will simply ignore everything that is listed as ‘Accept’) |
| `decision_date` | The date of final rejection from your journal. Should be a date string format, like: “YYYY-MM-DD”, “YYYY-MM-DD hh:mm:ss” Either format is fine. |
| `submission_date` | Same format as decision date. |
| `manuscript_id` | This can be any unique id that you use to identify the article. If it is formatted in the way that ScholarOne format their ids, then revision numbers will be ignored so that each article is only searched for once. So ‘ABC-20-123’, ‘ABC-20-123.R1’ and ‘ABC-20-123.R2’ all become ‘ABC-20-123’ |

---
<br>
<br>

## Usage with directly downloaded Scholar One data
**Preparing the input:**

If using Scholar One, under `‘Peer Review Details Reports’` select `‘Build Your Own Reports’`. 
The report should have the following columns:

```
‘Journal Name', 'Manuscript ID', 'Manuscript Title', 'Author Names', 'Submission Date', 'Decision Date', 'Accept or Reject Final Decision'
```

It’s ok to include other columns in the Excel file, but they are not needed. 
_IMPORTANTLY:_ remember to download your report as Excel 2007 Data Format.

If not using ScholarOne, then simply prepare your submission data with the above column headings ensuring that
- Author lists are correctly formatted `last_name1, first_name1; last_name2, first_name2;...`
- Date columns (`Submission Date` and `Decision Date`) are correctly formatted, either as datetime strings (as below) or as simple date strings, e.g. `2010-12-31` for 31 December 2010.

**Usage:**
```python

from rejected_article_tracker import ScholarOneRejectedArticlesMatch
import pandas as pd

df = pd.read_excel("/path/to/file")
allowed_cols = [
    'Journal Name',
    'Manuscript ID',
    'Manuscript Title',
    'Author Names',
    'Submission Date',
    'Decision Date',
    'Accept or Reject Final Decision'
]
articles = df[allowed_cols].to_dict('records')

# Which might look like:
"""  
articles = [
{
      "Journal Name": "The International Journal of Robotics Research",
      "Manuscript Title": "Learning hand-eye coordination for robotic grasping with deep learning and large-scale data collection",
      "Author Names": "Levine, Sergey; Pastor, Peter; Krizhevsky, Alex; Ibarz, Julian; Quillen, Deirdre",
      "Accept or Reject Final Decision": "",
      "Decision Date": "2019-01-01T13:29:58.999Z", 
      "Submission Date": "2018-10-01T13:29:58.999Z",
      "Manuscript ID": "ABC-18-070",
    }
]
"""

# @see below for configuration details.
config = {
    "threshold": 70, # Filters out matches which are less than this nubmer  
}

# The CrossRef API requires an email address for lookups.    
email = "someome@example.com"

# Define a 'results' list.
results = []

# Run match
ScholarOneRejectedArticlesMatch(
    articles=articles,
    config=config,
    email=email,
    results=results
).match()

print(results)
```


## Example output

Example output when match found:
```json
[
  {
    "manuscript_id": "ABC-18-070",
    "raw_manuscript_id": "ABC-18-070",
    "journal_name": "The International Journal of Robotics Research",
    "manuscript_title": "Learning hand-eye coordination for robotic grasping with deep learning and large-scale data collection",
    "submission_date": "2018-10-01",
    "decision_date": "2019-01-01",
    "authors": "Levine, Sergey; Pastor, Peter; Krizhevsky, Alex; Ibarz, Julian; Quillen, Deirdre",
    "text_sub_date": "2018-07-20",
    "match_doi": "10.1177/0278364917710318",
    "match_type": "journal-article",
    "match_title": "Learning hand-eye coordination for robotic grasping with deep learning and large-scale data collection",
    "match_authors": "Levine, Sergey; Pastor, Peter; Krizhevsky, Alex; Ibarz, Julian; Quillen, Deirdre",
    "match_publisher": "SAGE Publications",
    "match_journal": "The International Journal of Robotics Research",
    "match_pub_date": "2019-10-10",
    "match_earliest_date": "2019-10-10",
    "match_similarity": 97,
    "match_one": true,
    "match_all": true,
    "match_crossref_score": 107.89555,
    "match_crossref_cites": 3,
    "match_rank": 1,
    "match_total_decision_days": 43384
  }
]
```

Example out when NO match found:

```json
[
  {
    "manuscript_id": "ABC-18-070",
    "raw_manuscript_id": "ABC-18-070",
    "journal_name": "The International Journal of Robotics Research",
    "manuscript_title": "Learning hand-eye coordination for robotic grasping with deep learning and large-scale data collection",
    "submission_date": "2018-10-01",
    "decision_date": "2019-01-01",
    "authors": "Levine, Sergey; Pastor, Peter; Krizhevsky, Alex; Ibarz, Julian; Quillen, Deirdre",
    "text_sub_date": "2018-07-20",
    "final_decision": "",
    "match_doi": "No Match",
    "match_type": "No Match",
    "match_title": "No Match",
    "match_authors": "No Match",
    "match_publisher": "No Match",
    "match_journal": "No Match",
    "match_pub_date": "No Match",
    "match_earliest_date": "No Match",
    "match_similarity": "No Match",
    "match_one": "No Match",
    "match_all": "No Match",
    "match_crossref_score": "No Match",
    "match_crossref_cites": "No Match",
    "match_rank": "No Match",
    "match_total_decision_days": "No Match"
  }
]
``` 

**To rebuild the training dataset and train a new model**

Note that rebuilding the training dataset relies on external APIs and can be a very slow process (a few days depending on response times). However, once acquired, model training and testing takes seconds.

```python
from rejected_article_tracker.src.ML.Train import LogReg

LogReg().best_model_to_file()
```


---
## Configuration
Configuration is set using a dictionary. The following values can be set: 

| Name | Description | Example
| --- | --- | --- |  
| `threshold` | An integer value which determines the minimum "cut off" for scoring matching articles. Any matching articles below this score will not be considered. | `70` |   
---


## License
[MIT](LICENSE.md)

## Contributing
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

Please see the [contributing](CONTRIBUTING.md) for instructions 
