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

The tracker can be used to track rejected articles, or to perform DOI-resolution for other reasons, such as assigning DOIs to ArXiv preprints in order to connect the preprints to their published versions.

The tracker is available as [a Python package](https://github.com/ad48/rejected_article_tracker_pkg) with [a temporary live demonstration](https://rejectedarticlestorage.z6.web.core.windows.net/) scheduled to run until mid-2021.

# Statement of need

Rejected article tracking has been performed in a number of research settings [@Wijnhoven2010; @Docherty2017; @Citerio2018; @Chung2020]. Typically, this is done by manually searching for rejected articles over a small dataset. However, commercial rejected article trackers are available [@HighWire; @Incorvia2015].

To date, a lack of open source tools has prevented easy acquisition of data on rejected articles for analysis.

Data acquired by rejected article tracking makes various insights into the peer-review and publication processes possible.

1. It is possible to measure the rate at which rejected articles are published and cited. This shows the effectiveness of journal peer-review in identifying (or failing to identify) flaws in research.

2. Instances of author-misconduct can be identified and studied. 

    - Dual submission (where an author has submitted the same article to multiple journals simultaneously) can be detected automatically. 

    - When a rejected article has been later published _and then retracted_ due to fraud or other misconduct, researchers can identify failings in peer-review that may have missed obvious signs of misconduct.

3. We speculate that further, as yet unstudied, forms of misconduct can be investigated with data retrieved this way.

    - Research articles may be edited fraudulently between rejection by one journal and acceptance by another. This is a very rare occurrence, but it may be possible to identify and study such cases.

    - Often, research articles are rejected due to significant fundamental flaws in the science they present. If an author goes on to publish such work following rejection for this reason, it may simply be because the author disagreed that there were fundamental flaws in the work. However, it is possible that the author does so with deliberate intent to publish flawed work. This form of misconduct has never been studied and rejected article tracking is one step in doing so. 

As the rate of creation of research manuscripts continues to grow at a rapid pace, the need to understand the peer-review process, improve efficiencies and tackle abuse becomes all the more pressing. 


# Acknowledgements

We thank Helen King and Martha Sedgwick for support and advice in the development of this application. 

# References