# Part 2 maintenance: the DAG as label space

8646 tagged items placed on 98/99 nodes (35099 tags, 155087 closure placements).

## Objectives: content-driven vs Part 1 prior

| metric | from tags (empirical) | from is-a weights (Part 1) |
|---|---|---|
| bits per descent (information gain) | 6.9602 | 4.8239 |
| AUC of reach-a-leaf | 0.7714 | 0.8427 |
| expected depth | 3.6958 | 2.7029 |
| effective leaves | 21.256 | 18.496 |
| effective leaves / nodes | 0.2147 | 0.1868 |

## Where descents stop (top stop mass)

- Ledger purpose `ledger_purpose`: 0.222
- Smart contract usage domain `smart_contract_usage_domain`: 0.0947
- Native asset versus token standard `native_vs_token_standard`: 0.0895
- Privacy mechanism family `privacy_mechanism_family`: 0.0588
- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`: 0.0449
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 0.0391
- Identity binding mechanism `identity_binding_mechanism`: 0.0389
- Smart contract / distributed ledger application scope `smart_contract_definition_scope`: 0.0347
- Centralisation of control `centralisation_level`: 0.0343
- Privacy and anonymity features `privacy_enhancement`: 0.0326
- Smart contract / script language expressiveness `script_language_expressiveness`: 0.0321
- Interoperability and intraoperability `interoperability_type`: 0.0266
- Recording and cryptographic linkage `digital_asset_recording`: 0.0246
- Wallet storage mode (hot or cold) `wallet_type_storage`: 0.0201
- Node / DLT network node role `ledger_node_role`: 0.0191

## Node statistics (nodes with items, by closure size)

| node | cat | direct | closure | children | value entropy | dominance | branching gain | residual |
|---|---|---|---|---|---|---|---|---|
| Crypto-asset definitional criteria | asset | 806 | 6706 | 10 | 0.986 | 0.614 | 2.3748 | 94 (0.014) |
| Economic function of the asset | asset | 1221 | 6612 | 9 | 1.3329 | 0.667 | 2.7319 | 193 (0.029) |
| Legal classification of crypto-asset | asset | 85 | 6419 | 11 | 1.2016 | 0.648 | 2.6492 | 23 (0.004) |
| Governance model of a DLT system | techn | 519 | 6407 | 8 | 1.5883 | 0.563 | 2.7347 | 77 (0.012) |
| Reference asset type | asset | 282 | 6395 | 7 | 1.9918 | 0.423 | 2.1502 | 59 (0.009) |
| Ledger access and permissioning | techn | 2358 | 6330 | 14 | 1.6497 | 0.352 | 3.3813 | 186 (0.029) |
| Issuer identifiability | asset | 81 | 6303 | 6 | 0.8545 | 0.802 | 1.3784 | 4 (0.001) |
| Payment stablecoin / e-money / ART reg | asset | 45 | 6299 | 3 | 1.9305 | 0.478 | 0.7592 | 14 (0.002) |
| Ledger scope: open or closed access by | techn | 392 | 6144 | 5 | 1.5007 | 0.423 | 1.975 | 78 (0.013) |
| Convertible virtual currency (CVC) sta | asset | 106 | 6084 | 1 | 0.1858 | 0.972 | 0.0755 | 56 (0.009) |
| Network topology and node roles | techn | 1121 | 6066 | 7 | 1.1893 | 0.578 | 2.3443 | 118 (0.019) |
| Recording and cryptographic linkage | asset | 2316 | 6028 | 6 | 0.1823 | 0.972 | 1.7912 | 544 (0.09) |
| Consensus mechanism | techn | 1280 | 5915 | 6 | 1.7462 | 0.415 | 2.3746 | 227 (0.038) |
| Validator reward mechanism | techn | 229 | 5688 | 4 | 0.4952 | 0.913 | 1.1511 | 46 (0.008) |
| Transaction fee regime | techn | 79 | 5642 | 2 | 1.9442 | 0.512 | 0.0942 | 15 (0.003) |
| Native asset presence and type | techn | 218 | 5627 | 4 | 0.9029 | 0.812 | 1.3173 | 39 (0.007) |
| Software architecture (monolithic vs p | techn | 204 | 5571 | 5 | 0.819 | 0.745 | 2.0926 | 31 (0.006) |
| Ledger storage model (what is stored o | techn | 852 | 5534 | 3 | 1.1867 | 0.728 | 1.5017 | 139 (0.025) |
| Ledger purpose | techn | 4890 | 4890 | 0 | 2.1684 | 0.314 | -0.0 | 4890 (1.0) |
| DLT data structure (blockchain vs non- | techn | 2377 | 4212 | 4 | 0.2535 | 0.965 | 1.5929 | 1511 (0.359) |
| Node / DLT network node role | techn | 897 | 2910 | 1 | 2.0924 | 0.377 | 0.7931 | 695 (0.239) |
| Decentralised system certification | techn | 138 | 2446 | 2 | 1.4118 | 0.536 | 0.9105 | 78 (0.032) |
| Source code openness | techn | 45 | 2368 | 2 | 0.2623 | 0.956 | 0.3028 | 15 (0.006) |
| Smart contract / distributed ledger ap | techn | 1509 | 2263 | 2 | 1.1725 | 0.592 | 1.4515 | 493 (0.218) |
| Information and communications technol | techn | 90 | 2215 | 3 | 0.307 | 0.945 | 1.5818 | 64 (0.029) |
| Identity layer and onboarding | techn | 873 | 2150 | 3 | 0.7019 | 0.81 | 1.6298 | 336 (0.156) |
| Redemption mechanism | asset | 52 | 1555 | 4 | 1.6533 | 0.611 | 1.6562 | 14 (0.009) |
| Form of holder claim | asset | 57 | 1541 | 4 | 1.509 | 0.474 | 1.633 | 16 (0.01) |
| Smart contract usage domain | techn | 1347 | 1347 | 0 | 2.4907 | 0.261 | -0.0 | 1347 (1.0) |
| Source of yield | asset | 91 | 1045 | 1 | 1.3347 | 0.484 | 0.3171 | 60 (0.057) |
| Data classification (traffic, content, | techn | 2 | 1044 | 1 | -0.0 | 1.0 | 0.011 | 1 (0.001) |
| Privacy and anonymity features | techn | 571 | 1043 | 2 | 0.7554 | 0.832 | 1.2995 | 340 (0.326) |
| Identity binding mechanism | techn | 994 | 994 | 0 | 2.3137 | 0.407 | -0.0 | 994 (1.0) |
| Yield distribution mechanism | asset | 12 | 985 | 1 | 1.2075 | 0.75 | 0.0609 | 7 (0.007) |
| Centralisation of control | asset | 678 | 978 | 2 | 1.4988 | 0.44 | 1.0143 | 632 (0.646) |
| Tokenisation form | asset | 334 | 702 | 2 | 0.9553 | 0.624 | 1.1795 | 231 (0.329) |
| Smart contract / script language expre | techn | 379 | 669 | 2 | 0.9399 | 0.803 | 1.5308 | 309 (0.462) |
| Crypto-asset service provider or VASP  | actor | 190 | 656 | 16 | 1.719 | 0.626 | 3.498 | 118 (0.18) |
| Fungibility | asset | 446 | 649 | 1 | 0.6757 | 0.822 | 0.8475 | 178 (0.274) |
| Privacy mechanism family | techn | 613 | 613 | 0 | 1.9398 | 0.558 | -0.0 | 613 (1.0) |
| Offshore VASP status (activity-based o | actor | 0 | 538 | 2 | - | - | 0.9999 | 0 (0.0) |
| Jurisdictional regime and home or host | actor | 18 | 538 | 5 | 1.3472 | 0.611 | 1.6366 | 13 (0.024) |
| Financial institution status for AML | actor | 5 | 525 | 3 | 0.971 | 0.6 | 0.1887 | 2 (0.004) |
| Principal or agent role in transaction | actor | 28 | 523 | 8 | 1.8288 | 0.357 | 2.1285 | 15 (0.029) |
| Custody model | actor | 129 | 508 | 6 | 1.8137 | 0.366 | 2.3198 | 74 (0.146) |
| Native asset versus token standard | asset | 440 | 471 | 1 | 1.3107 | 0.58 | 0.4408 | 428 (0.909) |
| Trading venue type | actor | 65 | 419 | 1 | 1.4985 | 0.627 | 0.5477 | 53 (0.126) |
| Crypto-asset service type | activ | 254 | 370 | 9 | 2.2844 | 0.449 | 3.0276 | 177 (0.478) |
| Control or sufficient influence over D | actor | 20 | 366 | 3 | 0.971 | 0.6 | 1.0144 | 12 (0.033) |
| Ledger partitioning or layering topolo | techn | 340 | 340 | 0 | 2.0333 | 0.275 | -0.0 | 340 (1.0) |
| Hosted versus unhosted (self-hosted) w | asset | 334 | 334 | 0 | 1.0651 | 0.613 | -0.0 | 334 (1.0) |
| Infrastructure provider type | actor | 23 | 309 | 2 | 0.9961 | 0.8 | 0.806 | 16 (0.052) |
| Ecosystem participant role | actor | 239 | 293 | 4 | 2.077 | 0.388 | 1.6091 | 235 (0.802) |
| Interoperability and intraoperability | techn | 203 | 203 | 0 | 1.6864 | 0.502 | -0.0 | 203 (1.0) |
| Transfer of crypto-assets (travel rule | activ | 57 | 193 | 8 | -0.0 | 1.0 | 2.8625 | 40 (0.207) |
| Smart contract deployment context | techn | 161 | 161 | 0 | 1.9758 | 0.479 | -0.0 | 161 (1.0) |
| Money transmission (acceptance and tra | activ | 8 | 153 | 5 | 0.5436 | 0.875 | 2.1307 | 6 (0.039) |
| Public offer or private placement | activ | 16 | 147 | 3 | 0.8343 | 0.824 | 1.2649 | 5 (0.034) |
| Finality of agreement | techn | 143 | 143 | 0 | 0.8796 | 0.701 | -0.0 | 143 (1.0) |
| Offer and issuance method (token distr | activ | 43 | 142 | 3 | 1.2405 | 0.721 | 1.9543 | 36 (0.254) |
| Anti-money laundering obligations | oblig | 69 | 136 | 9 | 0.9242 | 0.729 | 2.3506 | 23 (0.169) |
| Virtual assets as property or proceeds | oblig | 1 | 113 | 7 | -0.0 | 1.0 | 1.9771 | 0 (0.0) |
| Permitted control over client assets ( | actor | 54 | 112 | 2 | 0.7889 | 0.764 | 1.4742 | 49 (0.438) |
| Freezing and blocking capability | oblig | 8 | 105 | 4 | 0.8113 | 0.75 | 1.2019 | 4 (0.038) |
| Wallet storage mode (hot or cold) | techn | 98 | 98 | 0 | 0.999 | 0.519 | -0.0 | 98 (1.0) |
| Illicit finance risk category | oblig | 82 | 98 | 2 | 1.3325 | 0.472 | 1.0034 | 64 (0.653) |
| Peer-to-peer (P2P) transaction | activ | 18 | 62 | 1 | 0.2975 | 0.947 | 0.7982 | 15 (0.242) |
| Stablecoin issuer model | actor | 2 | 58 | 1 | 1.0 | 0.5 | 0.2164 | 2 (0.034) |
| Operator of crypto-asset arrangement | actor | 11 | 56 | 2 | 0.994 | 0.545 | 0.7147 | 11 (0.196) |
| Payment service and funds transfer | activ | 31 | 47 | 1 | -0.0 | 1.0 | 0.9971 | 25 (0.532) |
| Asset supply management (monetary poli | techn | 46 | 46 | 0 | 1.2717 | 0.717 | -0.0 | 46 (1.0) |
| Central bank digital currency status | asset | 45 | 45 | 0 | 0.971 | 0.6 | -0.0 | 45 (1.0) |
| Validator operation capacity (who may  | actor | 45 | 45 | 0 | 0.7156 | 0.844 | -0.0 | 45 (1.0) |
| Staking arrangement (self, delegated,  | activ | 12 | 44 | 1 | 1.8262 | 0.385 | 0.8113 | 11 (0.25) |
| Wrapped / cross-chain representation | asset | 43 | 43 | 0 | 0.9965 | 0.535 | -0.0 | 43 (1.0) |
| Anonymity-enhancing crypto-asset statu | oblig | 34 | 34 | 0 | 0.874 | 0.706 | -0.0 | 34 (1.0) |
| Minting mechanism | activ | 33 | 33 | 0 | 2.4105 | 0.306 | -0.0 | 33 (1.0) |
| Nexus to jurisdiction (services offere | activ | 22 | 22 | 0 | -0.0 | 1.0 | -0.0 | 22 (1.0) |
| Address linkage to service provider | actor | 5 | 18 | 1 | 0.971 | 0.6 | 0.8524 | 5 (0.278) |
| Investment contract (Howey) criteria | oblig | 5 | 15 | 3 | 0.7219 | 0.8 | 1.9532 | 5 (0.333) |
| Security status of digital asset (US e | oblig | 1 | 15 | 2 | -0.0 | 1.0 | 0.9321 | 0 (0.0) |
| MiFID financial instrument status | oblig | 0 | 15 | 2 | - | - | 1.0 | 0 (0.0) |
| Excluded instrument category (EU scope | oblig | 0 | 15 | 4 | - | - | 1.9211 | 0 (0.0) |
| Originator and beneficiary role | actor | 3 | 13 | 1 | 0.971 | 0.6 | 0.7793 | 3 (0.231) |
| Ancillary asset and network token stat | asset | 12 | 12 | 0 | 1.0 | 0.5 | -0.0 | 12 (1.0) |
| Consumer or retail versus professional | actor | 10 | 10 | 1 | -0.0 | 1.0 | -0.0 | 10 (1.0) |
| Reference currency for stablecoin peg  | asset | 9 | 9 | 0 | 0.7642 | 0.778 | -0.0 | 9 (1.0) |
| Redemption and reserve adequacy | oblig | 2 | 8 | 4 | -0.0 | 1.0 | 2.2464 | 2 (0.25) |
| Yield or interest on stablecoin | oblig | 0 | 8 | 2 | - | - | 0.9183 | 0 (0.0) |
| Settlement finality and legal enforcea | oblig | 2 | 6 | 3 | -0.0 | 1.0 | 1.9502 | 2 (0.333) |
| Exemption from MSB status | oblig | 1 | 6 | 2 | -0.0 | 1.0 | 1.2516 | 1 (0.167) |
| Safeguarding and custody obligation | oblig | 4 | 4 | 0 | -0.0 | 1.0 | -0.0 | 4 (1.0) |
| ICT and operational resilience risk | oblig | 0 | 4 | 1 | - | - | -0.0 | 0 (0.0) |
| Prudential classification group (Basel | oblig | 0 | 4 | 1 | - | - | -0.0 | 0 (0.0) |
| Traditional finance analogue | oblig | 0 | 4 | 1 | - | - | -0.0 | 0 (0.0) |
| Pooled investment vehicle structure | actor | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Serious crime threshold for predicate  | oblig | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Tax reporting obligation status (CARF) | oblig | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |

## Maintenance proposals

**Dormant nodes (1)**, no items in this batch: `related_person_affiliation`

**Collapsed nodes (11)**, many items but one value absorbs them (merge or re-split candidates):
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 2377 items, dominance 0.965 (blockchain (chain of blocks))
- Source code openness `code_license_openness`: 45 items, dominance 0.956 (open source)
- Validator reward mechanism `reward_mechanism`: 229 items, dominance 0.913 (lump-sum reward)
- Peer-to-peer (P2P) transaction `transaction_type_p2p`: 18 items, dominance 0.947 (person-to-person transfer)
- Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`: 57 items, dominance 1.0 (transfer of crypto-assets (covered))
- Payment service and funds transfer `payment_or_transfer_service`: 31 items, dominance 1.0 (transfer of funds)
- Convertible virtual currency (CVC) status `convertible_virtual_currency_status`: 106 items, dominance 0.972 (convertible virtual currency (CVC))
- Recording and cryptographic linkage `digital_asset_recording`: 2316 items, dominance 0.972 (recorded on cryptographically secured distributed ledger)
- Information and communications technology system `ict_system_scope`: 90 items, dominance 0.945 (ICT / computer system)
- Consumer or retail versus professional user `consumer_vs_professional_status`: 10 items, dominance 1.0 (retail holder / consumer)
- Nexus to jurisdiction (services offered in jurisdiction) `service_location_nexus`: 22 items, dominance 1.0 (services offered to residents or customers in jurisdiction)

