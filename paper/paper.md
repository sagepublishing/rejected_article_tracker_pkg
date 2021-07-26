---
title: 'The SAGE Rejected Article Tracker'
tags:
  - Python
  - peer-review
  - academic publishing
  - crossref
authors:
  - name: Andrew Hails
    orcid: 0000-0002-1014-621X
    affiliation: 1
  - name: Adam Day
    orcid: 0000-0002-8529-9990
    affiliation: 1
affiliations:
  - name: "SAGE Publishing, 1 Oliver's Yard, London, EC1Y 1SP"
  - index: 1
date: 4 November 2020
bibliography: paper.bib

---
# Summary
Over 3m peer-reviewed research papers are published in academic journals each year [@STM]. An unknown number of research papers are also rejected by peer-review. There is little understanding of what happens to those rejected papers.

[CrossRef](https://www.crossref.org/about/) is a not-for-profit organisation which maintains a large set of metadata describing the majority of published peer-reviewed research papers. The SAGE rejected article tracker extracts knowledge from that dataset by analysing data from the [CrossRef REST API](https://github.com/CrossRef/rest-api-doc). 

Given metadata for a rejected article, the rejected article tracker will:

* search CrossRef's API to retrieve a list of possible matches and 

* select the most likely correct result from that list using simple machine learning.

The target audience for the tracker is researchers studying rejected articles. The task performed by the tracker is record-linkage, i.e. finding the correct CrossRef metadata record given incomplete data about a paper. So, while the intended use of the tracker is to track rejected articles, it might be used by researchers performing record-linkage for other reasons, such as connecting preprints to their published versions, e.g. [@Cabanac2021]. This is a particularly topical application at the current time due to the rapid growth of preprint servers in recent years [@Hoy2020].

The tracker is available as [a Python package](https://github.com/ad48/rejected_article_tracker_pkg) with [a temporary live demonstration](https://rejectedarticlestorage.z6.web.core.windows.net/) scheduled to run until mid-2021.

# Statement of need

As the rate of creation of research manuscripts continues to grow at a rapid pace, the need to understand the peer-review process, improve efficiencies and tackle abuse becomes all the more pressing. 

Rejected article tracking has been performed in a number of research settings [@Wijnhoven2010; @Docherty2017; @Citerio2018; @Chung2020]. Typically, this is done by manually searching for rejected articles over a small dataset. However, commercial rejected article trackers are available [@HighWire; @Incorvia2015]. To date, a lack of open source tools has prevented easy acquisition of data on rejected articles for analysis.

Data acquired by rejected article tracking makes various insights into the peer-review and publication processes possible. E.g. 

- It is possible to measure the rate at which rejected articles are published and cited. This provides evidence for the effectiveness of journal peer-review in identifying (or failing to identify) flaws in research.

Rejected article tracking is also valuable to the study of scientific misconduct (examples: [@Hesselmann2017; @Ding2019; @Bozzo2017]). 

Common forms of author-misconduct can be identified and studied. 

- Dual submission (where an author has submitted the same article to multiple journals simultaneously) can be detected retrospectively with a high-degree of confidence. 

- In a similar way, self-plagiarism can potentially be detected quickly and cheaply by checking new-submissions against CrossRef with the tracker. Although, the well-established [CrossCheck](https://www.crossref.org/services/similarity-check/) service based on [iThenticate](https://www.ithenticate.com/) should yield superior results. 

- When a rejected article has been later published _and then retracted_ due to fraud or other misconduct, this can allow the publisher who rejected the paper to identify that case of misconduct in their own part of the peer-review system.

Finally, the rejected article tracker can also be used to link preprints with their published versions. Due to the rapid recent growth in preprint servers [@Fraser2020], there is a growing need to improve the data-quality surrounding preprints. 

The rejected article tracker is set up, by default, to accept data in the format exported by [ScholarOne](https://clarivate.com/webofsciencegroup/solutions/scholarone/), a popular system for managing peer-review. However, the input data required is minimal, so data from any peer-review management system should be easily adapted for the tracker. Instructions are given in the `Readme.md` file of [the github repository](https://github.com/ad48/rejected_article_tracker_pkg).

## How the matching algorithm works

The CrossRef API is often used to perform record-linkage. A typical use-case would be for the purpose of adding metadata to incomplete references in the reference-list of a research paper [@Tkaczyk2018]. Under this typical use-case, there is often other data available, such as journal name and publication date as well as issue, volume or page numbers. However, if we wish to track rejected articles, it is likely that we only have the title and author-names for an article and there is a lower chance that it exists in CrossRef's data (since not all rejected articles are published). So, searching the API for just these 2 things often results in incorrect results being retrieved.

We begin with a dataset of ArXiv preprint metadata retrieved from the [ArXiv OAI-PMH API](https://arxiv.org/help/oa/index). This dataset resembles journal submission data in that it includes the titles and author names of preprints. In many cases, this data also includes the DOI of the same article when it was published. This means that we know the correct result of a record-linkage process for this article. We find that the title and author lists are not always identical. Titles often undergo minor (and occasionally major) changes and author lists can also change in a number of ways (full names might be used instead of initials, or perhaps new authors are added to an author list at some point in the process).

We search the CrossRef API for each preprint's DOI as well as the best incorrect search result. This means that we can fill out 2 rows of a table of data for each preprint.

| preprint title | preprint authors | published title | published authors | correct/incorrect |
|-|-|-|-|-|
| title1| author_list1 | title2 | author_list2 | correct |
| title1| author_list1 | title3 | author_list3 | incorrect |

We then:

- Calculate the Levenshtein distance between the titles in each row. This is normalised to a number between 0 and 100 using the `fuzz.ratio` method from the [Python `fuzzywuzzy` package](https://pypi.org/project/fuzzywuzzy/).

- Normalise all author names to a single string of `first_initial+last_name` in lower case. Then calculate 2 boolean values: one showing if there is a 100% match in author lists and one showing if there is at least 1 author name matching in the 2 lists. 

This gives us a table of numerical data:

| levenshtein_similarity | authors_match_one | authors_match_all | label |
|-|-|-|-|
| 98 | 1 | 1 | 1 |
| 70 | 1 | 0 | 0 |

Then this data can be used to create a Logistic Regression classifier model using [Scikit-Learn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) with `label` as our target variable. The model essentially learns what the typical difference is between a preprint title and its published version - a bespoke form of fuzzy matching. 

This model can then be used to classify search results from the CrossRef API in order to find the correct DOI, and other metadata, for a rejected article.

The complete code required to build and customise the training dataset is included in [the SAGE Rejected Article Tracker](https://github.com/ad48/rejected_article_tracker_pkg).

## The dataset

 The training dataset is also useful for other tasks such as identifying duplicate submissions. E.g. if an author submits a paper to 2 or more journals at once, fuzzy matching on titles and author lists is an effective way to identify this behaviour. 

 A dataset similar to the one used to train the SAGE Rejected Article Tracker is available to download from [Zenodo](http://doi.org/10.5281/zenodo.5122848) [@SAGERATData].


# Acknowledgements

We thank Helen King and Martha Sedgwick for support and advice in the development of this application. 

# References