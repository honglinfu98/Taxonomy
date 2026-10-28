"""RQ7: does the ontology improve a downstream classification of Web-sourced token descriptions?

Data: token descriptions and the site's own category tags from CoinGecko (collect.py). The
categories are assigned by the site, not by us, so they are an independent label space; the
descriptions are project- or site-written Web text. Systems (classify.py): an LLM that sees the
description and the category list (without the ontology); the same with the catalogue block and
an instruction to classify through its dimensions first (with the ontology as context); the
production tagger's ontology tags alone, mapped to categories by a second call (the ontology as
the only evidence); and supervised logistic regression on TF-IDF, on ontology tags, and on both
(supervised.py). Scored on micro- and macro-F1 over the retained categories (report.py).
"""