**Highest-gain nodes**:
- Crypto-asset service provider or VASP status `service_provider_status`: 3.498 bits over 656 items
- Ledger access and permissioning `ledger_access_permission`: 3.3813 bits over 6330 items
- Crypto-asset service type `crypto_asset_service_type`: 3.0276 bits over 370 items
- Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`: 2.8625 bits over 193 items
- Governance model of a DLT system `governance_model`: 2.7347 bits over 6407 items
- Economic function of the asset `crypto_asset_function`: 2.7319 bits over 6612 items
- Legal classification of crypto-asset `legal_classification_status`: 2.6492 bits over 6419 items
- Crypto-asset definitional criteria `crypto_asset_scope_criteria`: 2.3748 bits over 6706 items

**Discovery targets (32)**, residual >= threshold:
- Ledger purpose `ledger_purpose`: 4890 residual of 4890 (1.0)
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 1511 residual of 4212 (0.359)
- Smart contract usage domain `smart_contract_usage_domain`: 1347 residual of 1347 (1.0)
- Identity binding mechanism `identity_binding_mechanism`: 994 residual of 994 (1.0)
- Centralisation of control `centralisation_level`: 632 residual of 978 (0.646)
- Privacy mechanism family `privacy_mechanism_family`: 613 residual of 613 (1.0)
- Native asset versus token standard `native_vs_token_standard`: 428 residual of 471 (0.909)
- Privacy and anonymity features `privacy_enhancement`: 340 residual of 1043 (0.326)
- Ledger partitioning or layering topology `ledger_partitioning_topology`: 340 residual of 340 (1.0)
- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`: 334 residual of 334 (1.0)
- Smart contract / script language expressiveness `script_language_expressiveness`: 309 residual of 669 (0.462)
- Ecosystem participant role `ecosystem_participant_role`: 235 residual of 293 (0.802)
- Tokenisation form `tokenisation_form`: 231 residual of 702 (0.329)
- Interoperability and intraoperability `interoperability_type`: 203 residual of 203 (1.0)
- Crypto-asset service type `crypto_asset_service_type`: 177 residual of 370 (0.478)
- Smart contract deployment context `smart_contract_deployment_context`: 161 residual of 161 (1.0)
- Finality of agreement `consensus_finality`: 143 residual of 143 (1.0)
- Wallet storage mode (hot or cold) `wallet_type_storage`: 98 residual of 98 (1.0)
- Illicit finance risk category `risk_type_illicit_finance`: 64 residual of 98 (0.653)
- Permitted control over client assets (unilateral vs multi-party control) `unhosted_custody_control_policy`: 49 residual of 112 (0.438)
- Asset supply management (monetary policy) `asset_supply_policy`: 46 residual of 46 (1.0)
- Central bank digital currency status `central_bank_digital_currency`: 45 residual of 45 (1.0)
- Validator operation capacity (who may run a node) `consensus_participant_validator_capacity`: 45 residual of 45 (1.0)
- Wrapped / cross-chain representation `wrapped_or_bridged_asset`: 43 residual of 43 (1.0)
- Anonymity-enhancing crypto-asset status `anonymity_enhancing_status`: 34 residual of 34 (1.0)
- Minting mechanism `minting_mechanism`: 33 residual of 33 (1.0)
- Payment service and funds transfer `payment_or_transfer_service`: 25 residual of 47 (0.532)
- Nexus to jurisdiction (services offered in jurisdiction) `service_location_nexus`: 22 residual of 22 (1.0)
- Ancillary asset and network token status `ancillary_asset_status`: 12 residual of 12 (1.0)
- Consumer or retail versus professional user `consumer_vs_professional_status`: 10 residual of 10 (1.0)
- Reference currency for stablecoin peg (currency vs other) `native_vs_stable_price_reference_asset_currency`: 9 residual of 9 (1.0)
- Investment contract (Howey) criteria `investment_contract_howey`: 5 residual of 15 (0.333)

