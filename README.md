
# {{ Name }}: check if article has been published

## What is it?

The SAGE rejected article tracker
This package will take metadata(title, authors etc...) for research articles and will find the published versions in CrossRef. 
Presently, the package takes JSON input, but using a library such as [pandas](https://github.com/pandas-dev/pandas) to convert it, spreadsheet data can be used.  

If you are a ScholarOne user, you can produce this easily. More detailed instructions are below. 

## Where to get it

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
 
articles = [
{
      "journal_name": "Trauma, Violence, & Abuse",
      "manuscript_title": "The Impact of Childhood Abuse on the Commercial Sexual Exploitation of Youth. A Systematic Review and Meta-Analysis ",
      "authors": "De Vries, Ieke; Goggin, Kelly",
      "final_decision": "accept"
      "decision_date": "2019-07-20T13:29:58.999Z", # This value is fabricated for the example
      "submission_date": "2018-07-20T13:29:58.999Z",
      "manuscript_id": "TVA-18-057",
    }
]

# @see below for configuration details.
config = {
    "filter_dates": {'from': '2007-01-01', 'to': '2020-07-01'},
    "threshold": 70, # Filters out matches which are less than this nubmer  
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
      "Journal Name": "Trauma, Violence, & Abuse",
      "Manuscript ID": "TVA-18-057",
      "Manuscript Title": "The Impact of Childhood Abuse on the Commercial Sexual Exploitation of Youth. A Systematic Review and Meta-Analysis ",
      "Author Names": "De Vries, Ieke; Goggin, Kelly",
      "Submission Date": "2018-07-20T13:29:58.999Z",
      "Decision Date": "1899-12-30T00:00:00.000Z",
      "Accept or Reject Final Decision": ""
    }
]
"""

# @see below for configuration details.
config = {
    "filter_dates": {'from': '2007-01-01', 'to': '2020-07-01'},
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
    "manuscript_id": "TVA-18-057",
    "raw_manuscript_id": "TVA-18-057",
    "journal_name": "Trauma, Violence, & Abuse",
    "manuscript_title": "The Impact of Childhood Abuse on the Commercial Sexual Exploitation of Youth. A Systematic Review and Meta-Analysis ",
    "submission_date": "2018-07-20",
    "decision_date": "1899-12-30",
    "authors": "Ieke+De Vries, Kelly+Goggin",
    "text_sub_date": "2018-07-20",
    "match_doi": "10.1177/1524838018801332",
    "match_type": "journal-article",
    "match_title": "The Impact of Childhood Abuse on the Commercial Sexual Exploitation of Youth: A Systematic Review and Meta-Analysis",
    "match_authors": "Ieke+De Vries, Kelly E.+Goggin",
    "match_publisher": "SAGE Publications",
    "match_journal": "Trauma, Violence, & Abuse",
    "match_pub_date": "2018-10-10",
    "match_earliest_date": "2018-10-11",
    "match_similarity": 97,
    "match_one": true,
    "match_all": true,
    "match_crossref_score": 107.89555,
    "match_crossref_cites": 3,
    "match_rank": 1,
    "match_total_decision_days": 43384,
    "match_journal_acronym": "TVA"
  }
]
```

Example out when NO match found:

```json
[
  {
    "manuscript_id": "Sage-19-0492",
    "raw_manuscript_id": "Sage-19-0492",
    "journal_name": "SAGE Path",
    "manuscript_title": "Reported Adverse Events with -lactam Antibiotics: Data Mining of the FDA Adverse Events Reporting System",
    "submission_date": "2019-02-07",
    "decision_date": "1899-12-30",
    "authors": "Jielai+Xia, Liang+Tong, Ling+Wang, Wei+Ge, Chanjuan+Li, Chen+Li, Haixia+Hu, Fan+Li, Haona+Li",
    "text_sub_date": "2019-02-07",
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
    "match_total_decision_days": "No Match",
    "match_journal_acronym": "No Match"
  }
]
``` 

---
## Configuration
Configuration is set using a dictionary. The following values can be set: 

| Name | Description | Example
| --- | --- | --- |
| `filter_dates` |  Dates to include articles from and to. Anything outdide of these dates will not be considered | ```{"filter_dates": {'from': '2007-01-01', 'to': '2020-07-01'}}```  
| `threshold` | An integer value which determines the minimum "cut off" for scoring matching articles. Any matching aerticles below this score will not be considered. | `75` |   
---


## License
[MIT](LICENSE.md)

## Contributing
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

Please see the [contributing](CONTRIBUTING.md) for instructions 
