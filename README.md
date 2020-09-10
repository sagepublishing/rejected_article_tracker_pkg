
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
      "manuscript_title": "The Impact of Childhood Abuse on the Commercial Sexual Exploitation of Youth. A Systematic Review and Meta-Analysis ",
      "authors": "De Vries, Ieke; Goggin, Kelly",
      "manuscript_id": "TVA-18-057",
      "submission_date": "2018-07-20T13:29:58.999Z",
      "decision_date": "2019-07-20T13:29:58.999Z", # This value is fabricated for the example
      "journal_name": "Trauma, Violence, & Abuse",
      "final_decision": ""
    }
]


# A dict of configuration.
# See below for more details.
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



## Usage with directly downloaded Scholar One data

```python

from rejected_article_tracker import ScholarOneRejectedArticlesMatch

# A spreadsheet downloaded from S1 and converted to a python dict:   
articles = [
   {
      "Manuscript Title": "The Impact of Childhood Abuse on the Commercial Sexual Exploitation of Youth. A Systematic Review and Meta-Analysis ",
      "Author Names": "De Vries, Ieke; Goggin, Kelly",
      "Manuscript ID": "TVA-18-057",
      "Submission Date": "2018-07-20T13:29:58.999Z",
      "Decision Date": "1899-12-30T00:00:00.000Z",
      "Journal Name": "Trauma, Violence, & Abuse",
      "Accept or Reject Final Decision": ""
    }
]

... # Assume similar values in example above 


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