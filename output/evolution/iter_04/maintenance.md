# Part 2 maintenance: the DAG as label space

8646 tagged items placed on 113/113 nodes (35952 tags, 160157 closure placements).

## Objectives: content-driven vs Part 1 prior

| metric | from tags (empirical) | from is-a weights (Part 1) |
|---|---|---|
| bits per descent (information gain) | 7.2153 | 4.8767 |
| AUC of reach-a-leaf | 0.7796 | 0.8427 |
| expected depth | 3.8027 | 2.8591 |
| effective leaves | 24.68 | 23.087 |
| effective leaves / nodes | 0.2184 | 0.2043 |

## Where descents stop (top stop mass)

- Ledger purpose `ledger_purpose`: 0.2177
- Smart contract usage domain `smart_contract_usage_domain`: 0.0934
- Native asset versus token standard `native_vs_token_standard`: 0.077
- Key custody and control model `key_custody_control_model`: 0.0479
- Privacy mechanism family `privacy_mechanism_family`: 0.0439
- Identity binding mechanism `identity_binding_mechanism`: 0.0397
- Interoperability and intraoperability `interoperability_type`: 0.0376
- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`: 0.0338
- Centralisation of control `centralisation_level`: 0.0328
- Smart contract / script language expressiveness `script_language_expressiveness`: 0.0284
- Tokenisation form `tokenisation_form`: 0.0273
- Privacy and anonymity features `privacy_enhancement`: 0.0256
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 0.0252
- Smart contract / distributed ledger application scope `smart_contract_definition_scope`: 0.0249
- Recording and cryptographic linkage `digital_asset_recording`: 0.0221

## Node statistics (nodes with items, by closure size)

| node | cat | direct | closure | children | value entropy | dominance | branching gain | residual |
|---|---|---|---|---|---|---|---|---|
| Crypto-asset definitional criteria | asset | 720 | 6793 | 10 | 1.0137 | 0.607 | 2.3832 | 73 (0.011) |
| Economic function of the asset | asset | 1172 | 6720 | 9 | 1.26 | 0.708 | 2.743 | 234 (0.035) |
| Legal classification of crypto-asset | asset | 106 | 6486 | 11 | 1.0177 | 0.697 | 2.6649 | 31 (0.005) |
| Reference asset type | asset | 272 | 6453 | 7 | 2.0128 | 0.448 | 2.1833 | 61 (0.009) |
| Governance model of a DLT system | techn | 613 | 6438 | 8 | 1.7085 | 0.504 | 2.7706 | 95 (0.015) |
| Issuer identifiability | asset | 67 | 6370 | 6 | 0.7395 | 0.851 | 1.4126 | 4 (0.001) |
| Payment stablecoin / e-money / ART reg | asset | 38 | 6366 | 3 | 2.0374 | 0.421 | 0.7641 | 4 (0.001) |
| Ledger access and permissioning | techn | 1979 | 6343 | 14 | 1.6176 | 0.394 | 3.4354 | 152 (0.024) |
| Ledger scope: open or closed access by | techn | 437 | 6191 | 5 | 1.494 | 0.429 | 2.0143 | 62 (0.01) |
| Convertible virtual currency (CVC) sta | asset | 78 | 6162 | 1 | 0.172 | 0.974 | 0.0541 | 38 (0.006) |
| Network topology and node roles | techn | 1316 | 6129 | 7 | 1.1464 | 0.592 | 2.3937 | 140 (0.023) |
| Recording and cryptographic linkage | asset | 2115 | 6124 | 6 | 0.1955 | 0.97 | 1.8087 | 509 (0.083) |
| Consensus mechanism | techn | 1246 | 5961 | 6 | 1.7021 | 0.456 | 2.3809 | 212 (0.036) |
| Validator reward mechanism | techn | 202 | 5749 | 4 | 0.4253 | 0.931 | 1.172 | 50 (0.009) |
| Transaction fee regime | techn | 89 | 5699 | 2 | 2.0198 | 0.446 | 0.0869 | 10 (0.002) |
| Native asset presence and type | techn | 235 | 5689 | 4 | 1.1027 | 0.672 | 1.3315 | 36 (0.006) |
| Software architecture (monolithic vs p | techn | 196 | 5632 | 5 | 0.8946 | 0.689 | 2.12 | 47 (0.008) |
| Ledger storage model (what is stored o | techn | 828 | 5577 | 3 | 1.2566 | 0.696 | 1.536 | 158 (0.028) |
| Ledger purpose | techn | 5004 | 5004 | 0 | 2.5677 | 0.345 | -0.0 | 5004 (1.0) |
| DLT data structure (blockchain vs non- | techn | 1918 | 4156 | 4 | 0.3038 | 0.956 | 1.8308 | 1095 (0.263) |
| Node / DLT network node role | techn | 761 | 2999 | 1 | 2.0777 | 0.396 | 0.7201 | 597 (0.199) |
| Decentralised system certification | techn | 95 | 2658 | 2 | 1.495 | 0.495 | 0.8794 | 60 (0.023) |
| Source code openness | techn | 32 | 2598 | 2 | -0.0 | 1.0 | 0.6031 | 18 (0.007) |
| Information and communications technol | techn | 59 | 2402 | 3 | 0.2136 | 0.966 | 1.5529 | 38 (0.016) |
| Identity layer and onboarding | techn | 842 | 2364 | 3 | 0.5982 | 0.855 | 1.7334 | 280 (0.118) |
| Smart contract / distributed ledger ap | techn | 1423 | 2321 | 2 | 1.1714 | 0.602 | 1.3931 | 392 (0.169) |
| Redemption mechanism | asset | 37 | 1688 | 4 | 1.8098 | 0.486 | 1.6692 | 9 (0.005) |
| Form of holder claim | asset | 46 | 1679 | 4 | 1.5362 | 0.413 | 1.669 | 11 (0.007) |
| Smart contract usage domain | techn | 1471 | 1471 | 0 | 2.8298 | 0.277 | -0.0 | 1471 (1.0) |
| Identity binding mechanism | techn | 1200 | 1200 | 0 | 2.4696 | 0.433 | -0.0 | 1200 (1.0) |
| Privacy and anonymity features | techn | 514 | 1171 | 2 | 0.9933 | 0.753 | 1.5284 | 311 (0.266) |
| Data classification (traffic, content, | techn | 2 | 1171 | 1 | -0.0 | 1.0 | -0.0 | 0 (0.0) |
| Source of yield | asset | 67 | 1053 | 1 | 1.4461 | 0.457 | 0.2673 | 48 (0.046) |
| Yield distribution mechanism | asset | 10 | 1005 | 1 | 0.9219 | 0.8 | 0.0599 | 7 (0.007) |
| Centralisation of control | asset | 664 | 998 | 2 | 1.5325 | 0.437 | 1.0449 | 625 (0.626) |
| Tokenisation form | asset | 509 | 848 | 3 | 2.1754 | 0.279 | 1.4643 | 368 (0.434) |
| Smart contract / script language expre | techn | 406 | 744 | 4 | 0.8112 | 0.849 | 1.7363 | 302 (0.406) |
| Fungibility | asset | 394 | 653 | 1 | 0.6605 | 0.829 | 0.8739 | 192 (0.294) |
| Privacy mechanism family | techn | 569 | 570 | 1 | 1.9544 | 0.563 | 0.3399 | 534 (0.937) |
| Crypto-asset service provider or VASP  | actor | 140 | 561 | 16 | 1.734 | 0.629 | 3.5479 | 92 (0.164) |
| Ledger partitioning or layering topolo | techn | 547 | 547 | 0 | 2.4549 | 0.265 | -0.0 | 547 (1.0) |
| Crypto-asset service type | activ | 270 | 537 | 10 | 2.2382 | 0.442 | 3.1785 | 156 (0.291) |
| Offshore VASP status (activity-based o | actor | 0 | 469 | 2 | - | - | 0.9999 | 0 (0.0) |
| Jurisdictional regime and home or host | actor | 17 | 469 | 5 | 1.2533 | 0.529 | 1.7594 | 13 (0.028) |
| Native asset versus token standard | asset | 399 | 461 | 1 | 1.4191 | 0.489 | 0.6407 | 386 (0.837) |
| Financial institution status for AML | actor | 4 | 456 | 3 | 0.8113 | 0.75 | 0.1572 | 1 (0.002) |
| Principal or agent role in transaction | actor | 22 | 455 | 8 | 1.4949 | 0.455 | 2.1056 | 8 (0.018) |
| Custody model | actor | 76 | 447 | 6 | 1.5497 | 0.615 | 2.3551 | 42 (0.094) |
| Trading venue type | actor | 50 | 400 | 1 | 1.5278 | 0.528 | 0.4196 | 34 (0.085) |
| Control or sufficient influence over D | actor | 20 | 366 | 3 | 1.2192 | 0.55 | 1.2316 | 17 (0.046) |
| Hosted versus unhosted (self-hosted) w | asset | 324 | 359 | 2 | 1.3393 | 0.503 | 1.1119 | 272 (0.758) |
| Wallet storage mode (hot or cold) | techn | 129 | 337 | 1 | 1.3409 | 0.551 | 0.7371 | 70 (0.208) |
| Interoperability and intraoperability | techn | 314 | 314 | 0 | 2.382 | 0.413 | -0.0 | 314 (1.0) |
| Transfer of crypto-assets (travel rule | activ | 46 | 303 | 8 | 0.3015 | 0.957 | 2.7743 | 34 (0.112) |
| Money transmission (acceptance and tra | activ | 2 | 269 | 5 | -0.0 | 1.0 | 1.9982 | 2 (0.007) |
| Public offer or private placement | activ | 19 | 267 | 3 | -0.0 | 1.0 | 1.0215 | 6 (0.022) |
| Key custody and control model | techn | 267 | 267 | 0 | 1.3917 | 0.62 | -0.0 | 267 (1.0) |
| Offer and issuance method (token distr | activ | 46 | 261 | 3 | 1.4047 | 0.609 | 1.6606 | 33 (0.126) |
| Infrastructure provider type | actor | 13 | 231 | 2 | -0.0 | 1.0 | 0.8861 | 6 (0.026) |
| Ecosystem participant role | actor | 158 | 225 | 4 | 2.2415 | 0.391 | 1.944 | 150 (0.667) |
| Permitted control over client assets ( | actor | 36 | 193 | 3 | 0.885 | 0.778 | 1.658 | 18 (0.093) |
| Finality of agreement | techn | 178 | 188 | 1 | 0.8694 | 0.709 | 0.4379 | 171 (0.91) |
| Peer-to-peer (P2P) transaction | activ | 20 | 174 | 1 | -0.0 | 1.0 | 0.3401 | 11 (0.063) |
| Payment service and funds transfer | activ | 59 | 163 | 2 | -0.0 | 1.0 | 1.1093 | 24 (0.147) |
| Payment settlement mechanism | activ | 120 | 122 | 1 | 1.9123 | 0.469 | 0.8047 | 92 (0.754) |
| Anti-money laundering obligations | oblig | 52 | 112 | 9 | 1.1103 | 0.685 | 2.4696 | 21 (0.188) |
| Key splitting scheme | techn | 97 | 98 | 1 | 1.8053 | 0.415 | 0.7095 | 79 (0.806) |
| Key management control model | activ | 81 | 97 | 1 | 1.7948 | 0.386 | 0.7136 | 78 (0.804) |
| Virtual assets as property or proceeds | oblig | 1 | 91 | 7 | -0.0 | 1.0 | 2.1313 | 1 (0.011) |
| Smart contract deployment context | techn | 83 | 83 | 0 | 1.9771 | 0.46 | -0.0 | 83 (1.0) |
| Freezing and blocking capability | oblig | 5 | 80 | 4 | 0.7219 | 0.8 | 1.2708 | 4 (0.05) |
| Wrapped / cross-chain representation | asset | 57 | 75 | 1 | 0.998 | 0.526 | 0.9044 | 24 (0.32) |
| Stablecoin issuer model | actor | 0 | 75 | 1 | - | - | -0.0 | 0 (0.0) |
| Operator of crypto-asset arrangement | actor | 11 | 75 | 2 | 0.684 | 0.818 | 0.7383 | 10 (0.133) |
| Illicit finance risk category | oblig | 68 | 73 | 2 | 1.7026 | 0.45 | 1.0553 | 44 (0.603) |
| Validator operation capacity (who may  | actor | 63 | 63 | 0 | 1.1394 | 0.587 | -0.0 | 63 (1.0) |
| Key isolation from network connectivit | techn | 60 | 60 | 0 | 1.3986 | 0.58 | -0.0 | 60 (1.0) |
| Central bank digital currency status | asset | 57 | 57 | 0 | 0.9031 | 0.681 | -0.0 | 57 (1.0) |
| Staking arrangement (self, delegated,  | activ | 10 | 55 | 1 | 1.9219 | 0.4 | 0.684 | 10 (0.182) |
| Cross-chain transfer mechanism | asset | 51 | 51 | 0 | 1.9969 | 0.352 | -0.0 | 51 (1.0) |
| Script verification approach | techn | 51 | 51 | 0 | 1.7264 | 0.397 | -0.0 | 51 (1.0) |
| Asset supply management (monetary poli | techn | 47 | 47 | 0 | 1.1531 | 0.766 | -0.0 | 47 (1.0) |
| Minting mechanism | activ | 45 | 45 | 0 | 2.3487 | 0.422 | -0.0 | 45 (1.0) |
| Key recovery mechanism | techn | 42 | 42 | 0 | 2.2884 | 0.283 | -0.0 | 42 (1.0) |
| Zero-knowledge proof system variant | techn | 36 | 36 | 0 | 0.9739 | 0.811 | -0.0 | 36 (1.0) |
| Fiat-rail integration | activ | 30 | 30 | 0 | 1.4295 | 0.467 | -0.0 | 30 (1.0) |
| Anonymity-enhancing crypto-asset statu | oblig | 28 | 28 | 0 | 0.9464 | 0.786 | -0.0 | 28 (1.0) |
| Backing of token | asset | 25 | 25 | 0 | 0.8905 | 0.692 | -0.0 | 25 (1.0) |
| Nexus to jurisdiction (services offere | activ | 21 | 21 | 0 | 0.857 | 0.81 | -0.0 | 21 (1.0) |
| Key share distribution topology | techn | 19 | 19 | 0 | 1.4577 | 0.45 | -0.0 | 19 (1.0) |
| Address linkage to service provider | actor | 7 | 18 | 1 | 0.9852 | 0.571 | 0.8524 | 5 (0.278) |
| Finality mechanism | techn | 17 | 17 | 0 | 1.659 | 0.529 | -0.0 | 17 (1.0) |
| Ancillary asset and network token stat | asset | 15 | 15 | 0 | 0.9183 | 0.667 | -0.0 | 15 (1.0) |
| Investment contract (Howey) criteria | oblig | 1 | 14 | 3 | -0.0 | 1.0 | 1.6842 | 1 (0.071) |
| Security status of digital asset (US e | oblig | 0 | 14 | 2 | - | - | 0.9457 | 0 (0.0) |
| MiFID financial instrument status | oblig | 0 | 14 | 2 | - | - | 1.0 | 0 (0.0) |
| Excluded instrument category (EU scope | oblig | 0 | 14 | 4 | - | - | 1.9657 | 0 (0.0) |
| Originator and beneficiary role | actor | 6 | 13 | 1 | 1.3222 | 0.545 | 0.9957 | 6 (0.462) |
| Redemption and reserve adequacy | oblig | 0 | 8 | 4 | - | - | 1.8366 | 0 (0.0) |
| Yield or interest on stablecoin | oblig | 0 | 8 | 2 | - | - | 0.8454 | 0 (0.0) |
| Settlement finality and legal enforcea | oblig | 5 | 8 | 3 | -0.0 | 1.0 | 1.9592 | 5 (0.625) |
| Exemption from MSB status | oblig | 0 | 8 | 2 | - | - | 0.9544 | 0 (0.0) |
| Expressiveness claim basis | techn | 8 | 8 | 0 | 0.9544 | 0.625 | -0.0 | 8 (1.0) |
| Consumer or retail versus professional | actor | 5 | 7 | 1 | 0.971 | 0.6 | 0.8631 | 5 (0.714) |
| Reference currency for stablecoin peg  | asset | 5 | 5 | 0 | 0.971 | 0.6 | -0.0 | 5 (1.0) |
| Tax reporting obligation status (CARF) | oblig | 5 | 5 | 0 | -0.0 | 1.0 | -0.0 | 5 (1.0) |
| Safeguarding and custody obligation | oblig | 3 | 3 | 0 | -0.0 | 1.0 | -0.0 | 3 (1.0) |
| ICT and operational resilience risk | oblig | 0 | 3 | 1 | - | - | -0.0 | 0 (0.0) |
| Prudential classification group (Basel | oblig | 0 | 3 | 1 | - | - | -0.0 | 0 (0.0) |
| Traditional finance analogue | oblig | 0 | 3 | 1 | - | - | -0.0 | 0 (0.0) |
| Related person and affiliated person s | actor | 2 | 2 | 0 | -0.0 | 1.0 | -0.0 | 2 (1.0) |
| Pooled investment vehicle structure | actor | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Serious crime threshold for predicate  | oblig | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |

## Maintenance proposals

**Dormant nodes (0)**, no items in this batch: 

**Collapsed nodes (13)**, many items but one value absorbs them (merge or re-split candidates):
- Issuer identifiability `issuer_presence`: 67 items, dominance 0.851 (identifiable issuer)
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 1918 items, dominance 0.956 (blockchain (chain of blocks))
- Source code openness `code_license_openness`: 32 items, dominance 1.0 (open source)
- Identity layer and onboarding `digital_identity_layer`: 842 items, dominance 0.855 (KYC/AML identity layer)
- Validator reward mechanism `reward_mechanism`: 202 items, dominance 0.931 (lump-sum reward)
- Infrastructure provider type `infrastructure_provider_type`: 13 items, dominance 1.0 (oracle)
- Peer-to-peer (P2P) transaction `transaction_type_p2p`: 20 items, dominance 1.0 (person-to-person transfer)
- Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`: 46 items, dominance 0.957 (transfer of crypto-assets (covered))
- Payment service and funds transfer `payment_or_transfer_service`: 59 items, dominance 1.0 (transfer of funds)
- Convertible virtual currency (CVC) status `convertible_virtual_currency_status`: 78 items, dominance 0.974 (convertible virtual currency (CVC))
- Recording and cryptographic linkage `digital_asset_recording`: 2115 items, dominance 0.97 (recorded on cryptographically secured distributed ledger)
- Information and communications technology system `ict_system_scope`: 59 items, dominance 0.966 (ICT / computer system)
- Public offer or private placement `decentralised_or_centralised_offer_model`: 19 items, dominance 1.0 (offer to the public)

