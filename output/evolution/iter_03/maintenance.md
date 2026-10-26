# Part 2 maintenance: the DAG as label space

8646 tagged items placed on 106/107 nodes (35576 tags, 160789 closure placements).

## Objectives: content-driven vs Part 1 prior

| metric | from tags (empirical) | from is-a weights (Part 1) |
|---|---|---|
| bits per descent (information gain) | 7.0214 | 4.8413 |
| AUC of reach-a-leaf | 0.7781 | 0.8506 |
| expected depth | 3.826 | 2.7404 |
| effective leaves | 21.747 | 22.452 |
| effective leaves / nodes | 0.2032 | 0.2098 |

## Where descents stop (top stop mass)

- Ledger purpose `ledger_purpose`: 0.2473
- Smart contract usage domain `smart_contract_usage_domain`: 0.0926
- Native asset versus token standard `native_vs_token_standard`: 0.0736
- Key custody and control model `key_custody_control_model`: 0.0504
- Privacy mechanism family `privacy_mechanism_family`: 0.0473
- Identity binding mechanism `identity_binding_mechanism`: 0.0429
- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`: 0.0328
- Smart contract / script language expressiveness `script_language_expressiveness`: 0.0299
- Centralisation of control `centralisation_level`: 0.029
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 0.0272
- Smart contract / distributed ledger application scope `smart_contract_definition_scope`: 0.0269
- Cross-chain transfer mechanism `cross_chain_transfer_mechanism`: 0.0251
- Privacy and anonymity features `privacy_enhancement`: 0.0234
- Interoperability and intraoperability `interoperability_type`: 0.0222
- Recording and cryptographic linkage `digital_asset_recording`: 0.0175

## Node statistics (nodes with items, by closure size)

| node | cat | direct | closure | children | value entropy | dominance | branching gain | residual |
|---|---|---|---|---|---|---|---|---|
| Crypto-asset definitional criteria | asset | 669 | 6974 | 10 | 1.0075 | 0.585 | 2.3656 | 60 (0.009) |
| Economic function of the asset | asset | 1161 | 6914 | 9 | 1.2702 | 0.685 | 2.7102 | 200 (0.029) |
| Legal classification of crypto-asset | asset | 79 | 6714 | 11 | 0.9945 | 0.667 | 2.6119 | 15 (0.002) |
| Reference asset type | asset | 249 | 6696 | 7 | 2.0657 | 0.398 | 2.0887 | 55 (0.008) |
| Issuer identifiability | asset | 77 | 6618 | 6 | 0.7916 | 0.818 | 1.2953 | 3 (0.0) |
| Payment stablecoin / e-money / ART reg | asset | 35 | 6615 | 3 | 1.7479 | 0.556 | 0.7067 | 10 (0.002) |
| Convertible virtual currency (CVC) sta | asset | 93 | 6473 | 1 | 0.0857 | 0.989 | 0.0565 | 42 (0.006) |
| Recording and cryptographic linkage | asset | 1944 | 6431 | 6 | 0.1751 | 0.974 | 1.6557 | 396 (0.062) |
| Governance model of a DLT system | techn | 541 | 6339 | 8 | 1.6071 | 0.554 | 2.7446 | 67 (0.011) |
| Ledger access and permissioning | techn | 1909 | 6272 | 14 | 1.6353 | 0.346 | 3.4186 | 126 (0.02) |
| Ledger scope: open or closed access by | techn | 403 | 6146 | 5 | 1.4594 | 0.448 | 1.9899 | 70 (0.011) |
| Network topology and node roles | techn | 1108 | 6076 | 7 | 1.1443 | 0.634 | 2.3609 | 99 (0.016) |
| Consensus mechanism | techn | 1269 | 5946 | 6 | 1.7609 | 0.434 | 2.3901 | 231 (0.039) |
| Validator reward mechanism | techn | 248 | 5715 | 4 | 0.5012 | 0.913 | 1.1776 | 57 (0.01) |
| Transaction fee regime | techn | 77 | 5658 | 2 | 2.1416 | 0.39 | 0.0948 | 18 (0.003) |
| Native asset presence and type | techn | 219 | 5640 | 4 | 1.0019 | 0.767 | 1.308 | 44 (0.008) |
| Ledger purpose | techn | 5629 | 5629 | 0 | 2.5676 | 0.335 | -0.0 | 5629 (1.0) |
| Software architecture (monolithic vs p | techn | 206 | 5576 | 5 | 0.8765 | 0.704 | 2.0922 | 39 (0.007) |
| Ledger storage model (what is stored o | techn | 761 | 5535 | 3 | 1.2341 | 0.695 | 1.5189 | 138 (0.025) |
| DLT data structure (blockchain vs non- | techn | 1944 | 4119 | 4 | 0.3306 | 0.951 | 1.8412 | 1153 (0.28) |
| Node / DLT network node role | techn | 914 | 3132 | 1 | 2.0469 | 0.429 | 0.7578 | 685 (0.219) |
| Decentralised system certification | techn | 110 | 2538 | 2 | 1.5587 | 0.409 | 0.8521 | 63 (0.025) |
| Source code openness | techn | 33 | 2475 | 2 | 0.1959 | 0.97 | 0.5786 | 9 (0.004) |
| Information and communications technol | techn | 63 | 2447 | 3 | 0.3955 | 0.922 | 1.5394 | 40 (0.016) |
| Identity layer and onboarding | techn | 910 | 2407 | 3 | 0.6793 | 0.82 | 1.7337 | 309 (0.128) |
| Smart contract / distributed ledger ap | techn | 1375 | 2211 | 2 | 1.1619 | 0.617 | 1.3927 | 412 (0.186) |
| Redemption mechanism | asset | 51 | 1433 | 4 | 1.757 | 0.462 | 1.7442 | 14 (0.01) |
| Form of holder claim | asset | 45 | 1419 | 4 | 1.1874 | 0.578 | 1.7368 | 7 (0.005) |
| Smart contract usage domain | techn | 1416 | 1416 | 0 | 2.8976 | 0.253 | -0.0 | 1416 (1.0) |
| Identity binding mechanism | techn | 1281 | 1281 | 0 | 2.2868 | 0.47 | -0.0 | 1281 (1.0) |
| Privacy and anonymity features | techn | 485 | 1120 | 2 | 0.8147 | 0.825 | 1.5121 | 281 (0.251) |
| Data classification (traffic, content, | techn | 0 | 1120 | 1 | - | - | -0.0 | 0 (0.0) |
| Source of yield | asset | 83 | 913 | 1 | 1.4585 | 0.437 | 0.3108 | 51 (0.056) |
| Yield distribution mechanism | asset | 14 | 862 | 1 | 1.0949 | 0.714 | 0.0912 | 10 (0.012) |
| Centralisation of control | asset | 572 | 852 | 2 | 1.4706 | 0.483 | 1.0489 | 536 (0.629) |
| Tokenisation form | asset | 299 | 720 | 2 | 1.3691 | 0.525 | 1.3583 | 224 (0.311) |
| Fungibility | asset | 413 | 702 | 1 | 0.6877 | 0.816 | 0.8731 | 206 (0.293) |
| Crypto-asset service provider or VASP  | actor | 155 | 666 | 16 | 1.803 | 0.609 | 3.4912 | 112 (0.168) |
| Smart contract / script language expre | techn | 359 | 626 | 3 | 0.8607 | 0.837 | 1.5321 | 308 (0.492) |
| Privacy mechanism family | techn | 567 | 567 | 0 | 2.0211 | 0.516 | -0.0 | 567 (1.0) |
| Offshore VASP status (activity-based o | actor | 0 | 554 | 2 | - | - | 0.9999 | 0 (0.0) |
| Jurisdictional regime and home or host | actor | 10 | 554 | 5 | 1.4354 | 0.545 | 1.5908 | 10 (0.018) |
| Financial institution status for AML | actor | 1 | 544 | 3 | -0.0 | 1.0 | 0.113 | 1 (0.002) |
| Principal or agent role in transaction | actor | 15 | 543 | 8 | 1.8256 | 0.333 | 2.0626 | 8 (0.015) |
| Custody model | actor | 64 | 534 | 6 | 1.6794 | 0.515 | 2.2414 | 41 (0.077) |
| Ledger partitioning or layering topolo | techn | 513 | 513 | 0 | 2.3605 | 0.279 | -0.0 | 513 (1.0) |
| Native asset versus token standard | asset | 383 | 496 | 1 | 1.3793 | 0.529 | 0.7982 | 376 (0.758) |
| Trading venue type | actor | 35 | 474 | 1 | 1.3472 | 0.611 | 0.3067 | 26 (0.055) |
| Control or sufficient influence over D | actor | 23 | 448 | 3 | 0.8281 | 0.739 | 1.1249 | 16 (0.036) |
| Crypto-asset service type | activ | 219 | 401 | 10 | 2.2942 | 0.459 | 3.1244 | 135 (0.337) |
| Infrastructure provider type | actor | 25 | 327 | 2 | 0.6988 | 0.885 | 0.8634 | 20 (0.061) |
| Wallet storage mode (hot or cold) | techn | 103 | 319 | 1 | 1.0623 | 0.544 | 0.562 | 42 (0.132) |
| Ecosystem participant role | actor | 256 | 307 | 4 | 2.2403 | 0.326 | 1.6357 | 245 (0.798) |
| Hosted versus unhosted (self-hosted) w | asset | 284 | 303 | 1 | 1.4251 | 0.554 | 0.6834 | 248 (0.818) |
| Key custody and control model | techn | 277 | 277 | 0 | 1.5741 | 0.546 | -0.0 | 277 (1.0) |
| Transfer of crypto-assets (travel rule | activ | 33 | 237 | 8 | -0.0 | 1.0 | 2.7385 | 19 (0.08) |
| Money transmission (acceptance and tra | activ | 8 | 218 | 5 | -0.0 | 1.0 | 2.0051 | 4 (0.018) |
| Public offer or private placement | activ | 22 | 214 | 3 | 0.4395 | 0.909 | 1.032 | 7 (0.033) |
| Offer and issuance method (token distr | activ | 49 | 207 | 3 | 1.1838 | 0.755 | 1.8139 | 42 (0.203) |
| Finality of agreement | techn | 181 | 195 | 1 | 0.9574 | 0.621 | 0.4929 | 174 (0.892) |
| Permitted control over client assets ( | actor | 25 | 182 | 3 | 1.3195 | 0.593 | 1.4467 | 15 (0.082) |
| Interoperability and intraoperability | techn | 181 | 181 | 0 | 1.4221 | 0.672 | -0.0 | 181 (1.0) |
| Smart contract deployment context | techn | 142 | 142 | 0 | 1.7415 | 0.544 | -0.0 | 142 (1.0) |
| Anti-money laundering obligations | oblig | 68 | 124 | 9 | 1.0432 | 0.681 | 2.3301 | 25 (0.202) |
| Wrapped / cross-chain representation | asset | 87 | 120 | 1 | 0.9953 | 0.54 | 0.86 | 34 (0.283) |
| Peer-to-peer (P2P) transaction | activ | 18 | 120 | 1 | 0.6144 | 0.889 | 0.469 | 12 (0.1) |
| Key splitting scheme | techn | 111 | 111 | 0 | 1.7814 | 0.479 | -0.0 | 111 (1.0) |
| Payment service and funds transfer | activ | 60 | 108 | 2 | -0.0 | 1.0 | 1.2708 | 27 (0.25) |
| Virtual assets as property or proceeds | oblig | 1 | 99 | 7 | -0.0 | 1.0 | 1.913 | 1 (0.01) |
| Freezing and blocking capability | oblig | 6 | 87 | 4 | -0.0 | 1.0 | 1.0826 | 4 (0.046) |
| Cross-chain transfer mechanism | asset | 86 | 86 | 0 | 1.7061 | 0.574 | -0.0 | 86 (1.0) |
| Illicit finance risk category | oblig | 75 | 83 | 2 | 1.4172 | 0.565 | 0.9399 | 59 (0.711) |
| Payment settlement mechanism | activ | 71 | 71 | 0 | 2.1603 | 0.325 | -0.0 | 71 (1.0) |
| Stablecoin issuer model | actor | 3 | 62 | 1 | 1.585 | 0.333 | 0.2056 | 2 (0.032) |
| Operator of crypto-asset arrangement | actor | 8 | 60 | 2 | 0.8113 | 0.75 | 0.5665 | 8 (0.133) |
| Key isolation from network connectivit | techn | 55 | 55 | 0 | 1.3735 | 0.589 | -0.0 | 55 (1.0) |
| Validator operation capacity (who may  | actor | 52 | 52 | 0 | 0.9687 | 0.712 | -0.0 | 52 (1.0) |
| Staking arrangement (self, delegated,  | activ | 10 | 48 | 1 | 1.571 | 0.6 | 0.7383 | 10 (0.208) |
| Central bank digital currency status | asset | 46 | 46 | 0 | 0.973 | 0.596 | -0.0 | 46 (1.0) |
| Asset supply management (monetary poli | techn | 43 | 43 | 0 | 1.3548 | 0.605 | -0.0 | 43 (1.0) |
| Minting mechanism | activ | 38 | 38 | 0 | 2.0071 | 0.447 | -0.0 | 38 (1.0) |
| Key management control model | activ | 35 | 35 | 0 | 1.8622 | 0.395 | -0.0 | 35 (1.0) |
| Anonymity-enhancing crypto-asset statu | oblig | 23 | 23 | 0 | 0.8281 | 0.739 | -0.0 | 23 (1.0) |
| Finality mechanism | techn | 21 | 21 | 0 | 1.717 | 0.429 | -0.0 | 21 (1.0) |
| Ancillary asset and network token stat | asset | 14 | 14 | 0 | 0.9403 | 0.643 | -0.0 | 14 (1.0) |
| Excluded instrument category (EU scope | oblig | 1 | 13 | 4 | -0.0 | 1.0 | 1.9766 | 1 (0.077) |
| Nexus to jurisdiction (services offere | activ | 13 | 13 | 0 | -0.0 | 1.0 | -0.0 | 13 (1.0) |
| Investment contract (Howey) criteria | oblig | 4 | 12 | 3 | 0.8113 | 0.75 | 1.9329 | 4 (0.333) |
| Security status of digital asset (US e | oblig | 1 | 12 | 2 | -0.0 | 1.0 | 0.8113 | 0 (0.0) |
| MiFID financial instrument status | oblig | 1 | 12 | 2 | -0.0 | 1.0 | 1.0 | 0 (0.0) |
| Address linkage to service provider | actor | 2 | 8 | 1 | 1.0 | 0.5 | 0.5436 | 1 (0.125) |
| Reference currency for stablecoin peg  | asset | 8 | 8 | 0 | 1.0 | 0.5 | -0.0 | 8 (1.0) |
| Originator and beneficiary role | actor | 2 | 7 | 1 | 1.0 | 0.5 | 0.8631 | 2 (0.286) |
| Consumer or retail versus professional | actor | 5 | 5 | 1 | -0.0 | 1.0 | -0.0 | 5 (1.0) |
| Exemption from MSB status | oblig | 1 | 5 | 2 | -0.0 | 1.0 | 1.371 | 1 (0.2) |
| Redemption and reserve adequacy | oblig | 1 | 4 | 4 | -0.0 | 1.0 | 2.2464 | 1 (0.25) |
| Yield or interest on stablecoin | oblig | 0 | 4 | 2 | - | - | 0.9183 | 0 (0.0) |
| Settlement finality and legal enforcea | oblig | 1 | 3 | 3 | -0.0 | 1.0 | 1.9502 | 1 (0.333) |
| Tax reporting obligation status (CARF) | oblig | 3 | 3 | 0 | -0.0 | 1.0 | -0.0 | 3 (1.0) |
| ICT and operational resilience risk | oblig | 1 | 2 | 1 | -0.0 | 1.0 | 1.0 | 1 (0.5) |
| Prudential classification group (Basel | oblig | 0 | 2 | 1 | - | - | -0.0 | 0 (0.0) |
| Traditional finance analogue | oblig | 0 | 2 | 1 | - | - | -0.0 | 0 (0.0) |
| Expressiveness claim basis | techn | 2 | 2 | 0 | 1.0 | 0.5 | -0.0 | 2 (1.0) |
| Pooled investment vehicle structure | actor | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Safeguarding and custody obligation | oblig | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Serious crime threshold for predicate  | oblig | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |

## Maintenance proposals

**Dormant nodes (1)**, no items in this batch: `related_person_affiliation`

**Collapsed nodes (12)**, many items but one value absorbs them (merge or re-split candidates):
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 1944 items, dominance 0.951 (blockchain (chain of blocks))
- Source code openness `code_license_openness`: 33 items, dominance 0.97 (open source)
- Validator reward mechanism `reward_mechanism`: 248 items, dominance 0.913 (lump-sum reward)
- Infrastructure provider type `infrastructure_provider_type`: 25 items, dominance 0.885 (oracle)
- Peer-to-peer (P2P) transaction `transaction_type_p2p`: 18 items, dominance 0.889 (person-to-person transfer)
- Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`: 33 items, dominance 1.0 (transfer of crypto-assets (covered))
- Payment service and funds transfer `payment_or_transfer_service`: 60 items, dominance 1.0 (transfer of funds)
- Convertible virtual currency (CVC) status `convertible_virtual_currency_status`: 93 items, dominance 0.989 (convertible virtual currency (CVC))
- Recording and cryptographic linkage `digital_asset_recording`: 1944 items, dominance 0.974 (recorded on cryptographically secured distributed ledger)
- Information and communications technology system `ict_system_scope`: 63 items, dominance 0.922 (ICT / computer system)
- Public offer or private placement `decentralised_or_centralised_offer_model`: 22 items, dominance 0.909 (offer to the public)
- Nexus to jurisdiction (services offered in jurisdiction) `service_location_nexus`: 13 items, dominance 1.0 (services offered to residents or customers in jurisdiction)

