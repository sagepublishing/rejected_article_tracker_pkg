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
  - name: SAGE Publishing, 1 Oliver's Yard, London, EC1Y 1SP
date: 4 November 2020
bibliography: paper.bib

---
# Summary
Over 3m peer-reviewed research papers are published in academic journals each year [@STM]. An unknown number of research papers are also rejected by peer-review. There is little understanding of what happens to those rejected papers.

[CrossRef](https://www.crossref.org/about/) is a not-for-profit organisation which maintains a large dataset of metadata describing the majority of published peer-reviewed research papers. The SAGE rejected article tracker extracts knowledge from that dataset by analysing data from the [CrossRef REST API](https://github.com/CrossRef/rest-api-doc). 

Given metadata for a rejected article, the rejected article tracker will:
* search CrossRef's API to retrieve a list of possible matches and 
* select the most likely correct result from that list using simple machine learning.

The tracker is available as [a Python package](https://github.com/ad48/rejected_article_tracker_pkg) with [a temporary live demonstration](https://rejectedarticlestorage.z6.web.core.windows.net/) scheduled to run until mid-2021.

# Statement of need

Rejected article tracking has been performed in a number of research settings [@Wijnhoven2010; @Docherty2017; @Citerio2018; @Chung2020]. Typically, this is done by manually searching for rejected articles over a small dataset. However, commercial rejected article trackers are available [@HighWire; @Incorvia2015].

As the market for journal publications continues to grow at a rapid pace, it is critical that publishing houses are able to reach sound publication decisions.

Being able to track rejected articles can, for example, allow researchers working with publishing houses to see which of their rejected articles have been published elsewhere, and which have been cited. This is valuable feedback which can help publishers improve the quality of research assessment offered by their peer-review process. Furthermore, preventing unnecessary rejections of acceptable content reduces the publisher's costs as well as those of the academy (who as authors, referees and editors volunteer a significant amount of time to the peer-review process).


# Acknowledgements

We thank Helen King and Martha Sedgwick for support and advice in the development of this application. 

# References