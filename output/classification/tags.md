# Part 2, Task C: tagging the DLT-Corpus sample

300 items (paper: 150, patent: 150), 1065 tags (3.55 per item), 20 off-topic, 1026/1065 evidence spans verified, 2 tags rejected, 13 novel proposals. 64/93 term types used. Cost $0.1413 ($0.00047 per item).

## Items tagged per category

- asset: 169
- technology: 242
- actor: 27
- activity: 21
- obligation_or_risk: 6

## Most frequent (term type, value) tags

| term type | value | items |
|---|---|---|
| DLT data structure (blockchain vs non-chain DLT) | blockchain (chain of blocks) | 122 |
| Recording and cryptographic linkage | recorded on cryptographically secured distributed ledger | 110 |
| Ledger access and permissioning | public / permissionless | 48 |
| Ledger storage model (what is stored on chain) | transactions stored | 38 |
| Ledger access and permissioning | permissioned public | 37 |
| Ledger access and permissioning | permissioned private | 37 |
| Economic function of the asset | payment or investment purpose | 30 |
| Consensus mechanism | proof of work (PoW) | 29 |
| Smart contract / distributed ledger application scope | smart contract (self-executing) | 27 |
| Identity layer and onboarding | KYC/AML identity layer | 24 |
| Network topology and node roles | decentralised | 24 |
| Smart contract / distributed ledger application scope | distributed ledger application (smart contract) | 21 |
| Network topology and node roles | hierarchical / consortium | 20 |
| Consensus mechanism | Byzantine fault tolerant (BFT) | 20 |
| Governance model of a DLT system | decentralised governance system | 18 |
| Smart contract / script language expressiveness | Turing complete | 16 |
| Node / DLT network node role | validator | 16 |
| Ledger scope: open or closed access by design | closed-loop system | 15 |
| Ledger scope: open or closed access by design | open network | 15 |
| Privacy and anonymity features | built-in privacy | 14 |
| Hosted versus unhosted (self-hosted) wallet | non-custodial (unhosted/self-hosted) wallet | 14 |
| Centralisation of control | decentralised | 13 |
| Centralisation of control | centralised | 13 |
| Crypto-asset definitional criteria | payment or investment capable virtual asset | 12 |
| Crypto-asset definitional criteria | DLT-recorded digital representation of value or right | 11 |
| Identity layer and onboarding | anonymous / pseudonymous | 10 |
| Native asset presence and type | own single cryptocurrency | 10 |
| Software architecture (monolithic vs polylithic) | polylithic | 10 |
| Governance model of a DLT system | technical / company-led | 10 |
| Node / DLT network node role | full node (complete replica) | 9 |
| Privacy and anonymity features | add-on privacy | 8 |
| Validator reward mechanism | lump-sum reward | 8 |
| Crypto-asset service type | transfer services | 8 |
| Interoperability and intraoperability | explicit interoperability | 7 |
| Centralisation of control | hybrid | 7 |
| Node / DLT network node role | tracking node (non-validating) | 7 |
| Economic function of the asset | good, collectible or non-commodity asset | 6 |
| Tokenisation form | tokenised traditional asset | 6 |
| Reference asset type | other crypto-assets or none (algorithmic) | 6 |
| Ledger storage model (what is stored on chain) | binary Merkle tree header | 6 |

## Term types never used (29)

- Yield distribution mechanism `yield_distribution_mechanism` (asset)
- Staking arrangement (self, delegated, custodial, liquid) `staking_arrangement` (activity)
- Pooled investment vehicle structure `fund_or_pooled_vehicle` (actor)
- Stablecoin issuer model `stablecoin_issuer_model` (actor)
- Offshore VASP status (activity-based or location-based) `offshore_vasp_status` (actor)
- Payment service and funds transfer `payment_or_transfer_service` (activity)
- Money transmission (acceptance and transmission of value) `regulated_transmission_of_value` (activity)
- Minting mechanism `minting_mechanism` (activity)
- Yield or interest on stablecoin `stablecoin_interest_restriction` (obligation_or_risk)
- Safeguarding and custody obligation `custody_safeguarding_obligation` (obligation_or_risk)
- Freezing and blocking capability `sanctions_and_freezing_capability` (obligation_or_risk)
- ICT and operational resilience risk `operational_resilience_risk` (obligation_or_risk)
- Settlement finality and legal enforceability `settlement_finality_legal_test` (obligation_or_risk)
- Prudential classification group (Basel) `prudential_classification_group` (obligation_or_risk)
- Traditional finance analogue `tradfi_analogue` (obligation_or_risk)
- Investment contract (Howey) criteria `investment_contract_howey` (obligation_or_risk)
- Security status of digital asset (US exclusions) `securities_status_digital_asset` (obligation_or_risk)
- MiFID financial instrument status `financial_instrument_status` (obligation_or_risk)
- Excluded instrument category (EU scope exclusions) `excluded_instrument_category` (obligation_or_risk)
- Virtual assets as property or proceeds of crime `virtual_asset_property_status` (obligation_or_risk)
- Serious crime threshold for predicate offences `serious_crime_threshold` (obligation_or_risk)
- Data classification (traffic, content, subscriber) `traffic_and_subscriber_data_class` (technology)
- Originator and beneficiary role `party_role_transfer` (actor)
- Related person and affiliated person status `related_person_affiliation` (actor)
- Ancillary asset and network token status `ancillary_asset_status` (asset)
- Exemption from MSB status `regulated_status_cvc_mst_exemption` (obligation_or_risk)
- Financial institution status for AML `regulatory_perimeter_fi_status` (actor)
- Tax reporting obligation status (CARF) `tax_reporting_status` (obligation_or_risk)
- Permitted control over client assets (unilateral vs multi-party control) `unhosted_custody_control_policy` (actor)