**Highest-gain nodes**:
- Crypto-asset service provider or VASP status `service_provider_status`: 3.4912 bits over 666 items
- Ledger access and permissioning `ledger_access_permission`: 3.4186 bits over 6272 items
- Crypto-asset service type `crypto_asset_service_type`: 3.1244 bits over 401 items
- Governance model of a DLT system `governance_model`: 2.7446 bits over 6339 items
- Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`: 2.7385 bits over 237 items
- Economic function of the asset `crypto_asset_function`: 2.7102 bits over 6914 items
- Legal classification of crypto-asset `legal_classification_status`: 2.6119 bits over 6714 items
- Consensus mechanism `consensus_mechanism`: 2.3901 bits over 5946 items

**Discovery targets (32)**, residual >= threshold:
- Ledger purpose `ledger_purpose`: 5629 residual of 5629 (1.0)
- Smart contract usage domain `smart_contract_usage_domain`: 1416 residual of 1416 (1.0)
- Identity binding mechanism `identity_binding_mechanism`: 1281 residual of 1281 (1.0)
- Privacy mechanism family `privacy_mechanism_family`: 567 residual of 567 (1.0)
- Centralisation of control `centralisation_level`: 536 residual of 852 (0.629)
- Ledger partitioning or layering topology `ledger_partitioning_topology`: 513 residual of 513 (1.0)
- Native asset versus token standard `native_vs_token_standard`: 376 residual of 496 (0.758)
- Smart contract / script language expressiveness `script_language_expressiveness`: 308 residual of 626 (0.492)
- Key custody and control model `key_custody_control_model`: 277 residual of 277 (1.0)
- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`: 248 residual of 303 (0.818)
- Ecosystem participant role `ecosystem_participant_role`: 245 residual of 307 (0.798)
- Tokenisation form `tokenisation_form`: 224 residual of 720 (0.311)
- Interoperability and intraoperability `interoperability_type`: 181 residual of 181 (1.0)
- Finality of agreement `consensus_finality`: 174 residual of 195 (0.892)
- Smart contract deployment context `smart_contract_deployment_context`: 142 residual of 142 (1.0)
- Crypto-asset service type `crypto_asset_service_type`: 135 residual of 401 (0.337)
- Key splitting scheme `key_splitting_scheme`: 111 residual of 111 (1.0)
- Cross-chain transfer mechanism `cross_chain_transfer_mechanism`: 86 residual of 86 (1.0)
- Payment settlement mechanism `payment_settlement_mechanism`: 71 residual of 71 (1.0)
- Illicit finance risk category `risk_type_illicit_finance`: 59 residual of 83 (0.711)
- Key isolation from network connectivity `key_isolation_from_network`: 55 residual of 55 (1.0)
- Validator operation capacity (who may run a node) `consensus_participant_validator_capacity`: 52 residual of 52 (1.0)
- Central bank digital currency status `central_bank_digital_currency`: 46 residual of 46 (1.0)
- Asset supply management (monetary policy) `asset_supply_policy`: 43 residual of 43 (1.0)
- Minting mechanism `minting_mechanism`: 38 residual of 38 (1.0)
- Key management control model `key_management_control_model`: 35 residual of 35 (1.0)
- Anonymity-enhancing crypto-asset status `anonymity_enhancing_status`: 23 residual of 23 (1.0)
- Finality mechanism `finality_mechanism`: 21 residual of 21 (1.0)
- Ancillary asset and network token status `ancillary_asset_status`: 14 residual of 14 (1.0)
- Nexus to jurisdiction (services offered in jurisdiction) `service_location_nexus`: 13 residual of 13 (1.0)
- Reference currency for stablecoin peg (currency vs other) `native_vs_stable_price_reference_asset_currency`: 8 residual of 8 (1.0)
- Consumer or retail versus professional user `consumer_vs_professional_status`: 5 residual of 5 (1.0)

