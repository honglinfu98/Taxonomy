# Part 2, Task C: tagging the DLT-Corpus sample

1818 items (paper: 1472, patent: 346), 7330 tags (4.03 per item), 154 off-topic, 7057/7330 evidence spans verified, 45 tags rejected, 46 novel proposals. 105/128 term types used. Cost $1.0366 ($0.00057 per item).

## Items tagged per category

- asset: 752
- technology: 1451
- actor: 102
- activity: 63
- obligation_or_risk: 37

## Most frequent (term type, value) tags

| term type | value | items |
|---|---|---|
| Ledger purpose | data integrity and provenance | 585 |
| Ledger purpose | value transfer | 322 |
| DLT data structure (blockchain vs non-chain DLT) | blockchain (chain of blocks) | 297 |
| Recording and cryptographic linkage | recorded on cryptographically secured distributed ledger | 265 |
| Economic function of the asset | payment or investment purpose | 227 |
| Ledger purpose | identity and access control | 215 |
| Network topology and node roles | decentralised | 192 |
| Smart contract / distributed ledger application scope | smart contract (self-executing) | 188 |
| Ledger purpose | supply chain traceability and product provenance | 153 |
| Ledger purpose | consent or governance | 141 |
| Centralisation of control | decentralised | 136 |
| Ledger access and permissioning | permissioned public | 136 |
| Consensus mechanism | proof of work (PoW) | 134 |
| Consensus mechanism | Byzantine fault tolerant (BFT) | 130 |
| Ledger access and permissioning | public / permissionless | 127 |
| Smart contract usage domain | IoT and smart cities | 125 |
| Smart contract / distributed ledger application scope | distributed ledger application (smart contract) | 108 |
| Identity layer and onboarding | KYC/AML identity layer | 102 |
| Crypto-asset definitional criteria | payment or investment capable virtual asset | 101 |
| Ledger purpose | electronic health and medical record management | 99 |
| Ledger access and permissioning | permissioned private | 95 |
| Smart contract / script language expressiveness | Turing complete | 93 |
| Privacy and anonymity features | built-in privacy | 90 |
| Identity binding mechanism | cryptographic key pairs only | 88 |
| Governance model of a DLT system | decentralised governance system | 86 |
| Ledger storage model (what is stored on chain) | transactions stored | 80 |
| Smart contract usage domain | supply chain traceability and provenance | 69 |
| Privacy mechanism family | encryption (symmetric or public-key) | 68 |
| Network topology and node roles | hierarchical / consortium | 67 |
| Smart contract usage domain | electronic health records and medical data sharing | 67 |
| Ledger purpose | blockchain used for record-keeping of non-asset data | 65 |
| Validator reward mechanism | lump-sum reward | 60 |
| Native asset presence and type | own single cryptocurrency | 56 |
| Smart contract usage domain | energy trading and grid management | 50 |
| Crypto-asset definitional criteria | DLT-recorded digital representation of value or right | 50 |
| Ledger partitioning or layering topology | single chain | 50 |
| Reference asset type | other crypto-assets or none (algorithmic) | 45 |
| Software architecture (monolithic vs polylithic) | polylithic | 44 |
| Centralisation of control | hybrid | 40 |
| Centralisation of control | centralised | 40 |

## Term types never used (23)

- Yield distribution mechanism `yield_distribution_mechanism` (asset)
- Stablecoin issuer model `stablecoin_issuer_model` (actor)
- Offshore VASP status (activity-based or location-based) `offshore_vasp_status` (actor)
- Money transmission (acceptance and transmission of value) `regulated_transmission_of_value` (activity)
- Yield or interest on stablecoin `stablecoin_interest_restriction` (obligation_or_risk)
- Safeguarding and custody obligation `custody_safeguarding_obligation` (obligation_or_risk)
- Freezing and blocking capability `sanctions_and_freezing_capability` (obligation_or_risk)
- ICT and operational resilience risk `operational_resilience_risk` (obligation_or_risk)
- Prudential classification group (Basel) `prudential_classification_group` (obligation_or_risk)
- Traditional finance analogue `tradfi_analogue` (obligation_or_risk)
- Investment contract (Howey) criteria `investment_contract_howey` (obligation_or_risk)
- Security status of digital asset (US exclusions) `securities_status_digital_asset` (obligation_or_risk)
- MiFID financial instrument status `financial_instrument_status` (obligation_or_risk)
- Excluded instrument category (EU scope exclusions) `excluded_instrument_category` (obligation_or_risk)
- Data classification (traffic, content, subscriber) `traffic_and_subscriber_data_class` (technology)
- Address linkage to service provider `self_hosted_address_status` (actor)
- Originator and beneficiary role `party_role_transfer` (actor)
- Related person and affiliated person status `related_person_affiliation` (actor)
- Exemption from MSB status `regulated_status_cvc_mst_exemption` (obligation_or_risk)
- Financial institution status for AML `regulatory_perimeter_fi_status` (actor)
- Tax reporting obligation status (CARF) `tax_reporting_status` (obligation_or_risk)
- Cross-chain transfer mechanism `cross_chain_transfer_mechanism` (asset)
- Settlement counterparty `settlement_counterparty` (actor)

## Examples

**Security Analysis of DeFi: Vulnerabilities, Attacks and Advances** (paper)
- Smart contract usage domain = intellectual property and media (0.00) — "Decentralized finance (DeFi) in Ethereum is a financial ecosystem built on the b"

**Augmented YARA Rules Fused With Fuzzy Hashing in Ransomware Triaging** (paper)

**Blockchain-Based Traceability for Anti-Counterfeit in Cross-Border E-Commerce Transactions** (paper)
- Ledger purpose = supply chain traceability and product provenance (0.70) — "traceability system that can help overcome information uncertainty and asymmetry"
- Ledger purpose = data integrity and provenance (0.60) — "Blockchain-Based Traceability for Anti-Counterfeit in Cross-Border E-Commerce Tr"

**6G Wireless Communication Systems: Applications, Requirements, Technologies, Challenges, a** (paper)
- Recording and cryptographic linkage = recorded on cryptographically secured distributed ledger (0.45) — "blockchain, three-dimensional networking, quantum communications"
- Ledger purpose = value transfer (0.10) — "blockchain"

**A new product anti‐counterfeiting blockchain using a truly decentralized dynamic consensus** (paper)
- Validator selection mechanism = random or verifiable-random selection (0.70) — "randomly employs a different set of different size of validators each time a new"
- Centralisation of control = decentralised (0.60) — "a truly decentralized consensus protocol"
- Ledger purpose = data integrity and provenance (0.60) — "a decentralized anti‐counterfeiting supply chain that exploits NFC and blockchai"
- Ledger purpose = supply chain traceability and product provenance (0.50) — "a decentralized anti‐counterfeiting supply chain that exploits NFC and blockchai"
- Validator selection mechanism = capability-score threshold plus random selection (0.40) — "This risk likelihood is used to determine the number of validators involved in t"
- Validator reward mechanism = lump-sum reward (0.40) — "the game model enforces the honest consensus nodes' behavior by rewarding honest"

**Blockchain in Industries: A Survey** (paper)
