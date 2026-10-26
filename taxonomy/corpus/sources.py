"""Source specifications: which part of each PDF goes into the corpus.

This is the single place that says what is extracted. Edit it to add a source
or move a boundary, then rerun `python -m taxonomy.build_corpus`.

Two kinds of range spec, used by pdf_text.select():
  (start_line, end_line, label)   1-indexed inclusive lines of plain `pdftotext`
                                  output (split on '\\n' only; form feeds are
                                  stripped so page breaks do not shift numbering)
  (start_regex, end_regex, label) first line matching start_regex up to (excluding)
                                  the next line matching end_regex. Used with
                                  `-layout` for the US bills, whose two-column
                                  line-number typesetting scrambles plain output.
Mixed int/regex pairs are allowed.
"""
from __future__ import annotations

Range = tuple[int | str, int | str, str]

END = r"(?!x)x"  # regex that never matches -> run to end of file

# Legal instruments in legal/: (pdf stem, display title, layout_mode, [ranges])
# Display title is 'JURISDICTION | instrument name'.
SOURCES: list[tuple[str, str, bool, list[Range]]] = [
    ("EU_2023_MiCA Regulation 2023-1114", "EU | Regulation (EU) 2023/1114 Markets in Crypto-Assets (MiCA)", False,
     [(1609, 1898, "Articles 2-3: Scope and Definitions")]),
    ("EU_2024_AML Regulation 2024-1624", "EU | Regulation (EU) 2024/1624 Anti-Money Laundering Regulation (AMLR)", False,
     [(2391, 2795, "Article 2: Definitions")]),
    ("EU_2023_Transfer of Funds Regulation 2023-1113 (travel rule)", "EU | Regulation (EU) 2023/1113 Transfer of Funds (travel rule)", False,
     [(894, 1026, "Article 3: Definitions")]),
    ("EU_2022_DORA Regulation 2022-2554", "EU | Regulation (EU) 2022/2554 Digital Operational Resilience (DORA)", False,
     [(1610, 1839, "Article 3: Definitions")]),
    ("UK_2026_FSMA 2000 (Cryptoassets) Regulations (SI 2026-102)", "UK | FSMA 2000 (Cryptoassets) Regulations 2026 (SI 2026/102)", False,
     [(310, 348, "Regulation 2: Interpretation"),
      (1274, 1768, "Regulation 40: Amendment of the Regulated Activities Order (new cryptoasset specified activities, arts 9M-9Z, 88F-88G)")]),
    ("UK_2025_Reporting Cryptoasset Service Providers Regulations (SI 2025-744)", "UK | Reporting Cryptoasset Service Providers Regulations 2025 (SI 2025/744, CARF)", False,
     [(37, 95, "Regulations 2-3: Interpretation; UK reporting cryptoasset service provider")]),
    ("US_2026_CLARITY Act HR3633 (Senate-reported)", "US | Digital Asset Market Clarity Act, H.R. 3633 (Senate-reported, 2026)", True,
     # The Senate-reported print reproduces the House-passed text (Title I of which is
     # already captured from the House file) followed by the Senate Banking Committee
     # amendment in the nature of a substitute; only the substitute is taken here.
     [(r"^\s*\d*\s*SEC\. 2\. DEFINITIONS\.", r"^\s*\d*\s*TITLE I—RESPONSIBLE",
       "Senate Banking Committee substitute, Sec. 2: Definitions (ancillary asset, digital asset, distributed ledger, etc.)"),
      (r"^\s*\d*\s*SEC\. 105\. CHARACTERISTICS OF NETWORK TOKENS", r"^\s*\d*\s*SEC\. 106\. ",
       "Senate Banking Committee substitute, Sec. 105: Characteristics of network tokens")]),
    ("US_2025_CLARITY Act HR3633 (House-passed)", "US | Digital Asset Market Clarity Act, H.R. 3633 (House-passed, 2025)", True,
     [(r"^\s*\d*\s*SEC\. 101\. DEFINITIONS", r"^\s*\d*\s*SEC\. 105\. ", "Title I, Secs. 101-104: Definitions")]),
    ("US_2024_FIT21 HR4763 (House-passed)", "US | Financial Innovation and Technology for the 21st Century Act (FIT21), H.R. 4763 (House-passed, 2024)", True,
     [(r"^\s*\d*\s*SEC\. 101\. DEFINITIONS", r"^\s*\d*\s*SEC\. 105\. ", "Title I, Secs. 101-104: Definitions")]),
    ("US_2025_GENIUS Act (PL 119-27)", "US | GENIUS Act, Pub. L. 119-27 (2025)", True,
     [(r"^\s*SEC\. 2\. DEFINITIONS\.", r"^\s*SEC\. 3\. ", "Sec. 2: Definitions")]),
    ("US_2025_Executive Order 14178 Digital Financial Technology", "US | Executive Order 14178 Strengthening American Leadership in Digital Financial Technology (2025)", False,
     [(54, 90, "Sec. 2: Definitions")]),
    ("US_2025_PWG Digital Asset Markets Report", "US | President's Working Group on Digital Asset Markets Report (2025)", False,
     [(1075, 2334, "Chapter II: The Digital Asset Ecosystem (market participants, DeFi architecture, consensus, infrastructure providers)")]),
    ("US_2019_FinCEN CVC Guidance", "US | FinCEN Guidance FIN-2019-G001, Application of FinCEN Regulations to Convertible Virtual Currencies (2019)", False,
     [(119, 175, "Sec. 1.2.1: Definitions"),
      (302, 316, "Sec. 1.3: Convertible Virtual Currency (CVC)"),
      (617, 1269, "Secs. 4-5: Common CVC business models (P2P exchangers, wallets, kiosks, DApps, anonymity-enhanced CVC, trading platforms, ICOs, mining pools)")]),
    ("INTL_2021_FATF Updated Guidance Virtual Assets VASPs", "INTL | FATF Updated Guidance for a Risk-Based Approach to Virtual Assets and VASPs (2021)", False,
     [(1181, 2103, "Part Two: What is a virtual asset? What is a VASP? Scope of the definitions (incl. stablecoins, P2P, DeFi, NFTs)"),
      (5698, 5845, "Annex A: Recommendation 15, Interpretive Note and FATF Definitions; Glossary")]),
    ("INTL_2025_FATF Targeted Update VA VASP (6th)", "INTL | FATF Targeted Update on Implementation of the FATF Standards on VAs and VASPs, 6th (2025)", False,
     [(1392, 1644, "Section Two: ML/TF/PF Risks (stablecoins, unhosted wallets, offshore VASPs, DeFi)")]),
    ("INTL_2026_FATF Targeted Update VA VASP (7th)", "INTL | FATF Targeted Update on Implementation of the FATF Standards on VAs and VASPs, 7th (2026)", False,
     [(1402, 1675, "Section Two: ML/TF/PF Risks (stablecoins, P2P/unhosted wallets, offshore VASPs, DeFi)")]),
    ("INTL_2022_Basel Prudential Treatment of Cryptoasset Exposures", "INTL | Basel Committee SCO60 Prudential Treatment of Cryptoasset Exposures (2022)", False,
     [(365, 785, "SCO60.6-60.22: Classification conditions (Group 1a/1b/2a/2b cryptoassets)"),
      (2433, 2475, "SCO60.131: Definitions")]),
    ("INTL_2023_FSB High-level Recommendations Crypto-asset Activities", "INTL | FSB High-level Recommendations for the Regulation of Crypto-asset Activities and Markets (2023)", False,
     [(587, 651, "Glossary")]),
    ("INTL_2023_IOSCO Policy Recommendations Crypto and Digital Asset Markets", "INTL | IOSCO Policy Recommendations for Crypto and Digital Asset Markets (2023)", False,
     [(1634, 1715, "Annex A: Glossary of Relevant Terms and Definitions")]),
    ("INTL_2024_UN Convention against Cybercrime (A-RES-79-243)", "INTL | UN Convention against Cybercrime, A/RES/79/243 (2024)", False,
     [(260, 333, "Article 2: Use of terms")]),
    ("INTL_2001_CoE Budapest Convention on Cybercrime", "INTL | Council of Europe Convention on Cybercrime (Budapest Convention, 2001)", False,
     [(85, 119, "Article 1: Definitions")]),
]