**Highest-gain nodes**:
- Crypto-asset service provider or VASP status `service_provider_status`: 3.5479 bits over 561 items
- Ledger access and permissioning `ledger_access_permission`: 3.4354 bits over 6343 items
- Crypto-asset service type `crypto_asset_service_type`: 3.1785 bits over 537 items
- Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`: 2.7743 bits over 303 items
- Governance model of a DLT system `governance_model`: 2.7706 bits over 6438 items
- Economic function of the asset `crypto_asset_function`: 2.743 bits over 6720 items
- Legal classification of crypto-asset `legal_classification_status`: 2.6649 bits over 6486 items
- Anti-money laundering obligations `aml_obligations_applicability`: 2.4696 bits over 112 items

**Discovery targets (42)**, residual >= threshold:
- Ledger purpose `ledger_purpose`: 5004 residual of 5004 (1.0)
- Smart contract usage domain `smart_contract_usage_domain`: 1471 residual of 1471 (1.0)
- Identity binding mechanism `identity_binding_mechanism`: 1200 residual of 1200 (1.0)
- Centralisation of control `centralisation_level`: 625 residual of 998 (0.626)
- Ledger partitioning or layering topology `ledger_partitioning_topology`: 547 residual of 547 (1.0)
- Privacy mechanism family `privacy_mechanism_family`: 534 residual of 570 (0.937)
- Native asset versus token standard `native_vs_token_standard`: 386 residual of 461 (0.837)
- Tokenisation form `tokenisation_form`: 368 residual of 848 (0.434)
- Interoperability and intraoperability `interoperability_type`: 314 residual of 314 (1.0)
- Smart contract / script language expressiveness `script_language_expressiveness`: 302 residual of 744 (0.406)
- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`: 272 residual of 359 (0.758)
- Key custody and control model `key_custody_control_model`: 267 residual of 267 (1.0)
- Finality of agreement `consensus_finality`: 171 residual of 188 (0.91)
- Ecosystem participant role `ecosystem_participant_role`: 150 residual of 225 (0.667)
- Payment settlement mechanism `payment_settlement_mechanism`: 92 residual of 122 (0.754)
- Smart contract deployment context `smart_contract_deployment_context`: 83 residual of 83 (1.0)
- Key splitting scheme `key_splitting_scheme`: 79 residual of 98 (0.806)
- Key management control model `key_management_control_model`: 78 residual of 97 (0.804)
- Validator operation capacity (who may run a node) `consensus_participant_validator_capacity`: 63 residual of 63 (1.0)
- Key isolation from network connectivity `key_isolation_from_network`: 60 residual of 60 (1.0)
- Central bank digital currency status `central_bank_digital_currency`: 57 residual of 57 (1.0)
- Cross-chain transfer mechanism `cross_chain_transfer_mechanism`: 51 residual of 51 (1.0)
- Script verification approach `script_verification_approach`: 51 residual of 51 (1.0)
- Asset supply management (monetary policy) `asset_supply_policy`: 47 residual of 47 (1.0)
- Minting mechanism `minting_mechanism`: 45 residual of 45 (1.0)
- Illicit finance risk category `risk_type_illicit_finance`: 44 residual of 73 (0.603)
- Key recovery mechanism `key_recovery_mechanism`: 42 residual of 42 (1.0)
- Zero-knowledge proof system variant `zk_proof_system_variant`: 36 residual of 36 (1.0)
- Fiat-rail integration `fiat_rail_integration`: 30 residual of 30 (1.0)
- Anonymity-enhancing crypto-asset status `anonymity_enhancing_status`: 28 residual of 28 (1.0)
- Backing of token `backing_of_token`: 25 residual of 25 (1.0)
- Wrapped / cross-chain representation `wrapped_or_bridged_asset`: 24 residual of 75 (0.32)
- Nexus to jurisdiction (services offered in jurisdiction) `service_location_nexus`: 21 residual of 21 (1.0)
- Key share distribution topology `key_share_distribution_topology`: 19 residual of 19 (1.0)
- Finality mechanism `finality_mechanism`: 17 residual of 17 (1.0)
- Ancillary asset and network token status `ancillary_asset_status`: 15 residual of 15 (1.0)
- Expressiveness claim basis `expressiveness_claim_basis`: 8 residual of 8 (1.0)
- Originator and beneficiary role `party_role_transfer`: 6 residual of 13 (0.462)
- Settlement finality and legal enforceability `settlement_finality_legal_test`: 5 residual of 8 (0.625)
- Consumer or retail versus professional user `consumer_vs_professional_status`: 5 residual of 7 (0.714)
- Reference currency for stablecoin peg (currency vs other) `native_vs_stable_price_reference_asset_currency`: 5 residual of 5 (1.0)
- Tax reporting obligation status (CARF) `tax_reporting_status`: 5 residual of 5 (1.0)

