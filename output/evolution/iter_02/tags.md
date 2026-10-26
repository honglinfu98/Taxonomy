# Part 2, Task C: tagging the DLT-Corpus sample

8646 items (paper: 3744, patent: 4902), 35099 tags (4.06 per item), 596 off-topic, 33962/35099 evidence spans verified, 151 tags rejected, 408 novel proposals. 91/99 term types used. Cost $4.2509 ($0.00049 per item).

## Items tagged per category

- asset: 3886
- technology: 7323
- actor: 656
- activity: 370
- obligation_or_risk: 136

## Most frequent (term type, value) tags

| term type | value | items |
|---|---|---|
| DLT data structure (blockchain vs non-chain DLT) | blockchain (chain of blocks) | 2320 |
| Recording and cryptographic linkage | recorded on cryptographically secured distributed ledger | 2253 |
| Ledger purpose | data integrity and provenance | 2177 |
| Ledger purpose | blockchain used for record-keeping of non-asset data | 1822 |
| Ledger purpose | value transfer | 1495 |
| Smart contract / distributed ledger application scope | smart contract (self-executing) | 980 |
| Ledger purpose | identity and access control | 971 |
| Ledger access and permissioning | public / permissionless | 859 |
| Economic function of the asset | payment or investment purpose | 853 |
| Ledger access and permissioning | permissioned private | 849 |
| Identity layer and onboarding | KYC/AML identity layer | 711 |
| Ledger access and permissioning | permissioned public | 707 |
| Network topology and node roles | decentralised | 654 |
| Ledger storage model (what is stored on chain) | transactions stored | 633 |
| Smart contract / distributed ledger application scope | distributed ledger application (smart contract) | 618 |
| Consensus mechanism | proof of work (PoW) | 570 |
| Consensus mechanism | Byzantine fault tolerant (BFT) | 567 |
| Crypto-asset definitional criteria | DLT-recorded digital representation of value or right | 497 |
| Privacy and anonymity features | built-in privacy | 482 |
| Ledger purpose | consent or governance | 468 |
| Identity binding mechanism | cryptographic key pairs only | 446 |
| Network topology and node roles | hierarchical / consortium | 427 |
| Privacy mechanism family | encryption (symmetric or public-key) | 412 |
| Fungibility | unique / non-fungible | 374 |
| Smart contract usage domain | IoT and smart cities | 367 |
| Node / DLT network node role | validator | 359 |
| Economic function of the asset | good, collectible or non-commodity asset | 318 |
| Crypto-asset definitional criteria | payment or investment capable virtual asset | 310 |
| Smart contract / script language expressiveness | Turing complete | 309 |
| Centralisation of control | decentralised | 305 |
| Governance model of a DLT system | decentralised governance system | 298 |
| Smart contract usage domain | supply chain and retail | 280 |
| Smart contract usage domain | energy and utilities | 280 |
| Centralisation of control | centralised | 262 |
| Native asset versus token standard | other token template (e.g. ERC-721, ERC-1400) | 260 |
| Node / DLT network node role | tracking node (non-validating) | 237 |
| Validator reward mechanism | lump-sum reward | 211 |
| Hosted versus unhosted (self-hosted) wallet | non-custodial (unhosted/self-hosted) wallet | 211 |
| Tokenisation form | tokenised traditional asset | 209 |
| Smart contract usage domain | healthcare | 189 |

## Term types never used (8)

- Offshore VASP status (activity-based or location-based) `offshore_vasp_status` (actor)
- Yield or interest on stablecoin `stablecoin_interest_restriction` (obligation_or_risk)
- ICT and operational resilience risk `operational_resilience_risk` (obligation_or_risk)
- Prudential classification group (Basel) `prudential_classification_group` (obligation_or_risk)
- Traditional finance analogue `tradfi_analogue` (obligation_or_risk)
- MiFID financial instrument status `financial_instrument_status` (obligation_or_risk)
- Excluded instrument category (EU scope exclusions) `excluded_instrument_category` (obligation_or_risk)
- Related person and affiliated person status `related_person_affiliation` (actor)

## Examples

**An Architecture of IoT-Based Product Tracking with Blockchain in Multi-sided B2B Platform** (paper)
- Ledger purpose = data integrity and provenance (0.70) — "IoT-based traceability system can enable partners to track products and monitor "
- Ledger purpose = consent or governance (0.30) — "Partners can principally trust each other and can avoid fraudulent malpractices"
- Ledger scope: open or closed access by design = limited network of service providers (0.30) — "Multi-sided B2B platform with partners in a closed group of business participant"
- Node / DLT network node role = validator (0.20) — "IoT data transition from company-owned databases to Blockchain network"

**An Intelligent Scheduling Access Privacy Protection Model of Electric Vehicle Based on 5G-** (paper)
- Consensus mechanism = proof of work (PoW) (0.00) — ""

**The Impact of PMD on Single-Polarization Nonlinear Frequency Division Multiplexing** (paper)

**Blockchains: Improve the Scalability and Efficiency of Conventional Blockchain by Providin** (paper)
- Consensus mechanism = Byzantine fault tolerant (BFT) (0.80) — "using practical Byzantine fault tolerance and decentralized public key algorithm"
- DLT data structure (blockchain vs non-chain DLT) = blockchain (chain of blocks) (0.50) — "scalable blockchain (BC) mechanism is a necessity to integrate the scalable ledg"
- Network topology and node roles = decentralised (0.35) — "decentralized public key algorithms"
- Ledger purpose = data integrity and provenance (0.35) — "To provide security and privacy a scalable blockchain (BC) mechanism is a necess"
- Finality of agreement = deterministic (0.30) — "practical Byzantine fault tolerance"

**Generic Selfish Mining MDP for DAG Protocols** (paper)
- Consensus mechanism = proof of work (PoW) (0.90) — "Selfish Mining is strategic rule-breaking to maximize rewards in proof-of-work p"
- DLT data structure (blockchain vs non-chain DLT) = non-blockchain DLT (e.g. DAG, Hashgraph) (0.80) — "Protocols increasingly adopt non-sequential chain structures [11], for which MDP"
- DLT data structure (blockchain vs non-chain DLT) = DAG-based (IOTA) (0.50) — "Our approach is modular: we specify each protocol as one program, and then deriv"
- Validator reward mechanism = lump-sum reward (0.50) — "Selfish Mining is strategic rule-breaking to maximize rewards in proof-of-work p"
- Native asset presence and type = own single cryptocurrency (0.30) — "Selfish Mining is strategic rule-breaking to maximize rewards in proof-of-work p"

**Local Bitcoin Network Simulator for Performance Evaluation using Lightweight Virtualizatio** (paper)
- Consensus mechanism = proof of work (PoW) (0.85) — "the simulator can adjust the bitcoin mining difficulty level to below the defaul"
- Node / DLT network node role = miner (0.60) — "study the impact of the computation power and network delay on the network's con"
- DLT data structure (blockchain vs non-chain DLT) = blockchain (chain of blocks) (0.60) — "the block time as well as fork occurrences are evaluated"
- Finality of agreement = non-deterministic (probabilistic) (0.55) — "study the impact of the computation power and network delay on the network's con"
- Source code openness = open source (0.55) — "we have made the simulator available on Github for the community to use and impr"
- Ledger purpose = value transfer (0.50) — "This paper presents a new blockchain network simulator that uses bitcoin's origi"
