# Part 2 maintenance: the DAG as label space

300 tagged items placed on 80/93 nodes (1065 tags, 4630 closure placements).

## Objectives: content-driven vs Part 1 prior

| metric | from tags (empirical) | from is-a weights (Part 1) |
|---|---|---|
| bits per descent (information gain) | 6.9161 | 4.7155 |
| AUC of reach-a-leaf | 0.7943 | 0.8353 |
| expected depth | 3.373 | 2.8056 |
| effective leaves | 19.73 | 13.987 |
| effective leaves / nodes | 0.2122 | 0.1504 |

## Where descents stop (top stop mass)

- Recording and cryptographic linkage `digital_asset_recording`: 0.1448
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 0.1065
- Smart contract / distributed ledger application scope `smart_contract_definition_scope`: 0.0896
- Privacy and anonymity features `privacy_enhancement`: 0.0878
- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`: 0.0719
- Smart contract / script language expressiveness `script_language_expressiveness`: 0.0717
- Native asset versus token standard `native_vs_token_standard`: 0.0684
- Centralisation of control `centralisation_level`: 0.0399
- Identity layer and onboarding `digital_identity_layer`: 0.0395
- Node / DLT network node role `ledger_node_role`: 0.0379
- Interoperability and intraoperability `interoperability_type`: 0.0368
- Wallet storage mode (hot or cold) `wallet_type_storage`: 0.0249
- Nexus to jurisdiction (services offered in jurisdiction) `service_location_nexus`: 0.0234
- Ecosystem participant role `ecosystem_participant_role`: 0.0189
- Tokenisation form `tokenisation_form`: 0.015

## Node statistics (nodes with items, by closure size)

| node | cat | direct | closure | children | value entropy | dominance | branching gain | residual |
|---|---|---|---|---|---|---|---|---|
| Governance model of a DLT system | techn | 32 | 242 | 8 | 1.3663 | 0.562 | 2.6437 | 5 (0.021) |
| Ledger access and permissioning | techn | 118 | 237 | 14 | 1.6289 | 0.39 | 3.2748 | 9 (0.038) |
| Ledger scope: open or closed access by | techn | 33 | 228 | 5 | 1.3486 | 0.455 | 1.8519 | 5 (0.022) |
| Network topology and node roles | techn | 45 | 223 | 7 | 1.1257 | 0.533 | 2.2522 | 4 (0.018) |
| Consensus mechanism | techn | 51 | 219 | 6 | 1.2152 | 0.569 | 2.3907 | 14 (0.064) |
| Validator reward mechanism | techn | 9 | 205 | 4 | 0.5033 | 0.889 | 1.167 | 1 (0.005) |
| Transaction fee regime | techn | 5 | 204 | 2 | 0.971 | 0.6 | 0.1231 | 1 (0.005) |
| Native asset presence and type | techn | 11 | 203 | 4 | 0.4395 | 0.909 | 1.3157 | 1 (0.005) |
| Software architecture (monolithic vs p | techn | 13 | 201 | 5 | 0.7793 | 0.769 | 2.0168 | 3 (0.015) |
| Ledger storage model (what is stored o | techn | 46 | 198 | 3 | 1.0082 | 0.792 | 1.391 | 5 (0.025) |
| Crypto-asset definitional criteria | asset | 22 | 169 | 10 | 0.9986 | 0.522 | 2.3697 | 3 (0.018) |
| Economic function of the asset | asset | 39 | 166 | 9 | 1.2729 | 0.732 | 2.8315 | 9 (0.054) |
| DLT data structure (blockchain vs non- | techn | 124 | 162 | 3 | 0.3577 | 0.946 | 1.2694 | 98 (0.605) |
| Legal classification of crypto-asset | asset | 3 | 157 | 11 | -0.0 | 1.0 | 2.7822 | 1 (0.006) |
| Reference asset type | asset | 11 | 156 | 7 | 1.6172 | 0.545 | 2.388 | 4 (0.026) |
| Issuer identifiability | asset | 1 | 149 | 6 | -0.0 | 1.0 | 1.6919 | 0 (0.0) |
| Payment stablecoin / e-money / ART reg | asset | 1 | 149 | 3 | -0.0 | 1.0 | 0.936 | 0 (0.0) |
| Convertible virtual currency (CVC) sta | asset | 4 | 135 | 1 | -0.0 | 1.0 | 0.1537 | 3 (0.022) |
| Recording and cryptographic linkage | asset | 113 | 132 | 5 | 0.1768 | 0.973 | 1.7574 | 95 (0.72) |
| Node / DLT network node role | techn | 38 | 83 | 1 | 2.0797 | 0.4 | 0.9695 | 33 (0.398) |
| Decentralised system certification | techn | 10 | 65 | 2 | 1.361 | 0.5 | 1.234 | 8 (0.123) |
| Redemption mechanism | asset | 1 | 61 | 4 | -0.0 | 1.0 | 1.6673 | 1 (0.016) |
| Form of holder claim | asset | 3 | 60 | 4 | -0.0 | 1.0 | 1.5626 | 1 (0.017) |
| Source code openness | techn | 1 | 57 | 2 | -0.0 | 1.0 | 0.2975 | 0 (0.0) |
| Smart contract / distributed ledger ap | techn | 44 | 54 | 1 | 1.2314 | 0.54 | 0.9911 | 30 (0.556) |
| Source of yield | asset | 4 | 52 | 1 | -0.0 | 1.0 | 0.3912 | 4 (0.077) |
| Information and communications technol | techn | 1 | 50 | 3 | -0.0 | 1.0 | 1.5707 | 1 (0.02) |
| Identity layer and onboarding | techn | 34 | 49 | 2 | 0.874 | 0.706 | 1.2602 | 24 (0.49) |
| Yield distribution mechanism | asset | 0 | 48 | 1 | - | - | -0.0 | 0 (0.0) |
| Centralisation of control | asset | 32 | 48 | 2 | 1.5334 | 0.394 | 0.9685 | 29 (0.604) |
| Crypto-asset service provider or VASP  | actor | 7 | 27 | 16 | 0.5917 | 0.857 | 3.5334 | 3 (0.111) |
| Privacy and anonymity features | techn | 22 | 25 | 1 | 0.9457 | 0.636 | 0.5294 | 22 (0.88) |
| Data classification (traffic, content, | techn | 0 | 25 | 1 | - | - | -0.0 | 0 (0.0) |
| Smart contract / script language expre | techn | 19 | 24 | 1 | 0.7742 | 0.842 | 0.8709 | 17 (0.708) |
| Offshore VASP status (activity-based o | actor | 0 | 24 | 2 | - | - | 0.9986 | 0 (0.0) |
| Jurisdictional regime and home or host | actor | 3 | 24 | 5 | 0.9183 | 0.667 | 1.8282 | 2 (0.083) |
| Principal or agent role in transaction | actor | 2 | 22 | 8 | 1.0 | 0.5 | 2.1204 | 0 (0.0) |
| Custody model | actor | 4 | 22 | 6 | 1.0 | 0.5 | 2.3574 | 2 (0.091) |
| Financial institution status for AML | actor | 0 | 22 | 3 | - | - | 0.258 | 0 (0.0) |
| Crypto-asset service type | activ | 17 | 21 | 9 | 2.0169 | 0.444 | 2.8715 | 10 (0.476) |
| Trading venue type | actor | 6 | 20 | 1 | 1.3788 | 0.571 | 0.7219 | 4 (0.2) |
| Hosted versus unhosted (self-hosted) w | asset | 19 | 19 | 0 | 1.0215 | 0.737 | -0.0 | 19 (1.0) |
| Tokenisation form | asset | 9 | 17 | 2 | 0.9183 | 0.667 | 1.1942 | 6 (0.353) |
| Control or sufficient influence over D | actor | 1 | 16 | 3 | -0.0 | 1.0 | 1.0863 | 1 (0.062) |
| Fungibility | asset | 5 | 12 | 1 | -0.0 | 1.0 | 0.4138 | 1 (0.083) |
| Ecosystem participant role | actor | 9 | 12 | 4 | 1.9749 | 0.333 | 1.6226 | 9 (0.75) |
| Infrastructure provider type | actor | 1 | 12 | 2 | -0.0 | 1.0 | 0.3912 | 0 (0.0) |
| Native asset versus token standard | asset | 11 | 11 | 1 | 1.4834 | 0.417 | 0.4395 | 10 (0.909) |
| Transfer of crypto-assets (travel rule | activ | 6 | 11 | 8 | 0.9183 | 0.667 | 2.6817 | 3 (0.273) |
| Money transmission (acceptance and tra | activ | 0 | 8 | 5 | - | - | 1.8732 | 0 (0.0) |
| Public offer or private placement | activ | 1 | 8 | 3 | -0.0 | 1.0 | 1.2407 | 1 (0.125) |
| Finality of agreement | techn | 7 | 7 | 0 | 0.5917 | 0.857 | -0.0 | 7 (1.0) |
| Interoperability and intraoperability | techn | 7 | 7 | 0 | -0.0 | 1.0 | -0.0 | 7 (1.0) |
| Offer and issuance method (token distr | activ | 3 | 7 | 3 | 1.585 | 0.333 | 0.8631 | 2 (0.286) |
| Anti-money laundering obligations | oblig | 3 | 6 | 9 | 0.9183 | 0.667 | 1.9072 | 0 (0.0) |
| Virtual assets as property or proceeds | oblig | 0 | 6 | 7 | - | - | 2.006 | 0 (0.0) |
| Peer-to-peer (P2P) transaction | activ | 2 | 5 | 1 | 1.0 | 0.5 | 0.971 | 2 (0.4) |
| Freezing and blocking capability | oblig | 0 | 5 | 4 | - | - | 0.8631 | 0 (0.0) |
| Illicit finance risk category | oblig | 4 | 5 | 2 | 0.7219 | 0.8 | 0.971 | 3 (0.6) |
| Permitted control over client assets ( | actor | 0 | 4 | 2 | - | - | 0.8113 | 0 (0.0) |
| Wallet storage mode (hot or cold) | techn | 3 | 3 | 0 | -0.0 | 1.0 | -0.0 | 3 (1.0) |
| Stablecoin issuer model | actor | 0 | 3 | 1 | - | - | -0.0 | 0 (0.0) |
| Operator of crypto-asset arrangement | actor | 2 | 3 | 2 | -0.0 | 1.0 | 0.9183 | 2 (0.667) |
| Payment service and funds transfer | activ | 0 | 3 | 1 | - | - | -0.0 | 0 (0.0) |
| Address linkage to service provider | actor | 2 | 3 | 1 | -0.0 | 1.0 | 0.9183 | 2 (0.667) |
| Nexus to jurisdiction (services offere | activ | 3 | 3 | 0 | -0.0 | 1.0 | -0.0 | 3 (1.0) |
| Asset supply management (monetary poli | techn | 2 | 2 | 0 | 1.0 | 0.5 | -0.0 | 2 (1.0) |
| Anonymity-enhancing crypto-asset statu | oblig | 2 | 2 | 0 | -0.0 | 1.0 | -0.0 | 2 (1.0) |
| Wrapped / cross-chain representation | asset | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Redemption and reserve adequacy | oblig | 1 | 1 | 4 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Yield or interest on stablecoin | oblig | 0 | 1 | 2 | - | - | -0.0 | 0 (0.0) |
| Investment contract (Howey) criteria | oblig | 0 | 1 | 3 | - | - | -0.0 | 0 (0.0) |
| Security status of digital asset (US e | oblig | 0 | 1 | 2 | - | - | 1.0 | 0 (0.0) |
| MiFID financial instrument status | oblig | 0 | 1 | 2 | - | - | 1.0 | 0 (0.0) |
| Excluded instrument category (EU scope | oblig | 0 | 1 | 4 | - | - | 1.585 | 0 (0.0) |
| Central bank digital currency status | asset | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Originator and beneficiary role | actor | 0 | 1 | 1 | - | - | -0.0 | 0 (0.0) |
| Consumer or retail versus professional | actor | 1 | 1 | 1 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Reference currency for stablecoin peg  | asset | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Validator operation capacity (who may  | actor | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |

## Maintenance proposals

**Dormant nodes (13)**, no items in this batch: `staking_arrangement`, `fund_or_pooled_vehicle`, `minting_mechanism`, `custody_safeguarding_obligation`, `operational_resilience_risk`, `settlement_finality_legal_test`, `prudential_classification_group`, `tradfi_analogue`, `serious_crime_threshold`, `related_person_affiliation`, `ancillary_asset_status`, `regulated_status_cvc_mst_exemption`, `tax_reporting_status`

**Collapsed nodes (3)**, many items but one value absorbs them (merge or re-split candidates):
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 124 items, dominance 0.946 (blockchain (chain of blocks))
- Native asset presence and type `native_asset_type`: 11 items, dominance 0.909 (own single cryptocurrency)
- Recording and cryptographic linkage `digital_asset_recording`: 113 items, dominance 0.973 (recorded on cryptographically secured distributed ledger)

**Highest-gain nodes**:
- Crypto-asset service provider or VASP status `service_provider_status`: 3.5334 bits over 27 items
- Ledger access and permissioning `ledger_access_permission`: 3.2748 bits over 237 items
- Crypto-asset service type `crypto_asset_service_type`: 2.8715 bits over 21 items
- Economic function of the asset `crypto_asset_function`: 2.8315 bits over 166 items
- Legal classification of crypto-asset `legal_classification_status`: 2.7822 bits over 157 items
- Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`: 2.6817 bits over 11 items
- Governance model of a DLT system `governance_model`: 2.6437 bits over 242 items
- Consensus mechanism `consensus_mechanism`: 2.3907 bits over 219 items