## Discovery (Task E) candidates

- [ACCEPTED] at `key_share_distribution_topology`: new value **among blockchain network nodes** — Key shares are held by nodes of a blockchain or decentralized network, such that a threshold of nodes must cooperate to reconstruct the key. (supports 5 of 19 shown, est. 5 of 19 residual, gain 0.8315 bits, evidence verified)
- [ACCEPTED] at `anonymity_enhancing_status`: new child_term_type **Deanonymisation / tracing approach** — Method by which a pseudonymous ledger's transfers are clustered, labelled or attributed to real-world actors by investigators or detectors. (supports 6 of 28 shown, est. 6 of 28 residual, gain 0.7496 bits, evidence verified); values: address clustering heuristic, graph-based machine learning, transaction time-series analysis, wallet risk scoring, argumentation or legal reasoning
- [ACCEPTED] at `backing_of_token`: new value **backed by physical commodities or precious metals** — The token's value is backed by physical commodities, precious metals, gems or other tangible goods held in custody. (supports 5 of 25 shown, est. 5 of 25 residual, gain 0.7219 bits, evidence verified)
- [ACCEPTED] at `backing_of_token`: new child_term_type **backing mechanism** — Distinguishes whether backing assets are held in custody, pledged or locked, or governed by an oracle or algorithm. (supports 5 of 25 shown, est. 5 of 25 residual, gain 0.7219 bits, evidence verified); values: custodial reserve held by third party, pledged or encumbered on a ledger, oracle-priced collateral, algorithmic peg without collateral
- [ACCEPTED] at `fiat_rail_integration`: new value **card-network-issued crypto payment card** — The crypto settlement is triggered by a payment card whose authorization flows through a card network. (supports 5 of 30 shown, est. 5 of 30 residual, gain 0.65 bits, evidence verified)
- [ACCEPTED] at `fiat_rail_integration`: new child_term_type **Settlement counterparty** — Identifies the institution or platform that performs the fiat-side payout, distinct from the crypto-side transfer. (supports 5 of 30 shown, est. 5 of 30 residual, gain 0.65 bits, evidence verified); values: merchant acquirer / bank, payment platform remits fiat, commercial bank node, not applicable
- [ACCEPTED] at `fiat_rail_integration`: new value **ledger-tokenized fiat settlement** — Fiat settlement is replaced by settlement tokens or in-network tokens on a distributed ledger rather than a bridged rail. (supports 5 of 30 shown, est. 5 of 30 residual, gain 0.65 bits, evidence verified)
- [ACCEPTED] at `minting_mechanism`: new value **NFT minting for media and content licensing** — Units minted as NFTs representing a media asset, royalty split, or content authorisation, typically via a marketplace or digital vault. (supports 5 of 40 shown, est. 6 of 45 residual, gain 0.5665 bits, evidence verified)
- [ACCEPTED] at `key_isolation_from_network`: new child_term_type **physical transfer mechanism across air gap** — Distinguishes how signed or key material physically crosses an air gap, which the existing binary-style values do not separate. (supports 5 of 40 shown, est. 8 of 60 residual, gain 0.5665 bits, evidence verified); values: none (fully disconnected), removable storage media, optical/visual codes, acoustic, electrical diode or one-way link
- [ACCEPTED] at `consensus_participant_validator_capacity`: new child_term_type **validator selection mechanism** — Describes how the set of active validators is selected, independent of who is eligible to join. (supports 5 of 40 shown, est. 8 of 63 residual, gain 0.5491 bits, evidence verified); values: random or verifiable-random selection, stake or share weighted selection, reputation based selection, fixed rotation or leader election, all eligible nodes participate
- [ACCEPTED] at `ledger_partitioning_topology`: new child_term_type **sharding partition basis** — Describes what criterion divides the network or state into parallel shards. (supports 5 of 40 shown, est. 68 of 547 residual, gain 0.5416 bits, evidence verified); values: validator/node grouping, account or state partition, transaction-graph or workload-based partition, jurisdiction or location partition
- [ACCEPTED] at `key_custody_control_model`: new value **air-gapped offline signing device** — Private keys are generated and stored on a device never connected to a network, with signing performed offline via QR codes, cards, or isolated chambers. (supports 5 of 40 shown, est. 33 of 267 residual, gain 0.5396 bits, evidence verified)
- [ACCEPTED] at `native_vs_token_standard`: new value **NFT standard token** — Non-fungible token issued under a smart-contract standard, such as ERC-721 or ERC-1155, representing unique assets. (supports 5 of 40 shown, est. 48 of 386 residual, gain 0.4536 bits, evidence verified)
- [ACCEPTED] at `unhosted_vs_hosted_wallet`: new child_term_type **wallet interface or delivery form** — Classifies the physical or software form in which the wallet and its keys are presented to the user. (supports 6 of 40 shown, est. 41 of 272 residual, gain 0.4449 bits, evidence verified); values: software wallet application, physical card or token, physical object (e.g., sphere or coin), hardware device, browser or web extension
- [ACCEPTED] at `key_splitting_scheme`: new child_term_type **Share recovery mechanism** — Distinguishes how split key material is reconstituted, such as threshold reconstruction, escrow recovery, or dynamic re-sharing. (supports 5 of 40 shown, est. 10 of 79 residual, gain 0.4417 bits, evidence verified); values: threshold reconstruction from quorum, escrow recovery by third party, proactive resharing over time, no recovery path
- [ACCEPTED] at `payment_settlement_mechanism`: new child_term_type **settlement_finality_timing** — Distinguishes whether settlement is immediate, deferred to a batch or net window, or triggered by a condition or event. (supports 5 of 40 shown, est. 12 of 92 residual, gain 0.4213 bits, evidence verified); values: real-time or instant, batch or net settlement, condition- or event-triggered, periodic or scheduled
- [ACCEPTED] at `centralisation_level`: new child_term_type **centralisation_locus** — Splits centralisation by the specific layer where control concentrates, rather than an overall level. (supports 6 of 40 shown, est. 94 of 625 residual, gain 0.3822 bits, evidence verified); values: consensus_or_mining, block_building_or_ordering, governance_voting, token_issuance_or_monetary_policy, data_storage_or_oracles, validator_or_node_operation
- [ACCEPTED] at `wrapped_or_bridged_asset`: new child_term_type **Cross-chain interoperability mechanism** — Technique used to transfer or verify assets, data, or transactions across distinct blockchain networks. (supports 7 of 24 shown, est. 7 of 24 residual, gain 0.2787 bits, evidence verified); values: side-chain peg / two-way transfer, cross-chain relay or oracle verification, atomic cross-chain swap, software bridge between protocols, cross-chain smart contract execution
- [rejected] at `expressiveness_claim_basis`: new value **tagged as Turing-complete via a named platform or VM (implicit platform attribution)** — Source characterises expressiveness by naming a platform or virtual machine as Turing-complete rather than asserting the ledger's own scripting language directly. (supports 3 of 8 shown, est. 3 of 8 residual, gain 0.9544 bits, evidence verified)
- [rejected] at `ancillary_asset_status`: new child_term_type **token_issuance_model** — Describes the mechanism by which the crypto-asset is initially offered or distributed, such as public sale, airdrop, or protocol mining. (supports 4 of 15 shown, est. 4 of 15 residual, gain 0.8366 bits, evidence verified); values: ICO or token sale, airdrop or fork distribution, protocol mining or staking rewards, platform-internal allocation
- [rejected] at `ancillary_asset_status`: new value **non-fungible token** — A unique, non-interchangeable token representing ownership of a distinct digital or physical item, distinct from fungible tokens and from both listed categories. (supports 3 of 15 shown, est. 3 of 15 residual, gain 0.7219 bits, evidence verified)
- [rejected] at `native_vs_stable_price_reference_asset_currency`: new value **complementary or local currency** — Money-like unit issued alongside or outside national currency, used within a local community or network rather than pegged to a national fiat. (supports 1 of 5 shown, est. 1 of 5 residual, gain 0.7219 bits, evidence verified)
- [rejected] at `tax_reporting_status`: new child_term_type **Tax function supported** — Classifies the specific tax function a crypto-asset tax tool or method performs, such as calculation, withholding, reporting or basis tracking. (supports 4 of 5 shown, est. 4 of 5 residual, gain 0.7219 bits, evidence verified); values: tax calculation, automatic tax withholding, tax filing and reporting, cost basis tracking, tax compliance aid
- [rejected] at `service_location_nexus`: new child_term_type **geographic scope of activity** — Splits texts by the geographic breadth at which the described crypto activity, market or scheme operates. (supports 4 of 21 shown, est. 4 of 21 residual, gain 0.7025 bits, evidence verified); values: global or multi-country reach, single-country or national scope, not geographically specified
- [rejected] at `finality_mechanism`: new value **external checkpoint attestation** — Finality is conferred by a designated external set of parties who attest to or finalize blocks after creation. (supports 3 of 17 shown, est. 3 of 17 residual, gain 0.6723 bits, evidence verified)
- [rejected] at `finality_mechanism`: new value **timestamp-based fair ordering** — Finality and order are fixed by timestamps of receipt from a decentralized clock or agreement protocol, not by block production alone. (supports 3 of 17 shown, est. 3 of 17 residual, gain 0.6723 bits, evidence verified)
- [rejected] at `finality_mechanism`: new value **time-locked confirmation window** — Confirmation is deemed final after a predefined time window or waiting period elapses without objection. (supports 3 of 17 shown, est. 3 of 17 residual, gain 0.6723 bits, evidence verified)
- [rejected] at `backing_of_token`: new value **backed by a pledge or lien over an underlying asset** — The token is backed by a pledge, lien, encumbrance or escrow over an underlying asset held elsewhere. (supports 4 of 25 shown, est. 4 of 25 residual, gain 0.6343 bits, evidence verified)
- [rejected] at `key_share_distribution_topology`: new value **across multiple user-controlled devices** — Key shares are spread across several devices controlled by the same user or a set of user-operated wallets. (supports 3 of 19 shown, est. 3 of 19 residual, gain 0.6292 bits, evidence verified)
- [rejected] at `key_share_distribution_topology`: new value **stored with a file or data copy** — Key shares are associated with individual stored copies of data or files rather than with parties or devices. (supports 3 of 19 shown, est. 3 of 19 residual, gain 0.6292 bits, evidence verified)
- [rejected] at `service_location_nexus`: new value **services offered to cross-border remittance or fund-transfer senders** — Services offered to individuals or businesses sending value across borders, creating jurisdictional nexus through transfer corridors. (supports 3 of 21 shown, est. 3 of 21 residual, gain 0.5917 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **Event- or activity-triggered minting** — Units minted automatically when an external event, user action, or gameplay trigger occurs, rather than by a fixed consensus or collateral rule. (supports 5 of 40 shown, est. 6 of 45 residual, gain 0.5665 bits, evidence unverified)
- [rejected] at `zk_proof_system_variant`: new value **Zero-knowledge succinct range/sum proof (non-SNARK/STARK constructions in ledger confidentiality)** — Range, sum-balance or commitment-opening proofs used to hide transaction amounts, distinct from general-purpose SNARK/STARK circuits. (supports 4 of 36 shown, est. 4 of 36 residual, gain 0.5033 bits, evidence verified)
- [rejected] at `zk_proof_system_variant`: new value **Recursive proof composition / proof aggregation** — ZKP variants that verify other proofs recursively or aggregate multiple proofs into one. (supports 4 of 36 shown, est. 4 of 36 residual, gain 0.5033 bits, evidence verified)
- [rejected] at `anonymity_enhancing_status`: new value **mixing / tumbling service** — Service or protocol that obscures transfer provenance by pooling and redistributing funds, used as an external anonymity-enhancing layer. (supports 3 of 28 shown, est. 3 of 28 residual, gain 0.4912 bits, evidence verified)
- [rejected] at `anonymity_enhancing_status`: new value **off-chain / second-layer network** — Asset transfers conducted in layer-two channels whose activity is only partially visible on the base ledger. (supports 3 of 28 shown, est. 3 of 28 residual, gain 0.4912 bits, evidence verified)
- [rejected] at `central_bank_digital_currency`: new child_term_type **CBDC design model** — Whether the CBDC is issued directly by the central bank to the public or indirectly via intermediaries such as commercial banks. (supports 4 of 40 shown, est. 6 of 57 residual, gain 0.4855 bits, evidence unverified); values: direct (retail) CBDC, indirect (intermediated) CBDC, wholesale CBDC, hybrid CBDC
- [rejected] at `key_custody_control_model`: new value **hardware-isolated secure enclave or TEE** — Key material is held and used inside a hardware-isolated execution environment such as a TEE, enclave, or secure core, separated from the host OS. (supports 4 of 40 shown, est. 27 of 267 residual, gain 0.4725 bits, evidence verified)
- [rejected] at `key_custody_control_model`: new value **key material held on payment card or SIM/UICC chip** — The private key resides in a secure integrated circuit of a card or SIM-like element carried by the user and used for transaction signing. (supports 4 of 40 shown, est. 27 of 267 residual, gain 0.4725 bits, evidence verified)
- [rejected] at `key_custody_control_model`: new value **escrow-held key pair with activation-code release** — A key pair or private key is escrowed or conditionally released to a party only upon satisfying an activation code, endorsement, or policy condition. (supports 4 of 40 shown, est. 27 of 267 residual, gain 0.4725 bits, evidence verified)
- [rejected] at `identity_binding_mechanism`: new value **biometric DNA / voice-based identity binding** — Participant identity is bound to the ledger via inherent biological or voice-derived biometric traits rather than fingerprints or face alone. (supports 4 of 40 shown, est. 120 of 1200 residual, gain 0.469 bits, evidence verified)
- [rejected] at `key_isolation_from_network`: new value **optical/visual code transfer (QR)** — Data crosses the air gap via one-way optical or visual codes such as QR codes displayed and scanned between devices. (supports 4 of 40 shown, est. 6 of 60 residual, gain 0.469 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **cross-chain relay** — Relay of block headers or proofs from one blockchain to another so the receiving chain can verify foreign-chain state. (supports 4 of 40 shown, est. 31 of 314 residual, gain 0.4649 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **cross-chain query and computation execution** — Reading or invoking state, services, or computations on a different blockchain via cross-chain contracts or subscriptions. (supports 4 of 40 shown, est. 31 of 314 residual, gain 0.4649 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **multi-ledger service routing** — A gateway or proxy that routes requests and records across multiple distributed ledger systems. (supports 4 of 40 shown, est. 31 of 314 residual, gain 0.4649 bits, evidence verified)
- [rejected] at `script_verification_approach`: new value **proof-assistant-based verification** — Verifies scripts by encoding semantics and proving properties interactively in a proof assistant such as Coq or Isabelle. (supports 4 of 40 shown, est. 5 of 51 residual, gain 0.4627 bits, evidence verified)
- [rejected] at `cross_chain_transfer_mechanism`: new value **relay-verified burn-and-mint** — Asset is burned on the source chain and re-minted on the destination after an attestation or relay proof of the burn. (supports 4 of 40 shown, est. 5 of 51 residual, gain 0.4627 bits, evidence verified)
- [rejected] at `cross_chain_transfer_mechanism`: new value **notary or attestation-service bridge** — A trusted set of notaries, oracles or attestation services signs off on cross-chain events to authorise transfers. (supports 4 of 40 shown, est. 5 of 51 residual, gain 0.4627 bits, evidence verified)
- [rejected] at `cross_chain_transfer_mechanism`: new value **multi-chain interoperability hub or delegate network** — A common or hub ledger/delegate network mediates transfers among several entity-specific chains. (supports 4 of 40 shown, est. 5 of 51 residual, gain 0.4627 bits, evidence verified)
- [rejected] at `party_role_transfer`: new value **verifying party** — Actor who checks or verifies counterparty identity or account information before or during a transfer, distinct from sender and receiver. (supports 3 of 6 shown, est. 3 of 6 residual, gain 0.4615 bits, evidence verified)
- [rejected] at `party_role_transfer`: new value **mediating provider** — Service provider that relays, mediates or routes a transfer between the originating and beneficiary providers without being either endpoint. (supports 3 of 6 shown, est. 3 of 6 residual, gain 0.4615 bits, evidence verified)
- [rejected] at `consensus_participant_validator_capacity`: new value **consortium-designated (federation member) validators** — Validators drawn from a predefined federation or consortium of organisations, not open to arbitrary participants. (supports 4 of 40 shown, est. 6 of 63 residual, gain 0.4537 bits, evidence verified)
- [rejected] at `consensus_participant_validator_capacity`: new value **permission-gated access by identity or whitelist** — Operation or access is granted only to identities that appear on an authorisation list or are time-limited profiles. (supports 4 of 40 shown, est. 6 of 63 residual, gain 0.4537 bits, evidence verified)
- [rejected] at `key_recovery_mechanism`: new value **smart contract / on-chain recovery** — Recovery executed by a smart contract that authorizes transfer of assets or wallet control to a recovery address on-chain. (supports 4 of 40 shown, est. 4 of 42 residual, gain 0.4537 bits, evidence verified)
- [rejected] at `privacy_mechanism_family`: new value **trusted execution environment** — Confidentiality provided by hardware-isolated enclaves that process data protected from the host. (supports 4 of 40 shown, est. 53 of 534 residual, gain 0.4371 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **Cross-chain burn-and-remint bridging** — Units minted on a destination chain against a burn or lock of the same units on a source chain, with attestation. (supports 4 of 40 shown, est. 4 of 45 residual, gain 0.4328 bits, evidence verified)
- [rejected] at `consensus_finality`: new child_term_type **Finality source of settlement** — Identifies whether finality comes from chain depth, a finality gadget or checkpoint, a BFT quorum, or an off-chain channel. (supports 4 of 40 shown, est. 17 of 171 residual, gain 0.4249 bits, evidence verified); values: confirmation depth, checkpoint or finality gadget, BFT quorum certificate, off-chain channel settlement
- [rejected] at `asset_supply_policy`: new value **supply expanded by protocol-specified inflation** — Native asset supply grows continuously at a rate set by the protocol, without a hard cap. (supports 3 of 40 shown, est. 4 of 47 residual, gain 0.4199 bits, evidence verified)
- [rejected] at `zk_proof_system_variant`: new child_term_type **Trusted setup requirement** — Classifies ZKP systems by whether they need a trusted or universal setup ceremony and how it is conducted. (supports 3 of 36 shown, est. 3 of 36 residual, gain 0.4138 bits, evidence verified); values: trusted setup (per-circuit), universal/updatable setup, transparent (no setup), unspecified
- [rejected] at `script_verification_approach`: new value **type-based verification** — Verifies a script's correctness by type checking or refinement types rather than general formal proof or fuzzing. (supports 3 of 40 shown, est. 4 of 51 residual, gain 0.3966 bits, evidence verified)
- [rejected] at `script_verification_approach`: new value **theorem-carrying proof** — Each transaction carries a machine-checkable proof of safety properties that is checked at execution time. (supports 3 of 40 shown, est. 4 of 51 residual, gain 0.3966 bits, evidence verified)
- [rejected] at `cross_chain_transfer_mechanism`: new value **zero-knowledge proof verification** — The destination chain verifies a zero-knowledge proof or cryptographic certificate of source-chain state to accept a transfer. (supports 3 of 40 shown, est. 4 of 51 residual, gain 0.3966 bits, evidence verified)
- [rejected] at `native_vs_token_standard`: new child_term_type **token fungibility** — Splits tokens by whether each unit is interchangeable with others of the same type or uniquely identifiable. (supports 4 of 40 shown, est. 39 of 386 residual, gain 0.3954 bits, evidence verified); values: fungible, non-fungible, semi-fungible, multi-token (mixed)
- [rejected] at `interoperability_type`: new value **IoT sensor data oracle input** — An oracle that ingests sensor or device telemetry from IoT and industrial systems into a ledger. (supports 3 of 40 shown, est. 24 of 314 residual, gain 0.3895 bits, evidence verified)
- [rejected] at `identity_binding_mechanism`: new value **hardware PUF or chip-level physical identity** — Identity is derived from a physically unclonable function or chip-level hardware fingerprint embedded in the device. (supports 3 of 40 shown, est. 90 of 1200 residual, gain 0.3843 bits, evidence verified)
- [rejected] at `identity_binding_mechanism`: new value **registered personal device possession** — Proof of identity rests on possession of a registered personal electronic device (e.g. smartphone) identified by hardware ID hash. (supports 3 of 40 shown, est. 90 of 1200 residual, gain 0.3843 bits, evidence verified)
- [rejected] at `ledger_purpose`: new value **supply chain traceability and product provenance** — Duplicate-check: already an existing value; residual texts mostly fall here, so no new value needed. (supports 3 of 40 shown, est. 375 of 5004 residual, gain 0.3841 bits, evidence verified)
- [rejected] at `ledger_purpose`: new value **land registry and property record management** — Ledgers used to record ownership, title, or transfers of land and real property. (supports 3 of 40 shown, est. 375 of 5004 residual, gain 0.3841 bits, evidence verified)
- [rejected] at `ledger_partitioning_topology`: new value **parallel transaction groups by account conflict** — Ledger is processed as parallel transaction groups ordered to avoid account conflicts rather than as separate chains. (supports 3 of 40 shown, est. 41 of 547 residual, gain 0.3841 bits, evidence verified)
- [rejected] at `ledger_partitioning_topology`: new value **sharded storage with root-value state commitment** — Shards store partitioned state and commit to it through a root value at the ledger level. (supports 3 of 40 shown, est. 41 of 547 residual, gain 0.3841 bits, evidence verified)
- [rejected] at `ledger_partitioning_topology`: new value **jurisdictionally partitioned ledger** — Ledger partitioned by jurisdiction, region, or location-scoped sub-ledgers. (supports 3 of 40 shown, est. 41 of 547 residual, gain 0.3841 bits, evidence verified)
- [rejected] at `smart_contract_usage_domain`: new value **consent management in health research** — Ledger applications managing patient consent, access rights and sharing of health data for research. (supports 3 of 40 shown, est. 110 of 1471 residual, gain 0.3835 bits, evidence verified)
- [rejected] at `key_recovery_mechanism`: new value **biometric-based recovery** — Recovery of the key or access derived from or verified by biometric data of the user. (supports 3 of 40 shown, est. 3 of 42 residual, gain 0.3712 bits, evidence verified)
- [rejected] at `key_recovery_mechanism`: new value **knowledge-based / oracle-authenticated recovery** — Recovery where the user proves identity through knowledge factors or an oracle rather than holding the seed. (supports 3 of 40 shown, est. 3 of 42 residual, gain 0.3712 bits, evidence verified)
- [rejected] at `central_bank_digital_currency`: new value **stablecoin** — Digital money pegged to a fiat currency issued by a private entity, distinct from both CBDCs and volatile crypto-assets. (supports 3 of 40 shown, est. 4 of 57 residual, gain 0.3666 bits, evidence verified)
- [rejected] at `key_isolation_from_network`: new value **acoustic air-gap transmission** — Keys or signed transaction data are transferred between isolated devices via sound waves rather than a network or direct cable. (supports 3 of 40 shown, est. 4 of 60 residual, gain 0.3534 bits, evidence verified)
- [rejected] at `consensus_finality`: new value **fork-free by construction** — Protocol design that guarantees no forks occur, so settlement is immediate once a block is accepted. (supports 3 of 40 shown, est. 13 of 171 residual, gain 0.3529 bits, evidence verified)
- [rejected] at `payment_settlement_mechanism`: new value **hub-mediated off-chain settlement** — Payments are routed and settled through a central or semi-central payment hub or relay rather than peer-to-peer channels or direct on-chain transfers. (supports 4 of 40 shown, est. 9 of 92 residual, gain 0.3484 bits, evidence verified)
- [rejected] at `settlement_finality_legal_test`: new value **settlement finality defined by central bank or bank-network settlement** — Settlement finality is achieved through settlement at a central bank or inter-bank settlement network rather than by the ledger alone. (supports 3 of 5 shown, est. 3 of 5 residual, gain 0.3468 bits, evidence verified)
- [rejected] at `unhosted_vs_hosted_wallet`: new value **hybrid or multi-party controlled wallet** — Key control is split among several parties or devices (e.g., multisignature, threshold, or federated signing), so neither a single provider nor the user alone controls access. (supports 4 of 40 shown, est. 27 of 272 residual, gain 0.3394 bits, evidence verified)
- [rejected] at `unhosted_vs_hosted_wallet`: new value **identity-linked or biometric-gated wallet** — Access to the wallet keys is bound to a user identity credential or biometric rather than a seed phrase or provider account. (supports 4 of 40 shown, est. 27 of 272 residual, gain 0.3394 bits, evidence verified)
- [rejected] at `native_vs_token_standard`: new value **Bitcoin inscription / ordinal** — Non-fungible or digital asset embedded in Bitcoin transaction data rather than a smart-contract standard. (supports 3 of 40 shown, est. 29 of 386 residual, gain 0.3222 bits, evidence verified)
- [rejected] at `key_management_control_model`: new value **cryptographic escrow with recovery devices** — Private keys are controlled by escrow or recovery devices able to reconstruct the key under authorised conditions. (supports 3 of 40 shown, est. 6 of 78 residual, gain 0.3146 bits, evidence verified)
- [rejected] at `key_management_control_model`: new value **collective group key via weighted threshold scheme** — Signing authority is held collectively by a group whose members jointly produce signatures under a weighted or congress-style scheme. (supports 3 of 40 shown, est. 6 of 78 residual, gain 0.3146 bits, evidence verified)
- [rejected] at `key_management_control_model`: new value **policy-gated vault endorsement** — Key use is controlled by vault-specific policy maps requiring endorsement messages from designated approvers. (supports 3 of 40 shown, est. 6 of 78 residual, gain 0.3146 bits, evidence verified)
- [rejected] at `key_splitting_scheme`: new value **hierarchical deterministic key derivation** — Signing keys are derived from a master seed through a hierarchical tree, so child keys are split off from a single root rather than from shares of one key. (supports 3 of 40 shown, est. 6 of 79 residual, gain 0.3126 bits, evidence verified)
- [rejected] at `payment_settlement_mechanism`: new value **offline or disconnected settlement** — Payments are authorised and recorded locally without network connectivity, with settlement deferred until connectivity is restored. (supports 3 of 40 shown, est. 7 of 92 residual, gain 0.2928 bits, evidence verified)
- [rejected] at `payment_settlement_mechanism`: new value **commitment-based unidirectional settlement** — Payer pre-commits funds through signed commitment transactions that the payee can later redeem, with unidirectional flow. (supports 3 of 40 shown, est. 7 of 92 residual, gain 0.2928 bits, evidence verified)
- [rejected] at `centralisation_level`: new value **federated_or_consortium** — Control shared among a known, permissioned set of member institutions rather than one entity or open participants. (supports 4 of 40 shown, est. 62 of 625 residual, gain 0.2918 bits, evidence verified)
- [rejected] at `centralisation_level`: new value **centrally_administered_by_issuer** — Token or protocol rules remain modifiable by an administrator retained by the issuing platform after deployment. (supports 4 of 40 shown, est. 62 of 625 residual, gain 0.2918 bits, evidence verified)
- [rejected] at `smart_contract_usage_domain`: new value **online auction and bidding** — Smart contracts that run auctions, bidding and automated matching of offers between buyers and sellers. (supports 2 of 40 shown, est. 74 of 1471 residual, gain 0.2877 bits, evidence verified)
- [rejected] at `risk_type_illicit_finance`: new value **fund tracing and taint propagation** — Risk arising from tracing illicit funds through the chain and propagating taint scores across linked wallets and transactions. (supports 4 of 40 shown, est. 4 of 44 residual, gain 0.2649 bits, evidence verified)
- [rejected] at `risk_type_illicit_finance`: new value **Ponzi scheme** — Risk from Ponzi or high-yield investment programmes that pay earlier investors with later investors' funds. (supports 3 of 40 shown, est. 3 of 44 residual, gain 0.2164 bits, evidence verified)
- [rejected] at `risk_type_illicit_finance`: new value **wash trading** — Risk from artificial trading between controlled accounts to inflate apparent volume or price of an asset, including NFTs. (supports 3 of 40 shown, est. 3 of 44 residual, gain 0.2164 bits, evidence verified)
- [rejected] at `risk_type_illicit_finance`: new value **network-level address deanonymisation** — Risk that anonymity of addresses is broken by graph analysis or linking of off-chain data to on-chain identities. (supports 3 of 40 shown, est. 3 of 44 residual, gain 0.2164 bits, evidence verified)
- [rejected] at `wrapped_or_bridged_asset`: new value **custodial token / digital bearer representation** — Crypto-asset that represents a claim on a real or digital asset held in a card, vault, or platform account. (supports 4 of 24 shown, est. 4 of 24 residual, gain 0.208 bits, evidence unverified)
- [rejected] at `ecosystem_participant_role`: new value **construction practitioner / project stakeholder** — Participant whose role is as an owner, contractor, consultant or other stakeholder in a built-environment or industry project adopting blockchain. (supports 4 of 40 shown, est. 15 of 150 residual, gain 0.1927 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **supply chain / logistics** — Duplicate placeholder; ignore if already present. (supports 1 of 40 shown, est. 2 of 83 residual, gain 0.1639 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **retail investor / survey respondent** — Individual end user or investor whose role is as a non-professional holder, trader or respondent in a study of crypto-asset use. (supports 3 of 40 shown, est. 11 of 150 residual, gain 0.1554 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **oracle / data feeder operator** — Participant who supplies or aggregates off-chain data to a blockchain as an oracle node or data feeder. (supports 3 of 40 shown, est. 11 of 150 residual, gain 0.1554 bits, evidence verified)
- [rejected] at `script_language_expressiveness`: new value **concurrent multi-thread script execution** — Script execution model in which multiple execution threads run concurrently, typically forked from prior transaction scripts. (supports 3 of 40 shown, est. 23 of 302 residual, gain 0.1548 bits, evidence verified)
- [rejected] at `tokenisation_form`: new value **tokenised voting-trust interest** — Token representing beneficial interest held through a voting trust rather than direct equity ownership. (supports 3 of 40 shown, est. 28 of 368 residual, gain 0.1538 bits, evidence verified)
- [rejected] at `tokenisation_form`: new value **tokenised future production / offtake right** — Token representing a claim on future output or extraction of a resource, such as a mine partition. (supports 3 of 40 shown, est. 28 of 368 residual, gain 0.1538 bits, evidence verified)
- [rejected] at `tokenisation_form`: new value **tokenised right-to-use / usage-right token** — Token conferring a right to use or access a physical or virtual resource rather than ownership of it. (supports 3 of 40 shown, est. 28 of 368 residual, gain 0.1538 bits, evidence verified)
- [rejected] at `tokenisation_form`: new value **tokenised biological object** — Token representing ownership or transfer rights over a biological sample or specimen. (supports 2 of 40 shown, est. 18 of 368 residual, gain 0.1116 bits, evidence verified)
- [rejected] at `key_management_control_model`: new child_term_type **Key share distribution topology** —  (supports 0 of 40 shown, est. 0 of 78 residual, gain 0.0 bits, evidence unverified)