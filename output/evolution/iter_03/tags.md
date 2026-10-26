# Part 2, Task C: tagging the DLT-Corpus sample

8646 items (paper: 3744, patent: 4902), 35576 tags (4.11 per item), 555 off-topic, 34302/35576 evidence spans verified, 157 tags rejected, 390 novel proposals. 101/107 term types used. Cost $4.415 ($0.00051 per item).

## Items tagged per category

- asset: 3494
- technology: 7422
- actor: 576
- activity: 401
- obligation_or_risk: 124

## Most frequent (term type, value) tags

| term type | value | items |
|---|---|---|
| Ledger purpose | data integrity and provenance | 2870 |
| Ledger purpose | value transfer | 1919 |
| Recording and cryptographic linkage | recorded on cryptographically secured distributed ledger | 1894 |
| DLT data structure (blockchain vs non-chain DLT) | blockchain (chain of blocks) | 1886 |
| Ledger purpose | identity and access control | 1131 |
| Smart contract / distributed ledger application scope | smart contract (self-executing) | 917 |
| Economic function of the asset | payment or investment purpose | 836 |
| Ledger purpose | blockchain used for record-keeping of non-asset data | 832 |
| Identity layer and onboarding | KYC/AML identity layer | 749 |
| Ledger purpose | supply chain traceability and product provenance | 735 |
| Network topology and node roles | decentralised | 707 |
| Ledger access and permissioning | permissioned private | 680 |
| Ledger access and permissioning | public / permissionless | 671 |
| Ledger purpose | consent or governance | 669 |
| Identity binding mechanism | cryptographic key pairs only | 644 |
| Ledger access and permissioning | permissioned public | 599 |
| Consensus mechanism | proof of work (PoW) | 590 |
| Ledger storage model (what is stored on chain) | transactions stored | 544 |
| Consensus mechanism | Byzantine fault tolerant (BFT) | 521 |
| Smart contract / distributed ledger application scope | distributed ledger application (smart contract) | 514 |
| Node / DLT network node role | validator | 424 |
| Privacy and anonymity features | built-in privacy | 411 |
| Crypto-asset definitional criteria | DLT-recorded digital representation of value or right | 392 |
| Smart contract usage domain | IoT and smart cities | 388 |
| Network topology and node roles | hierarchical / consortium | 359 |
| Fungibility | unique / non-fungible | 347 |
| Privacy mechanism family | encryption (symmetric or public-key) | 345 |
| Governance model of a DLT system | decentralised governance system | 303 |
| Smart contract / script language expressiveness | Turing complete | 303 |
| Economic function of the asset | good, collectible or non-commodity asset | 288 |
| Centralisation of control | decentralised | 280 |
| Crypto-asset definitional criteria | payment or investment capable virtual asset | 276 |
| Ledger purpose | electronic health and medical record management | 263 |
| Validator reward mechanism | lump-sum reward | 230 |
| Node / DLT network node role | tracking node (non-validating) | 215 |
| Native asset versus token standard | other token template (e.g. ERC-721, ERC-1400) | 207 |
| Identity binding mechanism | trusted third-party attestation | 207 |
| Smart contract usage domain | supply chain and retail | 204 |
| Centralisation of control | centralised | 202 |
| Smart contract usage domain | electronic health records and medical data sharing | 193 |

## Term types never used (6)

- Offshore VASP status (activity-based or location-based) `offshore_vasp_status` (actor)
- Yield or interest on stablecoin `stablecoin_interest_restriction` (obligation_or_risk)
- Prudential classification group (Basel) `prudential_classification_group` (obligation_or_risk)
- Traditional finance analogue `tradfi_analogue` (obligation_or_risk)
- Data classification (traffic, content, subscriber) `traffic_and_subscriber_data_class` (technology)
- Related person and affiliated person status `related_person_affiliation` (actor)

## Examples

**Resolving the Multiple Withdrawal Attack on ERC20 Tokens** (paper)
- Native asset versus token standard = ERC-20 fungible token (0.90) — "the ERC20 standard is a widely used token interface and is interoperable with ma"
- Smart contract / distributed ledger application scope = distributed ledger application (smart contract) (0.60) — "Custom tokens are an integral component of decentralized applications (dapps) de"
- Fungibility = fungible (0.60) — "a way for token holders to give permission for other users and dapps to withdraw"
- Economic function of the asset = payment or investment purpose (0.30) — "a way for token holders to give permission for other users and dapps to withdraw"

**DEFYN - A DEFI PORTFOLIO MANAGER** (paper)
- Ledger purpose = value transfer (0.60) — "DeFi helps us to control and visibility over your money."
- Governance model of a DLT system = decentralised governance system (0.50) — "There is no single entity that has control over, or can alter, that ledger of tr"
- Ledger access and permissioning = public / permissionless (0.50) — "DeFi products open up financial services to anyone which requires internet conne"
- Recording and cryptographic linkage = recorded on cryptographically secured distributed ledger (0.50) — "DeFi is connected with blockchain, which is decentralized, immutable"
- Crypto-asset service type = transfer services (0.40) — "Decentralized Finance (DeFi) for transferring and managing crypto assets"
- Centralisation of control = decentralised (0.40) — "they're largely owned and maintained by their users all over the world."

**The Broad Impact of Feature Imitation: Neural Enhancements Across Financial, Speech, and P** (paper)

**Circularity for Electric and Electronic Equipment (EEE), the Edge and Distributed Ledger (** (paper)
- Ledger purpose = data integrity and provenance (0.80) — "data controlled by their authoritative source at the edge, and (3) independent a"
- Ledger purpose = supply chain traceability and product provenance (0.70) — "Edge and Distributed Ledger (Edge&DL) model"
- Identity binding mechanism = device / machine identity (0.50) — "Serialize product identifiers"
- Ledger purpose = blockchain used for record-keeping of non-asset data (0.30) — "building new circularity systems for electronic and electric products"

**Structural Attacks on Local Routing in Payment Channel Networks** (paper)
- Network topology and node roles = decentralised (0.45) — "compromised intermediate nodes can delay or drop transactions to create denial-o"
- Ledger purpose = value transfer (0.40) — "routing a payment via multiple channels in a PCN requires locking collateral for"
- Ledger partitioning or layering topology = single chain (0.35) — "Payment channel networks (PCN) enable scalable blockchain transactions without f"
- Node / DLT network node role = tracking node (non-validating) (0.35) — "compromised intermediate nodes can delay or drop transactions"
- Network topology and node roles = centralised (0.30) — "We also show that the attacks are ineffective in less centralized networks"

**Illegal Roads Leading to Legal Ends: Bitcoin Mining in Malaysia** (paper)