**Discovery targets (15)**, residual >= threshold:
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 98 residual of 162 (0.605)
- Recording and cryptographic linkage `digital_asset_recording`: 95 residual of 132 (0.72)
- Node / DLT network node role `ledger_node_role`: 33 residual of 83 (0.398)
- Smart contract / distributed ledger application scope `smart_contract_definition_scope`: 30 residual of 54 (0.556)
- Centralisation of control `centralisation_level`: 29 residual of 48 (0.604)
- Identity layer and onboarding `digital_identity_layer`: 24 residual of 49 (0.49)
- Privacy and anonymity features `privacy_enhancement`: 22 residual of 25 (0.88)
- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`: 19 residual of 19 (1.0)
- Smart contract / script language expressiveness `script_language_expressiveness`: 17 residual of 24 (0.708)
- Native asset versus token standard `native_vs_token_standard`: 10 residual of 11 (0.909)
- Crypto-asset service type `crypto_asset_service_type`: 10 residual of 21 (0.476)
- Ecosystem participant role `ecosystem_participant_role`: 9 residual of 12 (0.75)
- Finality of agreement `consensus_finality`: 7 residual of 7 (1.0)
- Interoperability and intraoperability `interoperability_type`: 7 residual of 7 (1.0)
- Tokenisation form `tokenisation_form`: 6 residual of 17 (0.353)

## Discovery (Task E) candidates

- [ACCEPTED] at `privacy_enhancement`: new child_term_type **Privacy mechanism family** — The primary cryptographic or structural mechanism used to conceal data, identities, or transaction details. (supports 8 items, gain 0.8322 bits, evidence verified); values: encryption (symmetric or public-key), homomorphic encryption, zero-knowledge proofs, data slicing or secret sharing, private channels or data collections, commitments and hashing
- [ACCEPTED] at `script_language_expressiveness`: new child_term_type **smart_contract_deployment_context** — Classifies the application domain or deployment setting in which the smart contract logic operates. (supports 6 items, gain 0.6635 bits, evidence verified); values: supply chain / logistics, certification / credentials, decentralized finance, healthcare data sharing, IoT / device identity, general-purpose / unspecified
- [ACCEPTED] at `smart_contract_definition_scope`: new child_term_type **smart_contract_usage_domain** — Splits residual texts by the sector or function the contract or application targets, such as energy, healthcare, copyright, identity, or advertising. (supports 8 items, gain 0.4648 bits, evidence verified); values: energy and utilities, healthcare, intellectual property and media, identity and authentication, supply chain and retail, IoT and smart cities
- [ACCEPTED] at `digital_identity_layer`: new child_term_type **identity_binding_mechanism** — The mechanism linking a real-world or device identity to ledger addresses, keys, or identifiers. (supports 5 items, gain 0.3407 bits, evidence verified); values: decentralised identifiers (DID), trusted third-party attestation, biometric authentication, cryptographic key pairs only, device or hardware identity
- [ACCEPTED] at `digital_identity_layer`: new value **device / machine identity** — Ledger identity is assigned to devices, things or digital twins rather than to human participants. (supports 5 items, gain 0.3407 bits, evidence verified)
- [ACCEPTED] at `digital_asset_recording`: new child_term_type **ledger purpose** — Classifies whether the ledger records transferable value, data integrity or provenance, governance or consent, or identity and access. (supports 6 items, gain 0.2083 bits, evidence verified); values: value transfer, data integrity and provenance, consent or governance, identity and access control
- [ACCEPTED] at `digital_asset_recording`: new value **blockchain used for record-keeping of non-asset data** — Distributed ledger used to store records, logs, certificates or events rather than a transferable asset or token. (supports 5 items, gain 0.1823 bits, evidence verified)
- [ACCEPTED] at `dlt_architecture`: new child_term_type **ledger partitioning or layering topology** — Describes how the ledger is divided across chains, layers, shards or partitions regardless of the underlying block or graph structure. (supports 5 items, gain 0.1759 bits, evidence verified); values: single chain, multiple parallel chains, layered main and sub-chains, partitioned ledger, two-dimensional chains
- [rejected] at `consensus_finality`: new value **transient (eventually consistent) disagreement** — Protocol allows temporary divergence among participants on the block for an index, resolved later into a single agreed block. (supports 3 items, gain 0.9852 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **oracle-mediated interoperability** — The ledger exchanges information with external systems or other chains through a trusted oracle or relay acting as an intermediary. (supports 3 items, gain 0.9852 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **cross-chain atomic swap** — Assets move between blockchains via trustless atomic exchange protocols without a centralised intermediary. (supports 3 items, gain 0.9852 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **multi-ledger or sidechain linking** — The ledger is split or extended into multiple linked ledgers or sidechains that interoperate with each other. (supports 3 items, gain 0.9852 bits, evidence verified)
- [rejected] at `native_vs_token_standard`: new value **multi-standard token (ERC-1155)** — Token issued under a smart-contract standard that combines fungible and non-fungible assets in one contract. (supports 3 items, gain 0.8012 bits, evidence verified)
- [rejected] at `unhosted_vs_hosted_wallet`: new value **multi-party or shared-control wallet** — Wallet whose keys or signing authority are split or shared among several parties or nodes, so no single party fully controls access. (supports 3 items, gain 0.6292 bits, evidence unverified)
- [rejected] at `unhosted_vs_hosted_wallet`: new value **identity-linked or credential-gated access** — Access to the crypto-asset is gated by user authentication or identity credentials tied to an external account rather than by possession of keys alone. (supports 3 items, gain 0.6292 bits, evidence verified)
- [rejected] at `privacy_enhancement`: new value **Selective disclosure or permissioned visibility** — Privacy achieved by controlling which parties or users can view particular data, rather than by global obfuscation. (supports 4 items, gain 0.602 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **end user / consumer / prosumer** — Participant who consumes or trades a resource on a ledger-based platform without issuing, validating, or developing the underlying infrastructure. (supports 3 items, gain 0.5165 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **organization adopter / enterprise user** — Organisation that adopts or deploys blockchain technology for its own operations rather than as a crypto-asset issuer or validator. (supports 3 items, gain 0.5165 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **criminal actor / attacker** — Participant who misuses, steals from, or launders through crypto-assets or ledgers, such as fraudsters or thieves. (supports 2 items, gain 0.4299 bits, evidence verified)
- [rejected] at `centralisation_level`: new value **partially decentralised (permissioned consortium)** — Control of critical resources is shared among a bounded set of known organisations rather than one entity or open participation. (supports 4 items, gain 0.3497 bits, evidence verified)
- [rejected] at `tokenisation_form`: new value **tokenised electronic document of title** — A token representing title or possession rights over an electronic document, such as a bill of lading or warehouse receipt, held on a ledger. (supports 3 items, gain 0.3333 bits, evidence verified)
- [rejected] at `tokenisation_form`: new value **tokenised intellectual property or copyright** — A token representing rights in a copyrighted work, licence, or other intellectual property managed on a ledger. (supports 2 items, gain 0.3061 bits, evidence verified)
- [rejected] at `smart_contract_definition_scope`: new value **smart contract security analysis tool** — Software that analyses, audits, or detects vulnerabilities in smart contract code rather than being a contract itself. (supports 3 items, gain 0.2606 bits, evidence verified)
- [rejected] at `ledger_node_role`: new value **storage / archival node** — A node dedicated to storing historical or block data separate from consensus participation. (supports 4 items, gain 0.2119 bits, evidence unverified)
- [rejected] at `ledger_node_role`: new child_term_type **node participation level** — Distinguishes nodes by whether they participate in consensus or only hold, store, or relay ledger data. (supports 4 items, gain 0.2119 bits, evidence verified); values: consensus participant, storage-only, relay-only, observer
- [rejected] at `ledger_node_role`: new value **orderer / ordering service node** — A node that sequences transactions into blocks without necessarily validating or replicating full state, as in permissioned consortium designs. (supports 3 items, gain 0.1747 bits, evidence unverified)
- [rejected] at `ledger_node_role`: new value **acceleration / relay node** — A node that forwards or accelerates transaction propagation between blockchains or peers without storing or validating the ledger. (supports 3 items, gain 0.1747 bits, evidence verified)
- [rejected] at `crypto_asset_service_type`: new value **decentralised exchange (DEX) operation** — Operating or using a non-custodial, smart-contract-based exchange where users trade crypto-assets peer-to-pool or via order books without a central intermediary. (supports 3 items, gain 0.1602 bits, evidence verified)
- [rejected] at `crypto_asset_service_type`: new value **supply chain tracking and provenance** — Providing blockchain-based recording, tracking or authentication of goods and business processes across supply chains, rather than financial crypto-asset services. (supports 3 items, gain 0.1602 bits, evidence verified)
- [rejected] at `crypto_asset_service_type`: new child_term_type **transaction_fraud_and_manipulation_risk** — Classifies whether the service concerns identifying wash trading, unfair trades, fraud or illicit flows in blockchain transactions. (supports 3 items, gain 0.1602 bits, evidence verified); values: detection or analysis of manipulation, fraud or illicit address scoring, not applicable
- [rejected] at `digital_asset_recording`: new value **ledger used for data storage or backup** — Blockchain used to store or anchor data, such as backups, encoded objects or storage metadata, rather than transactions. (supports 4 items, gain 0.1544 bits, evidence verified)
- [rejected] at `dlt_architecture`: new value **mutable or editable block history** — Ledger design that permits modification or editing of already-recorded blocks or transactions, contrasting with immutable chains. (supports 3 items, gain 0.1194 bits, evidence verified)