## Discovery (Task E) candidates

- [ACCEPTED] at `wrapped_or_bridged_asset`: new child_term_type **Cross-chain transfer mechanism** — The mechanism by which an asset is transferred or represented between two blockchains. (supports 8 of 40 shown, est. 9 of 43 residual, gain 0.7401 bits, evidence verified); values: lock-and-mint bridge, pegged sidechain, atomic swap / hashlock, cross-chain messaging / relay, token linking or coloured coin
- [ACCEPTED] at `wallet_type_storage`: new child_term_type **Key custody and control model** — Classifies how signing keys are controlled and shared among parties or devices, independent of network connectivity. (supports 7 of 40 shown, est. 17 of 98 residual, gain 0.6656 bits, evidence verified); values: self-custody single key, custodial third party, multi-party or threshold signing, split seed or secret sharing
- [ACCEPTED] at `ledger_purpose`: new value **supply chain traceability and product provenance** — Ledger used to record and trace the movement or origin of physical goods through a supply chain. (supports 6 of 40 shown, est. 734 of 4890 residual, gain 0.6101 bits, evidence verified)
- [ACCEPTED] at `ledger_purpose`: new value **educational credential and achievement verification** — Ledger used to issue, store, or verify academic certificates, diplomas, and learning records. (supports 6 of 40 shown, est. 734 of 4890 residual, gain 0.6101 bits, evidence verified)
- [ACCEPTED] at `consensus_finality`: new child_term_type **finality mechanism** — Splits protocols by how transactions become irreversible, which is distinct from whether finality is deterministic or probabilistic. (supports 5 of 40 shown, est. 18 of 143 residual, gain 0.546 bits, evidence verified); values: quorum certificate / BFT voting, longest-chain depth (k-deep confirmation), checkpointing / finalized prefix, no global ordering (causal or asynchronous settlement)
- [ACCEPTED] at `unhosted_vs_hosted_wallet`: new value **hardware-embedded key storage on physical medium** — Keys are held in dedicated hardware (hardware wallet, secure element, or key stored on a physical card or token) rather than in software controlled by a provider or the user's general device. (supports 5 of 40 shown, est. 42 of 334 residual, gain 0.5457 bits, evidence verified)
- [ACCEPTED] at `unhosted_vs_hosted_wallet`: new child_term_type **key isolation from network connectivity** — Refines the wallet's access model by whether signing keys are kept air-gapped or offline versus connected online. (supports 5 of 40 shown, est. 42 of 334 residual, gain 0.5457 bits, evidence verified); values: online/hot (network-connected), offline/cold (air-gapped), hybrid (offline signing with online broadcast)
- [ACCEPTED] at `ledger_purpose`: new value **electronic health and medical record management** — Ledger used to store, share, or audit patient health records and medical supply or waste data. (supports 5 of 40 shown, est. 611 of 4890 residual, gain 0.5434 bits, evidence verified)
- [ACCEPTED] at `identity_binding_mechanism`: new value **decentralised identifiers (DID) resolved via blockchain** — Identity is bound through a DID whose DID document is anchored and resolved on a distributed ledger, including DID-based authentication and credential flows. (supports 5 of 40 shown, est. 124 of 994 residual, gain 0.5429 bits, evidence verified)
- [ACCEPTED] at `smart_contract_usage_domain`: new value **energy trading and grid management** — Smart contracts for peer-to-peer energy trading, demand response, and local energy markets involving prosumers and grid operators. (supports 5 of 40 shown, est. 168 of 1347 residual, gain 0.5428 bits, evidence verified)
- [ACCEPTED] at `smart_contract_usage_domain`: new value **electronic health records and medical data sharing** — Ledger applications for storing, sharing, and governing patient medical records and health data access. (supports 5 of 40 shown, est. 168 of 1347 residual, gain 0.5428 bits, evidence verified)
- [ACCEPTED] at `ledger_partitioning_topology`: new value **sharded chain** — Ledger is split into shards or committees that each process a subset of transactions in parallel. (supports 5 of 40 shown, est. 42 of 340 residual, gain 0.5394 bits, evidence verified)
- [ACCEPTED] at `ledger_partitioning_topology`: new value **tiered parent-child chain hierarchy** — Blockchains arranged in tiers where higher-tier integrity derives from lower-tier chains, with child chains linked to a parent. (supports 5 of 40 shown, est. 42 of 340 residual, gain 0.5394 bits, evidence verified)
- [ACCEPTED] at `wallet_type_storage`: new value **paper or physical token** — Keys or addresses are stored on a physical medium such as paper, a card, or a note. (supports 5 of 40 shown, est. 12 of 98 residual, gain 0.5364 bits, evidence verified)
- [ACCEPTED] at `payment_or_transfer_service`: new child_term_type **payment_settlement_mechanism** — Splits payment-service transactions by how value is settled and reconciled between parties. (supports 5 of 25 shown, est. 5 of 25 residual, gain 0.384 bits, evidence verified); values: on-chain direct settlement, off-chain payment channel, escrow or smart-contract conditional release, fiat conversion and merchant settlement, multi-chain cross-ledger settlement
- [ACCEPTED] at `ecosystem_participant_role`: new value **researcher / evaluator** — Participant whose role is to study, measure, benchmark or assess blockchain systems rather than operate, issue or hold assets. (supports 5 of 40 shown, est. 29 of 235 residual, gain 0.3215 bits, evidence verified)
- [ACCEPTED] at `unhosted_custody_control_policy`: new child_term_type **key_splitting_scheme** — Mechanism by which the private key material is split across shares, shards, or devices (e.g., threshold sharing, MPC, partial keys). (supports 8 of 40 shown, est. 10 of 49 residual, gain 0.3194 bits, evidence verified); values: threshold secret sharing (t-of-n shards), multi-party computation key generation/signing, partial key split across devices or servers, no key splitting (single complete key)
- [ACCEPTED] at `script_language_expressiveness`: new child_term_type **expressiveness claim basis** — Whether the text asserts expressiveness from the platform's design, a patent claim, or only describes the scripting or verification of contracts without stating a class. (supports 5 of 40 shown, est. 39 of 309 residual, gain 0.2511 bits, evidence verified); values: explicitly Turing-complete claim, Turing-incomplete by design, not stated / implicit
- [ACCEPTED] at `unhosted_custody_control_policy`: new value **time-locked or recovery-key control** — Control exercised through time-delayed, recovery, or fallback keys that alter who can move assets under given conditions. (supports 5 of 40 shown, est. 6 of 49 residual, gain 0.2347 bits, evidence verified)
- [ACCEPTED] at `tokenisation_form`: new value **fractional equity or security token** — Token representing fractional ownership, equity, or a security interest in an off-chain asset or enterprise. (supports 5 of 40 shown, est. 29 of 231 residual, gain 0.169 bits, evidence verified)
- [ACCEPTED] at `crypto_asset_service_type`: new child_term_type **key_management_control_model** — Distinguishes how signing keys are held, split, or authorised when a service custodies crypto-assets. (supports 6 of 40 shown, est. 27 of 177 residual, gain 0.1069 bits, evidence verified); values: multi-party computation / threshold signing, hardware security module with approval policy, sharded key distribution, single-party key storage
- [rejected] at `native_vs_stable_price_reference_asset_currency`: new value **fiat-backed digital asset (multi-currency or unspecified fiat)** — Stable-value digital asset whose peg is to fiat currency, where the specific currency is not the referenced jurisdiction's or is left unspecified. (supports 3 of 9 shown, est. 3 of 9 residual, gain 0.9183 bits, evidence verified)
- [rejected] at `consumer_vs_professional_status`: new value **socio-economically disadvantaged or precarious user** — Person engaging with crypto assets out of financial hardship or marginality, seeking income or survival rather than trade or consumption. (supports 3 of 10 shown, est. 3 of 10 residual, gain 0.8813 bits, evidence verified)
- [rejected] at `consumer_vs_professional_status`: new value **unbanked or underbanked user** — Person without access to conventional banking who uses crypto assets as a substitute for bank accounts or payment services. (supports 3 of 10 shown, est. 3 of 10 residual, gain 0.8813 bits, evidence verified)
- [rejected] at `ancillary_asset_status`: new value **governance or utility token** — Digital asset whose primary role is granting governance rights or access to a platform or service, not representing ledger-derived value. (supports 3 of 12 shown, est. 3 of 12 residual, gain 0.8113 bits, evidence verified)
- [rejected] at `ancillary_asset_status`: new child_term_type **asset backing** — Splits assets by whether their value is backed by an external reference such as fiat, commodities, or nothing. (supports 3 of 12 shown, est. 3 of 12 residual, gain 0.8113 bits, evidence verified); values: fiat-collateralised, commodity-backed, unbacked, not applicable
- [rejected] at `service_location_nexus`: new value **services offered to residents of a jurisdiction via a cross-border or remote channel** — Crypto-asset or payment services are provided across borders in a way that engages licensing or AML obligations, but the operator's location is not stated as the basis for the nexus. (supports 4 of 22 shown, est. 4 of 22 residual, gain 0.684 bits, evidence verified)
- [rejected] at `service_location_nexus`: new child_term_type **nexus basis** — Distinguishes the legal hook that ties a crypto-asset service to a jurisdiction, such as customer residence, operator establishment, or product targeting. (supports 4 of 22 shown, est. 4 of 22 residual, gain 0.684 bits, evidence verified); values: customer residence or location, operator establishment or licensing location, targeting of jurisdiction-specific offerings, no stated nexus basis
- [rejected] at `wallet_type_storage`: new value **isolated or air-gapped device** — Keys reside on a dedicated device isolated from networks, such as a hardware signing device or secure enclave, rather than being simply offline. (supports 5 of 40 shown, est. 12 of 98 residual, gain 0.5364 bits, evidence unverified)
- [rejected] at `anonymity_enhancing_status`: new value **transaction-obfuscation service** — Crypto-asset or service that obscures transfer trails via mixing, coinjoin or decoy transactions rather than built-in protocol privacy. (supports 4 of 34 shown, est. 4 of 34 residual, gain 0.5226 bits, evidence verified)
- [rejected] at `anonymity_enhancing_status`: new value **pseudonymous ledger** — Asset whose addresses are pseudonymous and publicly traceable, giving partial but not built-in concealment of transfers. (supports 4 of 34 shown, est. 4 of 34 residual, gain 0.5226 bits, evidence verified)
- [rejected] at `native_vs_token_standard`: new value **NFT standard token (ERC-721/ERC-1155)** — A non-fungible token issued under an NFT smart-contract standard such as ERC-721 or ERC-1155, representing unique items or rights. (supports 5 of 40 shown, est. 54 of 428 residual, gain 0.4969 bits, evidence unverified)
- [rejected] at `native_vs_token_standard`: new child_term_type **Token use-case or economic function** — Classifies the purpose a crypto-asset serves, independent of its technical standard. (supports 5 of 40 shown, est. 54 of 428 residual, gain 0.4969 bits, evidence unverified); values: payment or medium of exchange, investment or security token, unique collectible or digital art, rights, identity or credential token, supply-chain or record-keeping token, governance or utility token
- [rejected] at `asset_supply_policy`: new value **supply reduced by burning or destruction** — Supply is intentionally decreased by permanently destroying existing units, as in burn or deflationary mechanisms. (supports 4 of 40 shown, est. 5 of 46 residual, gain 0.496 bits, evidence verified)
- [rejected] at `asset_supply_policy`: new value **supply adjusted by algorithmic or demand-responsive rule** — Supply expands or contracts dynamically in response to market demand, price, or a monetary target rather than a fixed schedule. (supports 4 of 40 shown, est. 5 of 46 residual, gain 0.496 bits, evidence verified)
- [rejected] at `ledger_partitioning_topology`: new value **main-sidechain pegged chain** — A parent or main chain issues assets and linked side chains operate cooperatively with cross-chain transfers. (supports 4 of 40 shown, est. 34 of 340 residual, gain 0.469 bits, evidence verified)
- [rejected] at `ledger_partitioning_topology`: new value **off-main-chain sub-ledger** — Operations are executed in a separate sub-ledger or off-main ledger layer, with results anchored to the main ledger. (supports 4 of 40 shown, est. 34 of 340 residual, gain 0.469 bits, evidence verified)
- [rejected] at `identity_binding_mechanism`: new child_term_type **DID binding scope** — Splits identity bindings by whether the decentralised identifier is globally unique, pairwise between two parties, or relational between entities. (supports 4 of 40 shown, est. 99 of 994 residual, gain 0.4677 bits, evidence verified); values: global DID, pairwise DID, relational DID
- [rejected] at `smart_contract_deployment_context`: new value **digital content / NFT / commerce** — Smart contracts deployed for NFTs, digital asset transfer, online marketplaces, crowdfunding, and payments. (supports 4 of 40 shown, est. 16 of 161 residual, gain 0.467 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **gambling / cybercrime / security analysis** — Smart contracts studied or deployed for gambling, ransomware, attacks, or vulnerability detection. (supports 4 of 40 shown, est. 16 of 161 residual, gain 0.467 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **cross-chain settlement bridge** — Ledger connects to another blockchain via a bridge that locks assets on one chain and mints or releases synthetic equivalents on the other. (supports 4 of 40 shown, est. 20 of 203 residual, gain 0.4643 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **cross-chain smart contract invocation** — A contract on one blockchain is invoked, mirrored, or called from another blockchain without rewriting it. (supports 4 of 40 shown, est. 20 of 203 residual, gain 0.4643 bits, evidence verified)
- [rejected] at `consensus_finality`: new value **conditional (synchrony-dependent) finality** — Settlement is guaranteed only under stated timing or network assumptions, such as partial synchrony or bounded delay. (supports 4 of 40 shown, est. 14 of 143 residual, gain 0.4623 bits, evidence unverified)
- [rejected] at `wrapped_or_bridged_asset`: new value **cross-chain exchange / atomic-swap asset** — Asset that is exchanged between chains through escrow or swap rather than wrapped as a durable representation. (supports 4 of 40 shown, est. 4 of 43 residual, gain 0.4465 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **metric-based performance-reward minting** — New units are minted as rewards tied to measured off-chain or on-chain performance, activity, or verified participation metrics rather than consensus or collateral. (supports 3 of 33 shown, est. 3 of 33 residual, gain 0.4395 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **bridge lock-and-mint of synthetic assets** — Synthetic representations are minted on a destination chain against native assets locked by a cross-chain bridge program or warden pool. (supports 3 of 33 shown, est. 3 of 33 residual, gain 0.4395 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **NFT minting of digital collectibles or certificates** — Non-fungible tokens are created on demand to represent collectibles, warranties, or content rights, without a monetary or consensus role. (supports 3 of 33 shown, est. 3 of 33 residual, gain 0.4395 bits, evidence unverified)
- [rejected] at `central_bank_digital_currency`: new child_term_type **CBDC design model** — Splits CBDC proposals by whether the central bank money is accessible to the general public or restricted to financial institutions. (supports 4 of 40 shown, est. 4 of 45 residual, gain 0.4328 bits, evidence verified); values: retail CBDC, wholesale CBDC
- [rejected] at `consensus_participant_validator_capacity`: new child_term_type **validator admission mechanism** — Distinguishes how a candidate node is granted validator status once it is willing to operate. (supports 4 of 40 shown, est. 4 of 45 residual, gain 0.4328 bits, evidence verified); values: registration by authorised signer, governance or epoch-based vote, stake or masternode collateral, position or reputation proof
- [rejected] at `privacy_mechanism_family`: new value **zk-STARK proofs** — Transparent zero-knowledge proof system based on hash functions and FRI, avoiding trusted setup, distinct from zk-SNARKs. (supports 3 of 40 shown, est. 46 of 613 residual, gain 0.3845 bits, evidence verified)
- [rejected] at `privacy_mechanism_family`: new value **ring signature** — Signature scheme where a signer hides identity within a set of possible signers, providing signer anonymity. (supports 3 of 40 shown, est. 46 of 613 residual, gain 0.3845 bits, evidence verified)
- [rejected] at `privacy_mechanism_family`: new value **trusted execution environment (TEE)** — Hardware-isolated enclave that executes computation confidentially so inputs and state remain hidden from the host. (supports 3 of 40 shown, est. 46 of 613 residual, gain 0.3845 bits, evidence verified)
- [rejected] at `smart_contract_usage_domain`: new value **insurance claims processing** — Blockchain applications that automate, verify, or audit insurance claim submission, approval, and payment. (supports 3 of 40 shown, est. 101 of 1347 residual, gain 0.3842 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **oracle-mediated external data access** — Ledger obtains off-chain or external-world state through oracle services that feed data to on-chain contracts. (supports 3 of 40 shown, est. 15 of 203 residual, gain 0.3803 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **domain-name-based cross-chain resolution** — Blockchain instances are addressed and reached through unique blockchain domain names resolved by relays. (supports 3 of 40 shown, est. 15 of 203 residual, gain 0.3803 bits, evidence verified)
- [rejected] at `consensus_participant_validator_capacity`: new value **trusted execution environment attested node** — Node eligibility is gated by hardware-attested trusted execution environment (TEE) proof rather than open stake or pre-selection. (supports 3 of 40 shown, est. 3 of 45 residual, gain 0.3534 bits, evidence verified)
- [rejected] at `consensus_participant_validator_capacity`: new value **permissioned signer-registered validator** — Validators are admitted only after registration or signature by an authorised signer or identity authority recorded on the ledger. (supports 3 of 40 shown, est. 3 of 45 residual, gain 0.3534 bits, evidence verified)
- [rejected] at `payment_or_transfer_service`: new value **merchant acceptance or checkout of crypto-asset payment** — Transaction in which a merchant accepts a crypto-asset payment, typically at checkout or point of sale, possibly converting to fiat. (supports 4 of 25 shown, est. 4 of 25 residual, gain 0.3374 bits, evidence verified)
- [rejected] at `centralisation_level`: new child_term_type **Governance and control mechanism** — Describes the concrete mechanism by which control over the asset's critical functions is exercised, distinct from who holds it. (supports 4 of 40 shown, est. 63 of 632 residual, gain 0.3024 bits, evidence verified); values: admin key or owner privilege, multisig or council, token-holder voting (DAO), no central control
- [rejected] at `centralisation_level`: new value **issuer-controlled (permissioned authority)** — Asset whose issuance and redemption are controlled by a designated authority such as a central bank or licensed issuer, rather than by a single firm or by protocol rules. (supports 4 of 40 shown, est. 63 of 632 residual, gain 0.3024 bits, evidence verified)
- [rejected] at `risk_type_illicit_finance`: new value **money laundering via mixing services** — Risk that crypto-asset activity is used to layer or conceal illicit proceeds through laundering or wash-trading schemes. (supports 4 of 40 shown, est. 6 of 64 residual, gain 0.2902 bits, evidence verified)
- [rejected] at `risk_type_illicit_finance`: new value **wallet-level criminal association scoring** — Risk assessed by scoring a wallet or address's propensity for criminal or suspicious activity via taint or association. (supports 4 of 40 shown, est. 6 of 64 residual, gain 0.2902 bits, evidence verified)
- [rejected] at `ledger_purpose`: new value **counterfeit detection and anti-fraud authentication of goods or transactions** — Ledger used to detect counterfeit products or fraudulent events such as phone fraud or traffic violation tampering. (supports 2 of 40 shown, est. 244 of 4890 residual, gain 0.286 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **energy trading / smart grid** — Smart contracts deployed for peer-to-peer energy trading, distributed energy resources, and smart grid transactions. (supports 2 of 40 shown, est. 8 of 161 residual, gain 0.2851 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **transportation / mobility** — Smart contracts deployed for transportation systems, vehicles, and mobility services. (supports 2 of 40 shown, est. 8 of 161 residual, gain 0.2851 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **end user / community member** — Individual participant using or engaging with crypto-assets for livelihood, social or personal purposes, including ethnographic subjects. (supports 3 of 40 shown, est. 18 of 235 residual, gain 0.2327 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **oracle / data provider** — Participant that supplies off-chain data or attestations to smart contracts or ledgers. (supports 3 of 40 shown, est. 18 of 235 residual, gain 0.2327 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **custodian / intermediary** — Participant that holds, safeguards or intermediates assets or orders on behalf of others. (supports 3 of 40 shown, est. 18 of 235 residual, gain 0.2327 bits, evidence verified)
- [rejected] at `script_language_expressiveness`: new value **new programming language for DLT** — Ledger scripting uses a newly designed or intermediate language (e.g., Albert, Michelson-targeted, Protean) rather than an existing general-purpose language. (supports 4 of 40 shown, est. 31 of 309 residual, gain 0.2158 bits, evidence verified)
- [rejected] at `investment_contract_howey`: new value **investment contract (portfolio asset)** — Crypto-asset treated as an individual investment or diversification component within a traditional portfolio, without a described common enterprise or managerial efforts. (supports 3 of 5 shown, est. 3 of 5 residual, gain 0.2111 bits, evidence verified)
- [rejected] at `script_language_expressiveness`: new value **script chunking / decomposition of transaction logic** — Expressiveness is extended by splitting transaction script functionality across multiple chunks or transactions on a restricted-script ledger. (supports 3 of 40 shown, est. 23 of 309 residual, gain 0.1755 bits, evidence verified)
- [rejected] at `dlt_architecture`: new value **mutable/rewritable blockchain** — A blockchain variant whose stored blocks or payloads can be edited or replaced under defined conditions, relaxing strict immutability. (supports 4 of 40 shown, est. 151 of 1511 residual, gain 0.1626 bits, evidence verified)
- [rejected] at `dlt_architecture`: new value **DAG-based (site or transaction graph)** — A DAG ledger where units of data (sites or transactions) reference multiple predecessors rather than a single linear chain of blocks. (supports 4 of 40 shown, est. 151 of 1511 residual, gain 0.1626 bits, evidence verified)
- [rejected] at `privacy_enhancement`: new value **blockchain clustering / transaction-graph deanonymisation** — Techniques that infer linked addresses or entities by analysing the public transaction graph, undermining obfuscation of the ledger. (supports 4 of 40 shown, est. 34 of 340 residual, gain 0.1517 bits, evidence verified)
- [rejected] at `privacy_enhancement`: new value **tumbler / mixing service overlay** — Third-party or coordinated mixing services that break the link between input and output coins to hide fund flows. (supports 4 of 40 shown, est. 34 of 340 residual, gain 0.1517 bits, evidence verified)
- [rejected] at `privacy_enhancement`: new value **off-chain transaction exchange before broadcast** — Obfuscation achieved by exchanging or relaying transactions off-chain before network diffusion to hide originating IP or address. (supports 4 of 40 shown, est. 34 of 340 residual, gain 0.1517 bits, evidence verified)
- [rejected] at `tokenisation_form`: new child_term_type **off-chain asset class** — Classifies the type of real-world or off-chain asset that a tokenised representation refers to. (supports 4 of 40 shown, est. 23 of 231 residual, gain 0.145 bits, evidence unverified); values: real estate or land, precious metal or commodity, energy or environmental attribute, intellectual property, financial instrument or loan, physical good or collectible
- [rejected] at `tokenisation_form`: new value **natural resource or commodity right token** — Token representing rights to explore, produce, mine, or harvest a natural resource, or ownership of an unrefined or pre-commodity asset. (supports 3 of 40 shown, est. 17 of 231 residual, gain 0.1176 bits, evidence verified)
- [rejected] at `crypto_asset_service_type`: new child_term_type **trading_venue_model** — Distinguishes centralised order-book exchanges, decentralised on-chain exchanges, and automated market makers used to execute crypto-asset trades. (supports 5 of 40 shown, est. 22 of 177 residual, gain 0.094 bits, evidence verified); values: centralised exchange, decentralised on-chain exchange, automated market maker, peer-to-peer matching
- [rejected] at `crypto_asset_service_type`: new child_term_type **fiat_crypto_conversion_route** — Distinguishes how fiat-to-crypto or crypto-to-fiat conversion is settled, such as via banks, secondary ledgers, or payment orchestration platforms. (supports 5 of 40 shown, est. 22 of 177 residual, gain 0.094 bits, evidence verified); values: bank-integrated conversion, secondary blockchain settlement, third-party payment orchestration, direct exchange conversion
- [rejected] at `crypto_asset_service_type`: new value **account freezing / resource transfer denial** — Service that freezes, blocks, or denies transfer of a user's account or crypto-asset resources. (supports 3 of 40 shown, est. 13 of 177 residual, gain 0.0657 bits, evidence verified)