## Examples

**The palgrave handbook of FinTech and blockchain** (paper)
- Recording and cryptographic linkage = recorded on cryptographically secured distributed ledger (0.50) — "Chapter 4 argues that blockchain technology revolutionizes the financial landsca"
- Consensus mechanism = proof of work (PoW) (0.00) — ""

**A Hierarchical Multi Blockchain for Fine Grained Access to Medical Data** (paper)
- Ledger access and permissioning = permissioned public (0.70) — "a proxy blockchain enables independently managed trust authorities to interopera"
- Network topology and node roles = hierarchical / consortium (0.60) — "hierarchical multi expressive blockchain architecture"
- Governance model of a DLT system = alliance / consortium (0.50) — "independently managed trust authorities to interoperate"
- Smart contract / script language expressiveness = Turing complete (0.40) — "Smart contracts are used to enforce decentralized policies"
- Ledger scope: open or closed access by design = closed-loop system (0.40) — "domain blockchains allow each domain (e.g. a hospital or device manufacturer) to"
- Identity layer and onboarding = KYC/AML identity layer (0.30) — "allow fine-grained access control with attribute-based encryption"

**Fostering Equality in Education: The Blockchain Business Model for Higher Education (BBM-H** (paper)
- Tokenisation form = native or unbacked tokenised asset (0.30) — "sustainability tokens"
- Economic function of the asset = utility token (0.30) — "sustainability tokens"

**Blockchain-Empowered Lifecycle Management for AI-Generated Content Products in Edge Networ** (paper)
- Fungibility = unique / non-fungible (0.70) — "as a kind of online non-fungible digital property"
- Recording and cryptographic linkage = recorded on cryptographically secured distributed ledger (0.60) — "blockchain-empowered framework to manage the lifecycle of edge AIGC products"
- Economic function of the asset = good, collectible or non-commodity asset (0.50) — "online non-fungible digital property, the free circulation of AIGC products"
- Identity layer and onboarding = anonymous / pseudonymous (0.40) — "exchanges among anonymous users"
- Ledger access and permissioning = public / permissionless (0.30) — "free circulation of AIGC products is hindered by the lack of trustworthiness in "
- Validator reward mechanism = lump-sum reward (0.30) — "we design an incentive mechanism to guarantee the legitimate and timely executio"

**Is Blockchain Hashing an Effective Method for Electronic Governance?** (paper)
- Ledger access and permissioning = permissioned public (0.50) — "permissioned blockchains"
- DLT data structure (blockchain vs non-chain DLT) = blockchain (chain of blocks) (0.50) — "Blockchain hashing - or the insertion of data in the blockchain"
- Recording and cryptographic linkage = recorded on cryptographically secured distributed ledger (0.40) — "ensuring both immutability and publicity"
- Economic function of the asset = payment or investment purpose (0.20) — "users can apply special scripts to add their data to blockchain transactions"

**Crypto Tokens and Token Systems** (paper)
- Crypto-asset definitional criteria = DLT-recorded digital representation of value or right (0.80) — "crypto tokens, cryptographically secured digital tokens connected to DLT systems"
- Recording and cryptographic linkage = recorded on cryptographically secured distributed ledger (0.75) — "allowing the digital representation of real-world objects on distributed ledger "
- Native asset versus token standard = native protocol asset (0.60) — "They can either be native to a blockchain (as in the case of cryptocurrencies) o"
- Economic function of the asset = payment or investment purpose (0.40) — "Crypto tokens, and especially Bitcoin and Ether tokens, have drawn the attention"
- DLT data structure (blockchain vs non-chain DLT) = blockchain (chain of blocks) (0.40) — "distributed ledger technologies (DLT) such as blockchain"
- Tokenisation form = tokenised traditional asset (0.40) — "the digital representation of real-world objects on distributed ledger technolog"