## Discovery (Task E) candidates

- [ACCEPTED] at `service_location_nexus`: new value **services offered to merchants accepting cryptocurrency payments** — Crypto-asset payment acceptance services offered to merchants or retailers in the jurisdiction, creating a nexus through the merchant-facing service rather than the end user. (supports 5 of 13 shown, est. 5 of 13 residual, gain 0.9612 bits, evidence verified)
- [ACCEPTED] at `anonymity_enhancing_status`: new value **traceable-but-pseudonymous ledger** — Transfers are publicly visible and linked to pseudonymous addresses, so they can be traced and deanonymised with analytics and clustering. (supports 5 of 23 shown, est. 5 of 23 residual, gain 0.7554 bits, evidence verified)
- [ACCEPTED] at `minting_mechanism`: new value **NFT creation via marketplace or service minting** — Units created by an NFT creator, marketplace, or platform service minting a token on request, without a consensus, collateral, or protocol-rule trigger. (supports 6 of 38 shown, est. 6 of 38 residual, gain 0.6292 bits, evidence verified)
- [ACCEPTED] at `privacy_mechanism_family`: new child_term_type **zero-knowledge proof system variant** — Distinguishes the specific zero-knowledge proof construction employed to hide witnesses while proving statements. (supports 6 of 40 shown, est. 85 of 567 residual, gain 0.6096 bits, evidence verified); values: zk-SNARK, zk-STARK, Sigma protocol / interactive-style proof, Bulletproofs (short range/inner-product proofs), one-out-of-many / ring proofs, non-interactive ZKP (unspecified)
- [ACCEPTED] at `key_management_control_model`: new child_term_type **key share distribution topology** — Describes where and among whom the secret key shares or portions reside when a key is split for control. (supports 5 of 35 shown, est. 5 of 35 residual, gain 0.5917 bits, evidence verified); values: across physical devices, among participants, across data centres, split between client and custodian
- [ACCEPTED] at `interoperability_type`: new value **external data oracle** — Interoperability achieved by an oracle or relay that attests to or forwards data from one chain to another via a trusted or voting-based party. (supports 5 of 40 shown, est. 23 of 181 residual, gain 0.5494 bits, evidence verified)
- [ACCEPTED] at `interoperability_type`: new value **domain-name-based chain addressing** — Cross-chain access resolves target chains through human-readable blockchain domain names rather than raw network identifiers. (supports 5 of 40 shown, est. 23 of 181 residual, gain 0.5494 bits, evidence verified)
- [ACCEPTED] at `interoperability_type`: new value **cross-chain transaction forwarding with hop limit** — Transactions or messages are relayed across a bounded sequence of intermediate chains or hops to reach the destination ledger. (supports 5 of 40 shown, est. 23 of 181 residual, gain 0.5494 bits, evidence verified)
- [ACCEPTED] at `payment_settlement_mechanism`: new child_term_type **fiat-rail integration** — Distinguishes whether crypto payments are bridged into fiat card, bank, or clearing networks during settlement. (supports 5 of 40 shown, est. 9 of 71 residual, gain 0.5485 bits, evidence verified); values: card-network bridged, bank transfer bridged, no fiat leg
- [ACCEPTED] at `identity_binding_mechanism`: new value **DID-anchored verifiable credential** — Identity is bound by issuing and verifying signed credentials that reference a decentralised identifier held in a user wallet. (supports 5 of 40 shown, est. 160 of 1281 residual, gain 0.5433 bits, evidence verified)
- [ACCEPTED] at `unhosted_vs_hosted_wallet`: new child_term_type **key_recovery_mechanism** — Mechanism by which lost wallet keys or seed phrases are restored, distinguishing recovery designs for hosted and unhosted wallets. (supports 6 of 40 shown, est. 37 of 248 residual, gain 0.4975 bits, evidence verified); values: seed phrase backup, secret sharing / social recovery, service-assisted recovery, threshold multiparty recovery, no recovery supported
- [ACCEPTED] at `risk_type_illicit_finance`: new value **wallet risk scoring and taint tracking** — Risk assessed by scoring addresses or wallets for criminal association and tracing tainted funds through transaction graphs. (supports 5 of 40 shown, est. 7 of 59 residual, gain 0.3735 bits, evidence verified)
- [ACCEPTED] at `centralisation_level`: new value **hybrid server-matching with decentralised execution** — Control is split: a central server or operator handles matching, coordination or access while settlement or execution remains decentralised on-chain. (supports 5 of 40 shown, est. 67 of 536 residual, gain 0.3416 bits, evidence verified)
- [ACCEPTED] at `script_language_expressiveness`: new child_term_type **Script verification approach** — The method or stage at which a smart contract's behaviour or safety is checked. (supports 5 of 40 shown, est. 38 of 308 residual, gain 0.2623 bits, evidence verified); values: static analysis, formal verification, runtime metering, fuzzing
- [ACCEPTED] at `tokenisation_form`: new value **tokenised physical commodity or precious metal** — A token representing ownership of a physical commodity, precious metal, or natural resource held in custody or inventory. (supports 6 of 40 shown, est. 34 of 224 residual, gain 0.1638 bits, evidence verified)
- [ACCEPTED] at `tokenisation_form`: new value **tokenised intellectual property or contractual claim** — A token representing rights in intellectual property, receivables, debt, or loan-backed equity rather than a physical asset. (supports 5 of 40 shown, est. 28 of 224 residual, gain 0.145 bits, evidence verified)
- [ACCEPTED] at `tokenisation_form`: new child_term_type **backing_of_token** — Splits tokens by the reserve or collateral that underpins their value, distinguishing asset-backed from unbacked tokens. (supports 5 of 40 shown, est. 28 of 224 residual, gain 0.145 bits, evidence verified); values: fully asset-backed, partially or fractionally backed, collateralised by claims or loans, unbacked
- [rejected] at `consumer_vs_professional_status`: new value **academic or research study participant** — Actor is a researcher or study subject whose role is neither a consumer holder nor a trading professional, as in survey or interview research. (supports 3 of 5 shown, est. 3 of 5 residual, gain 0.971 bits, evidence verified)
- [rejected] at `native_vs_stable_price_reference_asset_currency`: new value **pegged to a non-fiat reference asset** — Stablecoin whose peg target is a commodity, basket, or cryptocurrency rather than a fiat currency. (supports 3 of 8 shown, est. 3 of 8 residual, gain 0.9544 bits, evidence verified)
- [rejected] at `service_location_nexus`: new value **services offered to remittance senders or recipients across borders** — Cross-border remittance or fiat-crypto conversion services where the nexus arises from sender or recipient location in the jurisdiction. (supports 4 of 13 shown, est. 4 of 13 residual, gain 0.8905 bits, evidence verified)
- [rejected] at `ancillary_asset_status`: new value **application-level or non-tradeable token** — Token whose value derives from access, reputation, or usage within an application rather than from the ledger or an originator's enterprise. (supports 3 of 14 shown, est. 3 of 14 residual, gain 0.7496 bits, evidence verified)
- [rejected] at `ancillary_asset_status`: new child_term_type **token backing** — Splits tokens by whether their value is anchored to a physical or financial asset, the network, or nothing beyond market demand. (supports 3 of 14 shown, est. 3 of 14 residual, gain 0.7496 bits, evidence verified); values: physical or real-world asset backed, network utility backed, market-demand only
- [rejected] at `finality_mechanism`: new value **layer-2 / off-chain dispute resolution** — Finality is achieved by settling on a parent chain only if a challenge or dispute window passes without contest, with the base chain serving as arbiter. (supports 4 of 21 shown, est. 4 of 21 residual, gain 0.7025 bits, evidence verified)
- [rejected] at `finality_mechanism`: new value **cross-chain confirmation / pending-state commit** — Finality for a cross-chain transaction is established by waiting for confirmation or receipt from a target chain before committing the transaction. (supports 3 of 21 shown, est. 3 of 21 residual, gain 0.5917 bits, evidence verified)
- [rejected] at `finality_mechanism`: new value **threshold signature / notarization voting** — A leader proposes a block and a threshold of validator signatures or notarization votes certifies it as final. (supports 3 of 21 shown, est. 3 of 21 residual, gain 0.5917 bits, evidence verified)
- [rejected] at `anonymity_enhancing_status`: new child_term_type **anonymity-enhancement mechanism** — Identifies the technical mechanism, if any, that obscures sender, receiver or amount in transactions. (supports 3 of 23 shown, est. 3 of 23 residual, gain 0.5586 bits, evidence unverified); values: ring signatures and stealth addresses, zero-knowledge proofs, coin mixing or tumbling, none (transparent ledger)
- [rejected] at `key_management_control_model`: new value **policy-map endorsement control** — Signing authority is granted only when a policy map of access rules is satisfied by a threshold of endorsement messages from designated parties or devices. (supports 4 of 35 shown, est. 4 of 35 residual, gain 0.5127 bits, evidence verified)
- [rejected] at `key_isolation_from_network`: new child_term_type **unidirectional or one-way data transfer** — Distinguishes isolated devices that exchange data via one-way channels (e.g., QR codes, optical or data diodes) from those with bidirectional links. (supports 4 of 40 shown, est. 6 of 55 residual, gain 0.4972 bits, evidence verified); values: one-way (unidirectional channel), bidirectional, none (no transfer)
- [rejected] at `key_isolation_from_network`: new child_term_type **proximity wireless link** — Classifies how a key-holding device communicates with a nearby host, such as NFC, Bluetooth or other proximity links, separate from internet connectivity. (supports 4 of 40 shown, est. 6 of 55 residual, gain 0.4972 bits, evidence verified); values: NFC, Bluetooth or BLE, USB or wired, none (QR or manual transfer)
- [rejected] at `central_bank_digital_currency`: new child_term_type **CBDC design model** — Splits CBDC proposals by whether the central bank issues directly to the public or distributes through intermediaries. (supports 4 of 40 shown, est. 5 of 46 residual, gain 0.496 bits, evidence verified); values: direct (retail) CBDC, intermediated CBDC, hybrid CBDC
- [rejected] at `key_custody_control_model`: new value **multi-party computation (MPC) key system** — Key material is never assembled; parties jointly compute signatures over private shares without revealing their private data. (supports 4 of 40 shown, est. 28 of 277 residual, gain 0.4724 bits, evidence verified)
- [rejected] at `key_custody_control_model`: new value **social key recovery** — Key shards or recovery material are held by trusted contacts or social-service guardians who help restore access. (supports 4 of 40 shown, est. 28 of 277 residual, gain 0.4724 bits, evidence verified)
- [rejected] at `key_custody_control_model`: new value **hierarchical delegated authority with clawback** — Access is delegated through a hierarchy of keys or key pages, with the ability to revoke or reclaim control. (supports 4 of 40 shown, est. 28 of 277 residual, gain 0.4724 bits, evidence verified)
- [rejected] at `smart_contract_usage_domain`: new value **peer-to-peer energy trading** — Blockchain-based peer-to-peer electricity and energy trading among prosumers, EVs, and grid participants. (supports 4 of 40 shown, est. 142 of 1416 residual, gain 0.4699 bits, evidence unverified)
- [rejected] at `identity_binding_mechanism`: new value **pairwise or relationship-scoped DID** — Identity is bound through pairwise or per-relationship DIDs that limit correlation across counterparties. (supports 4 of 40 shown, est. 128 of 1281 residual, gain 0.4687 bits, evidence verified)
- [rejected] at `identity_binding_mechanism`: new child_term_type **DID binding scope** — Distinguishes whether the decentralised identifier denotes a human, a delegated actor, an object or device, or a data or algorithm artefact. (supports 4 of 40 shown, est. 128 of 1281 residual, gain 0.4687 bits, evidence verified); values: human participant, delegated or pairwise actor, physical object or IoT device, data or algorithm artefact
- [rejected] at `payment_settlement_mechanism`: new value **token-redemption escrow release** — Payment is settled by locking funds in escrow and releasing them to the payee upon a redemption or delivery condition being met. (supports 4 of 40 shown, est. 7 of 71 residual, gain 0.4645 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **logistics / shipping / cargo tracking** — Smart contracts deployed to track goods, shipments, containers or transport events in logistics networks. (supports 4 of 40 shown, est. 14 of 142 residual, gain 0.4645 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **food / pharmaceutical traceability** — Smart contracts deployed to trace food, drugs or dairy products along supply chains and prevent counterfeiting. (supports 4 of 40 shown, est. 14 of 142 residual, gain 0.4645 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **trading / exchange / commerce** — Smart contracts deployed for trading, automated market making, escrow or commerce between parties. (supports 4 of 40 shown, est. 14 of 142 residual, gain 0.4645 bits, evidence verified)
- [rejected] at `asset_supply_policy`: new value **supply managed by protocol-defined issuance schedule** — Native asset supply is created by the protocol at a predetermined rate or schedule, such as block rewards with periodic halvings, without a hard cap. (supports 4 of 40 shown, est. 4 of 43 residual, gain 0.4465 bits, evidence verified)
- [rejected] at `asset_supply_policy`: new value **elastic supply adjusted by algorithm or governance** — Supply expands or contracts in response to demand, price targets, or governance decisions rather than a fixed schedule. (supports 4 of 40 shown, est. 4 of 43 residual, gain 0.4465 bits, evidence unverified)
- [rejected] at `key_management_control_model`: new value **possession-token-bound key storage** — Private key is stored in a cryptographically secured container bound to a physical or logical possession token that controls access. (supports 3 of 35 shown, est. 3 of 35 residual, gain 0.422 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **Passive or rate-based issuance** — Units issued continuously or by a predetermined inflation schedule to users or participants rather than in response to a discrete event. (supports 3 of 38 shown, est. 3 of 38 residual, gain 0.3985 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **Burn-triggered issuance to members** — Units minted in proportion to tokens sent to burn addresses, with the minted amount allocated to participating entities. (supports 3 of 38 shown, est. 3 of 38 residual, gain 0.3985 bits, evidence verified)
- [rejected] at `consensus_participant_validator_capacity`: new value **permissioned consortium member validation** — Validators are drawn from a known consortium of organisations that each hold a fixed membership role in the permissioned network. (supports 3 of 40 shown, est. 4 of 52 residual, gain 0.3912 bits, evidence unverified)
- [rejected] at `consensus_participant_validator_capacity`: new value **stake- or vote-weighted delegated selection** — Validators or block producers are chosen dynamically by stake, votes, or a scoring criterion rather than open entry or fixed authority. (supports 3 of 40 shown, est. 4 of 52 residual, gain 0.3912 bits, evidence verified)
- [rejected] at `consensus_participant_validator_capacity`: new child_term_type **validator selection basis** — Distinguishes how validator membership or influence is determined once a participant is permitted to take part. (supports 3 of 40 shown, est. 4 of 52 residual, gain 0.3912 bits, evidence unverified); values: fixed role or authority, stake or token holdings, vote or election, reputation or trust score, resource or computing power, random or rotating selection
- [rejected] at `privacy_mechanism_family`: new value **trusted execution environment** — Confidentiality provided by hardware-isolated enclaves that run computations on private data. (supports 3 of 40 shown, est. 43 of 567 residual, gain 0.3873 bits, evidence verified)
- [rejected] at `privacy_mechanism_family`: new value **ring signatures and mixing (anonymity sets)** — Hides the sender or transaction origin among a set of candidates via ring or mixing constructions. (supports 3 of 40 shown, est. 43 of 567 residual, gain 0.3873 bits, evidence verified)
- [rejected] at `privacy_mechanism_family`: new value **threshold and multi-party secret sharing** — Splits keys or data across nodes so that a threshold of parties is needed to recover or decrypt. (supports 3 of 40 shown, est. 43 of 567 residual, gain 0.3873 bits, evidence verified)
- [rejected] at `unhosted_vs_hosted_wallet`: new value **hybrid / shared-control wallet** — Wallet where control of signing keys is split between the user and a service provider, neither holding full control alone. (supports 4 of 40 shown, est. 25 of 248 residual, gain 0.386 bits, evidence verified)
- [rejected] at `ledger_purpose`: new value **supply chain traceability and product provenance** —  (supports 3 of 40 shown, est. 422 of 5629 residual, gain 0.3842 bits, evidence verified)
- [rejected] at `smart_contract_usage_domain`: new value **agriculture and water management** — Smart contracts and ledgers used for agricultural supply traceability, crop insurance, and farm produce distribution. (supports 3 of 40 shown, est. 106 of 1416 residual, gain 0.3838 bits, evidence verified)
- [rejected] at `smart_contract_usage_domain`: new value **logistics and maritime supply chains** — Smart contracts for logistics, maritime, and inter-organisational supply chain collaboration and inventory management. (supports 3 of 40 shown, est. 106 of 1416 residual, gain 0.3838 bits, evidence verified)
- [rejected] at `key_splitting_scheme`: new value **seed phrase distributed across devices** — The seed phrase or wallet recovery secret is divided into portions stored on multiple devices or locations and reconstructed from a sufficient subset. (supports 3 of 40 shown, est. 8 of 111 residual, gain 0.3736 bits, evidence verified)
- [rejected] at `key_splitting_scheme`: new value **key recovery via user supplemental information** — The key is divided or regenerated using user-supplied factors such as password, biometrics, or social contacts as shares. (supports 3 of 40 shown, est. 8 of 111 residual, gain 0.3736 bits, evidence verified)
- [rejected] at `key_splitting_scheme`: new value **encrypted key fragments with off-chain storage** — The private key is encrypted and then split into fragments distributed among storage peers or nodes. (supports 3 of 40 shown, est. 8 of 111 residual, gain 0.3736 bits, evidence verified)
- [rejected] at `payment_settlement_mechanism`: new value **unidirectional channel swap** — Settlement of cross-chain token swaps performed peer-to-peer over unidirectional payment channels without escrow. (supports 3 of 40 shown, est. 5 of 71 residual, gain 0.3675 bits, evidence verified)
- [rejected] at `cross_chain_transfer_mechanism`: new value **relay with trusted execution environment** — Cross-chain data or assets are relayed and verified via a relay node running inside a trusted execution environment. (supports 3 of 40 shown, est. 6 of 86 residual, gain 0.3651 bits, evidence verified)
- [rejected] at `cross_chain_transfer_mechanism`: new value **notary / validator-committee attestation** — Transfers are authorised by a designated set of notary or validator nodes that attest to events on the source chain. (supports 3 of 40 shown, est. 6 of 86 residual, gain 0.3651 bits, evidence verified)
- [rejected] at `cross_chain_transfer_mechanism`: new value **burn-and-mint across a common ledger** — Tokens are burned on the origin ledger and freshly minted on the target ledger, with a common ledger coordinating the exchange. (supports 3 of 40 shown, est. 6 of 86 residual, gain 0.3651 bits, evidence verified)
- [rejected] at `asset_supply_policy`: new value **deflationary or burn-based supply reduction** — Native asset supply is reduced over time through token burning or fee destruction, making net issuance negative. (supports 3 of 40 shown, est. 3 of 43 residual, gain 0.3651 bits, evidence verified)
- [rejected] at `asset_supply_policy`: new value **supply minted on demand by a central authority** — Tokens are created or destroyed by a central issuer to maintain a peg or match demand, rather than by protocol rules alone. (supports 3 of 40 shown, est. 3 of 43 residual, gain 0.3651 bits, evidence verified)
- [rejected] at `native_vs_token_standard`: new value **ERC-721 non-fungible token** — A non-fungible token standard on Ethereum, distinct from fungible ERC-20 interfaces, used for unique digital assets. (supports 4 of 40 shown, est. 38 of 376 residual, gain 0.3581 bits, evidence verified)
- [rejected] at `native_vs_token_standard`: new child_term_type **token_fungibility** — Splits token-standard assets by whether individual units are interchangeable or uniquely identified. (supports 4 of 40 shown, est. 38 of 376 residual, gain 0.3581 bits, evidence verified); values: fungible, non-fungible, semi-fungible, not applicable
- [rejected] at `central_bank_digital_currency`: new child_term_type **CBDC access scope** — Distinguishes retail CBDC accessible to households from wholesale CBDC limited to banks for interbank settlement. (supports 3 of 40 shown, est. 3 of 46 residual, gain 0.3478 bits, evidence verified); values: retail CBDC, wholesale CBDC
- [rejected] at `central_bank_digital_currency`: new value **stablecoin (fiat-pegged private token)** — Privately issued crypto-asset whose value is tied to a fiat currency, not a central bank liability. (supports 3 of 40 shown, est. 3 of 46 residual, gain 0.3478 bits, evidence verified)
- [rejected] at `consensus_finality`: new value **accountable safety** — Protocol guarantees that if safety is violated, a set of validators who misbehaved can be identified and held accountable. (supports 3 of 40 shown, est. 13 of 174 residual, gain 0.342 bits, evidence verified)
- [rejected] at `key_management_control_model`: new value **trusted execution enclave key control** — Private keys are held and used inside a processor enclave or trusted execution environment rather than an external HSM. (supports 2 of 35 shown, est. 2 of 35 residual, gain 0.316 bits, evidence verified)
- [rejected] at `key_isolation_from_network`: new value **physical key medium (etched gemstone)** — Keys are stored as physical engravings or etchings on a material object such as a gemstone, rather than on an electronic device. (supports 2 of 40 shown, est. 3 of 55 residual, gain 0.3054 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **Cross-chain transfer minting** — New units created on a destination chain in exchange for assets locked or burned on a source chain, or by re-issuing an existing token on a secondary platform. (supports 2 of 38 shown, est. 2 of 38 residual, gain 0.2975 bits, evidence verified)
- [rejected] at `centralisation_level`: new value **centrally issued and administered** — A single authority issues, mints, and administers tokens or records, typically off-chain or on a permissioned ledger, with centrally controlled rules. (supports 4 of 40 shown, est. 54 of 536 residual, gain 0.2962 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **mining pool operator** — Entity that aggregates hash power from many miners to share block rewards, distinct from individual miners and network validators. (supports 4 of 40 shown, est. 24 of 245 residual, gain 0.2704 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **retail trader / holder** — End user who buys, sells or holds crypto-assets for personal investment or payment, as opposed to issuers, operators or infrastructure providers. (supports 4 of 40 shown, est. 24 of 245 residual, gain 0.2704 bits, evidence verified)
- [rejected] at `risk_type_illicit_finance`: new value **wash trading / market manipulation** — Risk that crypto-asset activity involves artificial volume or price manipulation such as pump-and-dump schemes. (supports 3 of 40 shown, est. 4 of 59 residual, gain 0.2542 bits, evidence verified)
- [rejected] at `risk_type_illicit_finance`: new value **corruption** — Risk that crypto-asset activity enables bribery, corrupt public officials, or illicit proceeds from corruption. (supports 3 of 40 shown, est. 4 of 59 residual, gain 0.2542 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **block builder / relay operator** — Actor constructing or relaying blocks under proposer-builder separation to capture maximal extractable value. (supports 3 of 40 shown, est. 18 of 245 residual, gain 0.2215 bits, evidence verified)
- [rejected] at `script_language_expressiveness`: new value **Turing incomplete with static analysis** — A non-Turing complete language explicitly designed to permit static analysis before publication. (supports 3 of 40 shown, est. 23 of 308 residual, gain 0.1864 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **voting / governance / e-democracy** — Smart contracts deployed to run elections, voting protocols or organizational governance. (supports 1 of 40 shown, est. 4 of 142 residual, gain 0.1851 bits, evidence verified)
- [rejected] at `ledger_purpose`: new value **energy trading and dispatch coordination** — Ledger used to coordinate energy trading, dispatch, or microgrid information exchange. (supports 1 of 40 shown, est. 141 of 5629 residual, gain 0.1689 bits, evidence verified)
- [rejected] at `smart_contract_usage_domain`: new value **pharmaceutical distribution and prescriptions** — Ledgers used for drug distribution, good distribution practice, and prescription refill management. (supports 1 of 40 shown, est. 35 of 1416 residual, gain 0.1672 bits, evidence verified)
- [rejected] at `crypto_asset_service_type`: new child_term_type **custody key control model** — Describes whether keys are held by the service provider, distributed among parties, or held by the user under the custodial arrangement. (supports 5 of 40 shown, est. 17 of 135 residual, gain 0.0537 bits, evidence verified); values: single custodian holds keys, distributed or threshold key shares, user-held keys with provider assistance, hardware security module controlled
- [rejected] at `crypto_asset_service_type`: new value **liquidity provision / redemption** — Actor supplies liquidity to a pool or redeems its liquidity position, as in automated market maker pools. (supports 4 of 40 shown, est. 14 of 135 residual, gain 0.0473 bits, evidence verified)
- [rejected] at `crypto_asset_service_type`: new value **escrow and atomic swap** — Actor holds assets in escrow and performs conditional or atomic exchange between parties without a conventional order book. (supports 4 of 40 shown, est. 14 of 135 residual, gain 0.0473 bits, evidence verified)
- [rejected] at `crypto_asset_service_type`: new value **collateral management / lending** — Actor takes collateral, extends credit or manages loan terms and repayment against crypto-assets. (supports 4 of 40 shown, est. 14 of 135 residual, gain 0.0473 bits, evidence verified)
- [rejected] at `ledger_partitioning_topology`: new value **sharded chain** — Ledger partitioned into shards that each process a subset of transactions in parallel; already exists as 'sharded chain' so this is a duplicate and should not be added. (supports 0 of 40 shown, est. 0 of 513 residual, gain 0.0 bits, evidence unverified)