# Academic papers in context/: (pdf stem, metadata, [ranges])
PAPERS: list[tuple[str, dict[str, str], list[Range]]] = [
    ("Taxonomy of Blockchain Technologies Principles of Identification and Classification",
     {"type": "taxonomy_framework", "title": "Taxonomy of Blockchain Technologies. Principles of Identification and Classification",
      "authors": "Paolo Tasca; Claudio J. Tessone", "year": "2018", "venue": "arXiv:1708.04872v2",
      "focus": "component-level taxonomy of blockchain architectures (consensus, transactions, native assets, extensibility, security, codebase, identity, fees)"},
     [(1, r"^REFERENCES$", "Body: Sections I-XII (introduction through conclusion)"),
      (r"^Appendix A: Blockchains Analysed", END, "Appendix A: Blockchains analysed for the taxonomy")]),
    ("Crypto-asset Taxonomy for Investors and Regulators",
     {"type": "taxonomy_framework", "title": "Crypto-asset Taxonomy for Investors and Regulators",
      "authors": "Xiao Zhang; Juan Ignacio Ibanez; Jiahua Xu", "year": "2026", "venue": "arXiv:2602.05098v1",
      "focus": "asset-level taxonomy: technical standard, centralisation, asset function, minting/yield/redemption mechanisms, legal classification (MiCAR), TradFi analogues"},
     [(1, r"^Table 2: TradFi analogues", "Sections 1-5: motivation, related work, methodology, taxonomy dimensions, dataclass and decision rules, mapping results (summary)"),
      (r"^6 Case studies, TradFi analogues", r"^References$", "Sections 6-7: case studies, TradFi analogues and regulatory implications; conclusion")]),
    ("DLT-Corpus - A Large-Scale Text Collection for the Distributed Ledger Technology Domain",
     {"type": "domain_corpus_paper", "title": "DLT-Corpus: A Large-Scale Text Collection for the Distributed Ledger Technology Domain",
      "authors": "Walter Hernandez Cruz; Peter Devine; Nikhil Vadgama; Paolo Tasca; Jiahua Xu", "year": "2026", "venue": "KDD '26",
      "focus": "construction of a DLT-domain text corpus (scientific literature, patents, social media); domain vocabulary and sub-domain coverage"},
     [(1, r"^Acknowledgements$", "Body: all sections (introduction through limitations)")]),
]
