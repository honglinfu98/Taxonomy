# References for the WWW '27 paper

70 PDFs, one BibTeX entry each in `candidates.bib` (keys match the `file:` note).
The 35 WWW exemplars live in `../WWW/`; the paper's current bibliography is in
`../paper/references.bib` (22 academic entries plus the regulatory instruments).
Together with the entries already cited, this folder gives around 90 academic
candidates; pick about 30 of them to reach the target of roughly 50 references
in the main text.

## Where each paper fits

### Introduction and Related Work: taxonomy induction before LLMs
Use these to show the lineage of "induce the hierarchy from text" and the fact
that every method assumes the nodes are terms, not dimensions.

| File | Cite for |
|---|---|
| COLING1992 Hearst | pattern-based hypernym extraction, the origin of taxonomy induction from text |
| ACL2006 Snow et al. | probabilistic taxonomy induction from heterogeneous evidence |
| EMNLP2010 Kozareva and Hovy | taxonomy construction from the Web with patterns |
| ACL2010 Navigli and Velardi | definition and hypernym extraction from definitional sentences (closest classic analogue to definitions-first) |
| CL2013 OntoLearn Reloaded | end-to-end taxonomy induction evaluated on gold hierarchies |
| SIGMOD2012 Probase | probabilistic is-a edges at Web scale; precedent for weighted edges |
| EMNLP2017 Wang et al. survey | survey of taxonomy learning from corpora |
| SemEval2016 TExEval-2 | the shared-task evaluation protocol for induced taxonomies |
| arXiv2017 Camacho-Collados | why the field moved from full taxonomies to hypernymy detection (motivates evaluating edges) |
| KDD2018 TaxoGen, KDD2018 HiExpan, KDD2020 CoRel | topic-taxonomy construction by clustering and expansion |
| ACL2018 Mao et al. | reinforcement learning for taxonomy induction |
| KDD2021 GenTaxo, EMNLP2023 TacoPrompt, WWW2023/IJCAI2024 BoxTaxo | taxonomy completion and expansion baselines beyond the WWW set |

### Related Work: LLMs for taxonomies, ontologies and knowledge graphs
| File | Cite for |
|---|---|
| NAACL2021 Chen et al. | taxonomies from pretrained LM prompting |
| StarSEM2022 Jain and Espinosa Anke | zero-shot hypernymy from LMs |
| ACL2024 TaxoLLaMA, ACL2024 TaxoInstruct | instruction-tuned LLMs for taxonomy tasks |
| CIKM2024 Chain-of-Layer | iterative LLM prompting for taxonomy induction from few examples |
| arXiv2024 Gunn et al. | LLM-built entity type taxonomy |
| NeurIPS2024 OLLM | end-to-end ontology learning with LLMs, evaluated against gold ontologies |
| arXiv2023 Funk et al., arXiv2024 Kommineni et al. | LLM ontology construction pipelines |
| KCAP2023 OLaLa | LLM ontology matching (alias and cross-source merging) |
| JBS2024 DRAGON-AI | retrieval-augmented ontology generation |
| TKDE2024 Pan et al., WWWJ2024 Zhu et al. | LLM and KG unification, KG construction surveys |
| arXiv2024 GraphRAG | global summarisation over an LLM-built graph |

### Related Work: inducing a label space from text with LLMs
These are the nearest non-taxonomy relatives of term type induction.

| File | Cite for |
|---|---|
| NAACL2024 TopicGPT | LLM generates and refines a topic hierarchy from documents |
| CHI2024 LLooM | concept induction from unstructured text with LLMs |
| TACL2024 Viswanathan et al., EMNLP2023 ClusterLLM, EMNLP2023 GoalEx | LLM-guided clustering with language descriptions |
| NeurIPS2023 Zhong et al. | goal-driven discovery of differences described in language |

### Related Work: hierarchical text classification
| File | Cite for |
|---|---|
| AAAI2019 WeSHClass, NAACL2021 TaxoClass | weakly supervised hierarchical classification from class names |
| ACL2020 HiAGM, ACL2022 HGCLR | hierarchy-aware encoders (the supervised baselines TELEClass compares to) |

### Method 4.3 and 4.4: whole-corpus context and citation verification
| File | Cite for |
|---|---|
| MLSys2024 Prompt Cache | prefix caching as the mechanism behind one cached corpus |
| TACL2024 Lost in the Middle | position effects in long contexts (limitation to acknowledge) |
| arXiv2024 LOFT, EMNLP2024 Li et al., ICLR2024 Xu et al., ICLR2025 Jin et al. | long context versus retrieval, the trade-off behind choosing whole-corpus over RAG |
| CL2023 AIS (Rashkin et al.) | attributable-to-identified-sources, the definition of a supported citation |
| EMNLP2023 ALCE, arXiv2022 GopherCite, arXiv2022 Attributed QA | generating text with verifiable quotes and citations |
| EMNLP2023 Liu et al. verifiability, EMNLP2023 Yue et al. | measuring citation support and automatic attribution evaluation |
| EMNLP2024 Attribute First | locally attributable generation (plan-then-cite) |
| EMNLP2023 FActScore, CSUR2023 hallucination survey | atomic-fact precision and the hallucination problem the verifier guards against |

### Problem and Discussion: legal text, definitions, regulatory domain
| File | Cite for |
|---|---|
| SemEval2020 DEFT | definition extraction as a task |
| ACL2022 LexGLUE, EMNLP2021 MultiEURLEX, EMNLP2023 LEXTREME, NeurIPS2021 CUAD, NeurIPS2023 LegalBench | legal NLP benchmarks; MultiEURLEX for EuroVoc-style hierarchical legal labels |
| ACL2020 Zhong et al. | survey of legal AI |
| arXiv2023 Savelka and Ashley, arXiv2023 Savelka et al. | GPT zero-shot annotation of legal text and explanation of legal concepts |

### Introduction and Corpus: crypto-asset and DLT taxonomies
| File | Cite for |
|---|---|
| ClusterComp2022 Ballandies et al. | DLT design taxonomy from the literature |
| IJDSA2021 Di Angelo and Salzer | token identification and standards on Ethereum |
| AFT2022 SoK DeFi, SP2023 SoK DeFi attacks | DeFi building blocks and risk vocabulary |

### Experiments: evaluation
| File | Cite for |
|---|---|
| NeurIPS2023 MT-Bench | LLM-as-judge and its agreement with humans, if an LLM grader is used for edges or tags |
| ACL1994 Wu and Palmer | Wu&P similarity, if hierarchy placement is scored against an expert taxonomy |
| SemEval2016 TExEval-2 | edge precision, recall and F1 against a gold hierarchy |

## Not downloadable from this machine
The ACM DL, NSF PAR, Stanford and SSRN hosts refuse automated requests. Fetch
these by hand if needed:

- Shang et al., NetTaxo (WWW '20), https://doi.org/10.1145/3366423.3380259 (PAR: https://par.nsf.gov/servlets/purl/10160122)
- Manzoor et al., Arborist (WWW '20), https://ai.stanford.edu/~jure/pubs/arborist-www20.pdf
- Jiang et al., BoxTaxo full paper (WWW '23), https://doi.org/10.1145/3543507.3583310 (the IJCAI extended abstract is in this folder)
- Xu et al., A taxonomy of blockchain-based systems for architecture design (ICSA '17), https://doi.org/10.1109/ICSA.2017.33
- Oliveira et al., To token or not to token (ICIS '18), https://aisel.aisnet.org/icis2018/crypto/Presentations/5/
- Chen et al., Detecting Ponzi schemes on Ethereum (WWW '18), https://doi.org/10.1145/3178876.3186046
- Di Angelo and Salzer, Tokens, types, and standards (DAPPS '20), https://doi.org/10.1109/DAPPS49028.2020.00001
- Freni et al., Tokenomics and blockchain tokens (Blockchain: Research and Applications, 2022), https://doi.org/10.1016/j.bcra.2022.100069
- Schär, Decentralized finance (FRB St. Louis Review, 2021), https://doi.org/10.20955/r.103.153-74
- Zetzsche et al., MiCA and the EU digital finance strategy (Capital Markets Law Journal, 2021), https://doi.org/10.1093/cmlj/kmaa025

## Using the BibTeX
`candidates.bib` entries fetched from arXiv are `@misc` with a `booktitle` added
by hand for the published venue; change the entry type to `@inproceedings` or
`@article` when you import one into `paper/references.bib`, and drop the
`eprint`, `primaryClass` and `note` fields. ACL Anthology entries are
camera-ready as fetched.
