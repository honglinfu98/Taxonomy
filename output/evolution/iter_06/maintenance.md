# Part 2 maintenance: the DAG as label space

1818 tagged items placed on 119/128 nodes (7330 tags, 33463 closure placements).

## Objectives: content-driven vs Part 1 prior

| metric | from tags (empirical) | from is-a weights (Part 1) |
|---|---|---|
| bits per descent (information gain) | 7.0636 | 5.0241 |
| AUC of reach-a-leaf | 0.7734 | 0.8331 |
| expected depth | 3.8953 | 3.0033 |
| effective leaves | 22.947 | 26.075 |
| effective leaves / nodes | 0.1793 | 0.2037 |

## Where descents stop (top stop mass)

- Ledger purpose `ledger_purpose`: 0.2443
- Smart contract usage domain `smart_contract_usage_domain`: 0.1205
- Native asset versus token standard `native_vs_token_standard`: 0.0634
- Centralisation of control `centralisation_level`: 0.0493
- Privacy mechanism family `privacy_mechanism_family`: 0.0417
- Identity binding mechanism `identity_binding_mechanism`: 0.0338
- Interoperability and intraoperability `interoperability_type`: 0.0332
- Privacy and anonymity features `privacy_enhancement`: 0.0331
- Cross-chain interoperability mechanism `cross_chain_interoperability_mechanism`: 0.0327
- Smart contract / script language expressiveness `script_language_expressiveness`: 0.0314
- Validator selection mechanism `validator_selection_mechanism`: 0.0304
- Recording and cryptographic linkage `digital_asset_recording`: 0.0237
- Key custody and control model `key_custody_control_model`: 0.0181
- Centralisation locus `centralisation_locus`: 0.0177
- Smart contract deployment context `smart_contract_deployment_context`: 0.0155

## Node statistics (nodes with items, by closure size)

| node | cat | direct | closure | children | value entropy | dominance | branching gain | residual |
|---|---|---|---|---|---|---|---|---|
| Crypto-asset definitional criteria | asset | 150 | 1461 | 10 | 0.9672 | 0.664 | 2.3459 | 24 (0.016) |
| Economic function of the asset | asset | 258 | 1437 | 9 | 1.0437 | 0.799 | 2.7696 | 52 (0.036) |
| Legal classification of crypto-asset | asset | 46 | 1385 | 11 | 1.0914 | 0.766 | 2.7175 | 19 (0.014) |
| Reference asset type | asset | 73 | 1366 | 7 | 1.8418 | 0.549 | 2.2353 | 23 (0.017) |
| Issuer identifiability | asset | 14 | 1333 | 6 | 1.1981 | 0.643 | 1.4512 | 0 (0.0) |
| Payment stablecoin / e-money / ART reg | asset | 10 | 1333 | 3 | 1.7219 | 0.4 | 0.8169 | 2 (0.002) |
| Convertible virtual currency (CVC) sta | asset | 34 | 1265 | 1 | 0.1914 | 0.971 | 0.0979 | 16 (0.013) |
| Governance model of a DLT system | techn | 141 | 1259 | 8 | 1.5921 | 0.601 | 2.793 | 26 (0.021) |
| Recording and cryptographic linkage | asset | 282 | 1249 | 6 | 0.3286 | 0.94 | 1.6115 | 103 (0.082) |
| Ledger access and permissioning | techn | 342 | 1233 | 14 | 1.6251 | 0.377 | 3.4073 | 23 (0.019) |
| Ledger scope: open or closed access by | techn | 69 | 1210 | 5 | 1.4881 | 0.449 | 1.9645 | 8 (0.007) |
| Network topology and node roles | techn | 264 | 1202 | 7 | 1.0233 | 0.714 | 2.3829 | 27 (0.022) |
| Consensus mechanism | techn | 284 | 1172 | 6 | 1.6618 | 0.428 | 2.3725 | 46 (0.039) |
| Validator reward mechanism | techn | 67 | 1126 | 4 | 0.6583 | 0.87 | 1.2229 | 15 (0.013) |
| Transaction fee regime | techn | 20 | 1111 | 2 | 1.8716 | 0.429 | 0.1434 | 1 (0.001) |
| Native asset presence and type | techn | 65 | 1110 | 4 | 0.686 | 0.862 | 1.4375 | 15 (0.014) |
| Software architecture (monolithic vs p | techn | 58 | 1085 | 5 | 0.8179 | 0.746 | 2.1853 | 10 (0.009) |
| Ledger storage model (what is stored o | techn | 103 | 1075 | 3 | 1.1987 | 0.727 | 1.4536 | 14 (0.013) |
| Ledger purpose | techn | 1057 | 1057 | 0 | 2.5731 | 0.361 | -0.0 | 1057 (1.0) |
| DLT data structure (blockchain vs non- | techn | 320 | 866 | 4 | 0.5684 | 0.9 | 1.6071 | 148 (0.171) |
| Decentralised system certification | techn | 26 | 629 | 2 | 1.5486 | 0.385 | 0.8949 | 12 (0.019) |
| Source code openness | techn | 13 | 617 | 2 | -0.0 | 1.0 | 0.3336 | 4 (0.006) |
| Smart contract / distributed ledger ap | techn | 291 | 590 | 2 | 1.0815 | 0.623 | 1.2289 | 54 (0.092) |
| Node / DLT network node role | techn | 95 | 482 | 1 | 2.2009 | 0.324 | 0.5978 | 70 (0.145) |
| Smart contract usage domain | techn | 426 | 426 | 0 | 3.0416 | 0.266 | -0.0 | 426 (1.0) |
| Information and communications technol | techn | 4 | 412 | 3 | -0.0 | 1.0 | 1.5361 | 2 (0.005) |
| Identity layer and onboarding | techn | 133 | 410 | 3 | 0.7833 | 0.767 | 1.6086 | 46 (0.112) |
| Redemption mechanism | asset | 7 | 403 | 4 | 1.1488 | 0.714 | 1.7258 | 3 (0.007) |
| Form of holder claim | asset | 3 | 400 | 4 | 0.9183 | 0.667 | 1.4583 | 2 (0.005) |
| Source of yield | asset | 17 | 318 | 1 | 0.6402 | 0.882 | 0.2605 | 14 (0.044) |
| Yield distribution mechanism | asset | 0 | 304 | 1 | - | - | -0.0 | 0 (0.0) |
| Centralisation of control | asset | 211 | 304 | 3 | 1.3213 | 0.63 | 1.3758 | 195 (0.641) |
| Privacy and anonymity features | techn | 126 | 219 | 2 | 1.0469 | 0.703 | 1.4229 | 82 (0.374) |
| Data classification (traffic, content, | techn | 0 | 219 | 1 | - | - | -0.0 | 0 (0.0) |
| Identity binding mechanism | techn | 206 | 206 | 0 | 2.5639 | 0.411 | -0.0 | 206 (1.0) |
| Smart contract / script language expre | techn | 106 | 196 | 4 | 0.8585 | 0.853 | 1.9293 | 75 (0.383) |
| Crypto-asset service provider or VASP  | actor | 25 | 148 | 16 | 1.7098 | 0.5 | 3.5892 | 17 (0.115) |
| Ledger partitioning or layering topolo | techn | 147 | 147 | 1 | 2.4652 | 0.325 | 0.3323 | 138 (0.939) |
| Offshore VASP status (activity-based o | actor | 0 | 131 | 2 | - | - | 1.0 | 0 (0.0) |
| Jurisdictional regime and home or host | actor | 5 | 131 | 5 | 0.7219 | 0.8 | 1.9146 | 2 (0.015) |
| Principal or agent role in transaction | actor | 6 | 129 | 8 | 1.4591 | 0.5 | 2.1138 | 5 (0.039) |
| Financial institution status for AML | actor | 0 | 129 | 3 | - | - | 0.1292 | 0 (0.0) |
| Custody model | actor | 14 | 124 | 6 | 1.4926 | 0.5 | 2.3517 | 8 (0.065) |
| Tokenisation form | asset | 48 | 120 | 3 | 2.1745 | 0.3 | 1.5242 | 25 (0.208) |
| Trading venue type | actor | 8 | 116 | 1 | 0.9911 | 0.556 | 0.3621 | 8 (0.069) |
| Privacy mechanism family | techn | 110 | 110 | 1 | 2.0096 | 0.535 | 0.3417 | 103 (0.936) |
| Control or sufficient influence over D | actor | 3 | 108 | 3 | 0.9183 | 0.667 | 0.9574 | 0 (0.0) |
| Fungibility | asset | 38 | 102 | 1 | 0.8582 | 0.718 | 0.5504 | 13 (0.127) |
| Ecosystem participant role | actor | 48 | 95 | 4 | 1.9083 | 0.583 | 1.9996 | 48 (0.505) |
| Infrastructure provider type | actor | 2 | 95 | 2 | 1.0 | 0.5 | 0.9059 | 0 (0.0) |
| Native asset versus token standard | asset | 64 | 89 | 1 | 1.4817 | 0.538 | 0.8715 | 63 (0.708) |
| Centralisation locus | asset | 70 | 70 | 0 | 2.2898 | 0.324 | -0.0 | 70 (1.0) |
| Crypto-asset service type | activ | 27 | 67 | 10 | 2.2597 | 0.281 | 3.151 | 17 (0.254) |
| Interoperability and intraoperability | techn | 61 | 61 | 0 | 2.6483 | 0.304 | -0.0 | 61 (1.0) |
| Permitted control over client assets ( | actor | 2 | 58 | 3 | -0.0 | 1.0 | 1.0528 | 1 (0.017) |
| Stablecoin issuer model | actor | 0 | 47 | 1 | - | - | -0.0 | 0 (0.0) |
| Operator of crypto-asset arrangement | actor | 2 | 47 | 2 | 1.0 | 0.5 | 0.2539 | 2 (0.043) |
| Validator operation capacity (who may  | actor | 8 | 45 | 1 | 0.9544 | 0.625 | 0.6236 | 7 (0.156) |
| Transfer of crypto-assets (travel rule | activ | 5 | 40 | 8 | -0.0 | 1.0 | 2.7531 | 4 (0.1) |
| Finality of agreement | techn | 33 | 39 | 2 | 0.9183 | 0.667 | 1.2151 | 26 (0.667) |
| Validator selection mechanism | techn | 38 | 38 | 0 | 2.8984 | 0.182 | -0.0 | 38 (1.0) |
| Anti-money laundering obligations | oblig | 16 | 37 | 9 | 0.5226 | 0.882 | 2.3267 | 11 (0.297) |
| Smart contract deployment context | techn | 37 | 37 | 0 | 1.6769 | 0.541 | -0.0 | 37 (1.0) |
| Hosted versus unhosted (self-hosted) w | asset | 21 | 36 | 3 | 1.408 | 0.571 | 1.7561 | 16 (0.444) |
| Money transmission (acceptance and tra | activ | 0 | 36 | 5 | - | - | 1.9427 | 0 (0.0) |
| Public offer or private placement | activ | 3 | 36 | 3 | -0.0 | 1.0 | 1.0213 | 1 (0.028) |
| Offer and issuance method (token distr | activ | 8 | 35 | 3 | 1.3568 | 0.7 | 1.8599 | 8 (0.229) |
| Wallet storage mode (hot or cold) | techn | 11 | 30 | 1 | 0.9457 | 0.636 | 0.8813 | 9 (0.3) |
| Script verification approach | techn | 27 | 27 | 0 | 2.0054 | 0.375 | -0.0 | 27 (1.0) |
| Wrapped / cross-chain representation | asset | 11 | 26 | 2 | 0.994 | 0.545 | 0.6194 | 4 (0.154) |
| Virtual assets as property or proceeds | oblig | 2 | 26 | 7 | -0.0 | 1.0 | 2.1513 | 0 (0.0) |
| Freezing and blocking capability | oblig | 0 | 23 | 4 | - | - | 1.1297 | 0 (0.0) |
| Illicit finance risk category | oblig | 16 | 23 | 2 | 1.7219 | 0.4 | 0.8077 | 3 (0.13) |
| Cross-chain interoperability mechanism | techn | 22 | 22 | 0 | 2.5387 | 0.304 | -0.0 | 22 (1.0) |
| Asset supply management (monetary poli | techn | 21 | 21 | 0 | 0.9939 | 0.773 | -0.0 | 21 (1.0) |
| Key custody and control model | techn | 21 | 21 | 0 | 1.1155 | 0.667 | -0.0 | 21 (1.0) |
| Peer-to-peer (P2P) transaction | activ | 1 | 19 | 1 | -0.0 | 1.0 | 0.2975 | 1 (0.053) |
| Anonymity-enhancing crypto-asset statu | oblig | 16 | 19 | 1 | 1.2608 | 0.647 | 0.9819 | 8 (0.421) |
| Payment service and funds transfer | activ | 8 | 18 | 2 | -0.0 | 1.0 | 1.2997 | 5 (0.278) |
| Key splitting scheme | techn | 12 | 17 | 3 | 1.7842 | 0.417 | 1.7474 | 8 (0.471) |
| Central bank digital currency status | asset | 15 | 15 | 0 | 0.9495 | 0.632 | -0.0 | 15 (1.0) |
| Key isolation from network connectivit | techn | 10 | 13 | 3 | 1.361 | 0.5 | 1.9542 | 4 (0.308) |
| Payment settlement mechanism | activ | 9 | 11 | 2 | 1.8911 | 0.333 | 1.5567 | 4 (0.364) |
| Key management control model | activ | 7 | 11 | 1 | 1.8424 | 0.429 | 0.9457 | 7 (0.636) |
| Deanonymisation / tracing approach | oblig | 11 | 11 | 0 | 1.9591 | 0.5 | -0.0 | 11 (1.0) |
| Finality mechanism | techn | 9 | 9 | 0 | 0.9864 | 0.778 | -0.0 | 9 (1.0) |
| Sharding partition basis | techn | 9 | 9 | 0 | 1.1568 | 0.7 | -0.0 | 9 (1.0) |
| Wallet interface or delivery form | techn | 9 | 9 | 0 | 1.7219 | 0.4 | -0.0 | 9 (1.0) |
| Staking arrangement (self, delegated,  | activ | 1 | 8 | 1 | 1.0 | 0.5 | 0.5436 | 1 (0.125) |
| Minting mechanism | activ | 7 | 7 | 0 | 1.4488 | 0.429 | -0.0 | 7 (1.0) |
| Zero-knowledge proof system variant | techn | 7 | 7 | 0 | 0.8631 | 0.714 | -0.0 | 7 (1.0) |
| Backing of token | asset | 4 | 7 | 1 | 1.5 | 0.5 | 0.5917 | 1 (0.143) |
| Ancillary asset and network token stat | asset | 6 | 6 | 0 | 0.9183 | 0.667 | -0.0 | 6 (1.0) |
| Backing mechanism | asset | 6 | 6 | 0 | 1.4591 | 0.5 | -0.0 | 6 (1.0) |
| Settlement finality timing | activ | 6 | 6 | 0 | 1.4591 | 0.5 | -0.0 | 6 (1.0) |
| Key isolation mechanism | techn | 6 | 6 | 0 | 1.9183 | 0.333 | -0.0 | 6 (1.0) |
| Key share cryptographic primitive | techn | 6 | 6 | 0 | 0.65 | 0.833 | -0.0 | 6 (1.0) |
| Key share distribution topology | techn | 4 | 4 | 0 | 1.0 | 0.5 | -0.0 | 4 (1.0) |
| Fiat-rail integration | activ | 4 | 4 | 1 | 1.5 | 0.5 | -0.0 | 4 (1.0) |
| Physical transfer mechanism across air | techn | 3 | 4 | 1 | 0.9183 | 0.667 | 0.8113 | 1 (0.25) |
| Finality guarantee mode | techn | 4 | 4 | 0 | 0.8113 | 0.75 | -0.0 | 4 (1.0) |
| Redemption and reserve adequacy | oblig | 1 | 3 | 4 | -0.0 | 1.0 | 0.9183 | 1 (0.333) |
| Yield or interest on stablecoin | oblig | 0 | 3 | 2 | - | - | -0.0 | 0 (0.0) |
| Investment contract (Howey) criteria | oblig | 0 | 3 | 3 | - | - | -0.0 | 0 (0.0) |
| Security status of digital asset (US e | oblig | 0 | 3 | 2 | - | - | 1.0 | 0 (0.0) |
| MiFID financial instrument status | oblig | 0 | 3 | 2 | - | - | 1.0 | 0 (0.0) |
| Excluded instrument category (EU scope | oblig | 0 | 3 | 4 | - | - | 1.9808 | 0 (0.0) |
| Key distribution method across isolati | techn | 3 | 3 | 0 | 0.9183 | 0.667 | -0.0 | 3 (1.0) |
| Settlement finality and legal enforcea | oblig | 2 | 2 | 3 | -0.0 | 1.0 | -0.0 | 2 (1.0) |
| Nexus to jurisdiction (services offere | activ | 2 | 2 | 0 | -0.0 | 1.0 | -0.0 | 2 (1.0) |
| Key recovery mechanism | techn | 2 | 2 | 0 | -0.0 | 1.0 | -0.0 | 2 (1.0) |
| Pooled investment vehicle structure | actor | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Serious crime threshold for predicate  | oblig | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Address linkage to service provider | actor | 0 | 1 | 1 | - | - | -0.0 | 0 (0.0) |
| Originator and beneficiary role | actor | 0 | 1 | 1 | - | - | -0.0 | 0 (0.0) |
| Consumer or retail versus professional | actor | 1 | 1 | 1 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Reference currency for stablecoin peg  | asset | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Expressiveness claim basis | techn | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Share recovery mechanism | techn | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |

## Maintenance proposals

**Dormant nodes (9)**, no items in this batch: `custody_safeguarding_obligation`, `operational_resilience_risk`, `prudential_classification_group`, `tradfi_analogue`, `related_person_affiliation`, `regulated_status_cvc_mst_exemption`, `tax_reporting_status`, `cross_chain_transfer_mechanism`, `settlement_counterparty`

**Collapsed nodes (9)**, many items but one value absorbs them (merge or re-split candidates):
- Source of yield `yield_source`: 17 items, dominance 0.882 (no yield)
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 320 items, dominance 0.9 (blockchain (chain of blocks))
- Smart contract / script language expressiveness `script_language_expressiveness`: 106 items, dominance 0.853 (Turing complete)
- Source code openness `code_license_openness`: 13 items, dominance 1.0 (open source)
- Native asset presence and type `native_asset_type`: 65 items, dominance 0.862 (own single cryptocurrency)
- Validator reward mechanism `reward_mechanism`: 67 items, dominance 0.87 (lump-sum reward)
- Convertible virtual currency (CVC) status `convertible_virtual_currency_status`: 34 items, dominance 0.971 (convertible virtual currency (CVC))
- Anti-money laundering obligations `aml_obligations_applicability`: 16 items, dominance 0.882 (obliged entity (crypto-asset service provider))
- Recording and cryptographic linkage `digital_asset_recording`: 282 items, dominance 0.94 (recorded on cryptographically secured distributed ledger)

**Highest-gain nodes**:
- Crypto-asset service provider or VASP status `service_provider_status`: 3.5892 bits over 148 items
- Ledger access and permissioning `ledger_access_permission`: 3.4073 bits over 1233 items
- Crypto-asset service type `crypto_asset_service_type`: 3.151 bits over 67 items
- Governance model of a DLT system `governance_model`: 2.793 bits over 1259 items
- Economic function of the asset `crypto_asset_function`: 2.7696 bits over 1437 items
- Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`: 2.7531 bits over 40 items
- Legal classification of crypto-asset `legal_classification_status`: 2.7175 bits over 1385 items
- Network topology and node roles `network_topology`: 2.3829 bits over 1202 items

**Discovery targets (36)**, residual >= threshold:
- Ledger purpose `ledger_purpose`: 1057 residual of 1057 (1.0)
- Smart contract usage domain `smart_contract_usage_domain`: 426 residual of 426 (1.0)
- Identity binding mechanism `identity_binding_mechanism`: 206 residual of 206 (1.0)
- Centralisation of control `centralisation_level`: 195 residual of 304 (0.641)
- Ledger partitioning or layering topology `ledger_partitioning_topology`: 138 residual of 147 (0.939)
- Privacy mechanism family `privacy_mechanism_family`: 103 residual of 110 (0.936)
- Privacy and anonymity features `privacy_enhancement`: 82 residual of 219 (0.374)
- Smart contract / script language expressiveness `script_language_expressiveness`: 75 residual of 196 (0.383)
- Centralisation locus `centralisation_locus`: 70 residual of 70 (1.0)
- Native asset versus token standard `native_vs_token_standard`: 63 residual of 89 (0.708)
- Interoperability and intraoperability `interoperability_type`: 61 residual of 61 (1.0)
- Ecosystem participant role `ecosystem_participant_role`: 48 residual of 95 (0.505)
- Validator selection mechanism `validator_selection_mechanism`: 38 residual of 38 (1.0)
- Smart contract deployment context `smart_contract_deployment_context`: 37 residual of 37 (1.0)
- Script verification approach `script_verification_approach`: 27 residual of 27 (1.0)
- Finality of agreement `consensus_finality`: 26 residual of 39 (0.667)
- Cross-chain interoperability mechanism `cross_chain_interoperability_mechanism`: 22 residual of 22 (1.0)
- Asset supply management (monetary policy) `asset_supply_policy`: 21 residual of 21 (1.0)
- Key custody and control model `key_custody_control_model`: 21 residual of 21 (1.0)
- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`: 16 residual of 36 (0.444)
- Central bank digital currency status `central_bank_digital_currency`: 15 residual of 15 (1.0)
- Deanonymisation / tracing approach `deanonymisation_tracing_approach`: 11 residual of 11 (1.0)
- Wallet storage mode (hot or cold) `wallet_type_storage`: 9 residual of 30 (0.3)
- Finality mechanism `finality_mechanism`: 9 residual of 9 (1.0)
- Sharding partition basis `sharding_partition_basis`: 9 residual of 9 (1.0)
- Wallet interface or delivery form `wallet_interface_delivery_form`: 9 residual of 9 (1.0)
- Anonymity-enhancing crypto-asset status `anonymity_enhancing_status`: 8 residual of 19 (0.421)
- Key splitting scheme `key_splitting_scheme`: 8 residual of 17 (0.471)
- Minting mechanism `minting_mechanism`: 7 residual of 7 (1.0)
- Key management control model `key_management_control_model`: 7 residual of 11 (0.636)
- Zero-knowledge proof system variant `zk_proof_system_variant`: 7 residual of 7 (1.0)
- Ancillary asset and network token status `ancillary_asset_status`: 6 residual of 6 (1.0)
- Backing mechanism `backing_mechanism`: 6 residual of 6 (1.0)
- Settlement finality timing `settlement_finality_timing`: 6 residual of 6 (1.0)
- Key isolation mechanism `isolation_mechanism`: 6 residual of 6 (1.0)
- Key share cryptographic primitive `key_share_cryptographic_primitive`: 6 residual of 6 (1.0)

## Discovery (Task E) candidates

- [ACCEPTED] at `zk_proof_system_variant`: new child_term_type **ZKP application role** — Distinguishes whether the ZKP is used for rollup validity, identity or privacy of data, verifiable computation, or range and rating validation. (supports 5 of 7 shown, est. 5 of 7 residual, gain 0.8631 bits, evidence verified); values: scaling / rollup validity proof, data or identity privacy, verifiable computation / virtual machine, range or rating correctness
- [ACCEPTED] at `key_custody_control_model`: new child_term_type **key storage medium or environment** — Distinguishes whether keys reside in volatile memory, hardware security modules, trusted execution environments, or are only on a user's device. (supports 5 of 21 shown, est. 5 of 21 residual, gain 0.7919 bits, evidence verified); values: volatile memory with power-down erasure, hardware security module or trusted execution environment, user mobile or desktop device, physical card or bearer medium, cloud or remote encrypted server
- [ACCEPTED] at `ledger_partitioning_topology`: new value **hierarchical multi-blockchain with main and multiple subchains** — Topology where a main chain anchors or coordinates several subchains or sidechains that each process a partition of state or tasks. (supports 6 of 40 shown, est. 21 of 138 residual, gain 0.5776 bits, evidence verified)
- [ACCEPTED] at `ledger_partitioning_topology`: new child_term_type **parent-child coupling mechanism** — Distinguishes how partitions or subchains are bound to the main ledger, which affects cross-chain verification and security inheritance. (supports 6 of 40 shown, est. 21 of 138 residual, gain 0.5776 bits, evidence verified); values: merged mining, sidechain two-way peg, coupled pair anchoring, interlinked peer chains, none or independent
- [ACCEPTED] at `centralisation_locus`: new value **identity_or_access_control** — Centralisation of who may join, authorise, or hold access rights, such as a single controlling address or a trusted authority issuing keys or approvals. (supports 5 of 40 shown, est. 9 of 70 residual, gain 0.5535 bits, evidence verified)
- [ACCEPTED] at `consensus_finality`: new child_term_type **Finality guarantee source** — Whether finality comes from quorum intersection, chain depth or confirmation count, economic stake slashing, or a checkpoint/justification gadget. (supports 5 of 26 shown, est. 5 of 26 residual, gain 0.4708 bits, evidence verified); values: quorum-based BFT finality, confirmation-depth finality, economic-penalty finality, checkpoint or justification finality
- [rejected] at `settlement_finality_timing`: new value **on-demand or on-request** — Settlement finality is triggered by an explicit request or action from a party, such as a merchant funding request or a shipper's withdrawal, rather than by a clock or by network events. (supports 3 of 6 shown, est. 3 of 6 residual, gain 1.0 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **reward-gated minting** — New tokens are issued as rewards for verified work or behaviour, such as completing education tasks or contributing to a mining pool. (supports 3 of 7 shown, est. 3 of 7 residual, gain 0.9852 bits, evidence verified)
- [rejected] at `zk_proof_system_variant`: new value **MPC-in-the-Head proof** — Zero-knowledge proofs constructed by simulating a multi-party computation in the prover's head, typically post-quantum secure. (supports 3 of 7 shown, est. 3 of 7 residual, gain 0.9852 bits, evidence verified)
- [rejected] at `finality_mechanism`: new value **payment-channel dispute window** — Finality is enforced off-chain by channel closure or dispute resolution, settled by an on-chain transaction within a time window. (supports 3 of 9 shown, est. 3 of 9 residual, gain 0.9183 bits, evidence verified)
- [rejected] at `wallet_interface_delivery_form`: new value **physical card or token** — placeholder (supports 3 of 9 shown, est. 3 of 9 residual, gain 0.9183 bits, evidence verified)
- [rejected] at `sharding_partition_basis`: new value **security-threshold or committee-size partition** — Shards are formed so each committee's size or adversary-tolerance threshold meets a security bound, rather than by accounts or graph structure. (supports 3 of 9 shown, est. 3 of 9 residual, gain 0.9183 bits, evidence verified)
- [rejected] at `sharding_partition_basis`: new value **hash-based or deterministic-function assignment** — Nodes or users are assigned to shards by applying a deterministic function such as consistent hashing to an identifier. (supports 3 of 9 shown, est. 3 of 9 residual, gain 0.9183 bits, evidence verified)
- [rejected] at `backing_mechanism`: new value **title or equitable interest in physical commodities in place** — Token represents equitable title to unsevered physical commodities that stay at their site and are traded without moving them. (supports 2 of 6 shown, est. 2 of 6 residual, gain 0.9183 bits, evidence verified)
- [rejected] at `settlement_finality_timing`: new value **off-chain channel or layer-2 finality** — Payments become final off the main ledger through channel state updates or layer-2 mechanisms, with on-chain settlement occurring only at channel open or close. (supports 2 of 6 shown, est. 2 of 6 residual, gain 0.9183 bits, evidence verified)
- [rejected] at `key_share_cryptographic_primitive`: new value **Weighted threshold secret sharing** — Secret sharing in which shareholders hold weighted shares and a threshold of total weight is needed to reconstruct the key. (supports 2 of 6 shown, est. 2 of 6 residual, gain 0.9183 bits, evidence verified)
- [rejected] at `key_share_cryptographic_primitive`: new value **Threshold Schnorr signature scheme** — Threshold signature scheme producing Schnorr signatures, such as FROST, with distributed signing rounds. (supports 2 of 6 shown, est. 2 of 6 residual, gain 0.9183 bits, evidence verified)
- [rejected] at `isolation_mechanism`: new value **physically separated offline device** — Key material resides on a device kept physically disconnected from the internet, with transactions handled offline and synchronised later. (supports 2 of 6 shown, est. 2 of 6 residual, gain 0.9183 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **location-verified minting** — New NFTs are minted only after a location verification device confirms the requesting user's physical presence at an event. (supports 2 of 7 shown, est. 2 of 7 residual, gain 0.8631 bits, evidence verified)
- [rejected] at `deanonymisation_tracing_approach`: new value **multi-input common-spend heuristic** — Links addresses co-spent in one transaction to the same controlling entity, as a deanonymisation technique. (supports 3 of 11 shown, est. 3 of 11 residual, gain 0.8454 bits, evidence verified)
- [rejected] at `deanonymisation_tracing_approach`: new value **seed-address forward and backward tracing** — Follows funds from known or seed addresses through the ledger to identify linked actors and payment flows. (supports 3 of 11 shown, est. 3 of 11 residual, gain 0.8454 bits, evidence verified)
- [rejected] at `deanonymisation_tracing_approach`: new value **forensic artifact recovery** — Recovers identifying artifacts from seized devices, software or service images to link pseudonymous activity to people. (supports 3 of 11 shown, est. 3 of 11 residual, gain 0.8454 bits, evidence verified)
- [rejected] at `central_bank_digital_currency`: new value **unbacked crypto-asset or stablecoin** — Private digital asset not issued as a central bank liability, including unbacked crypto assets and stablecoins that compete with CBDCs. (supports 3 of 15 shown, est. 3 of 15 residual, gain 0.7219 bits, evidence verified)
- [rejected] at `key_custody_control_model`: new value **policy-validated or delegated signing** — Signing authority is granted via smart-contract policy, delegation attestation, or validation rules rather than held solely by the user or a custodian. (supports 4 of 21 shown, est. 4 of 21 residual, gain 0.7025 bits, evidence verified)
- [rejected] at `ancillary_asset_status`: new child_term_type **Market manipulation scheme type** — Classifies the form of manipulative or fraudulent trading scheme described in the text. (supports 1 of 6 shown, est. 1 of 6 residual, gain 0.65 bits, evidence verified); values: pump and dump, wash trading, ponzi or fraud scheme, none
- [rejected] at `backing_mechanism`: new value **cross-chain collateral via bridged or pegged token** — Backing is cryptocurrency collateral on another blockchain, represented on the token's chain by a pegged stablecoin or wrapped asset. (supports 1 of 6 shown, est. 1 of 6 residual, gain 0.65 bits, evidence verified)
- [rejected] at `isolation_mechanism`: new value **power-cut volatile memory erasure** — Key material is held only in volatile memory and is erased when electrical power is interrupted, so it never persists to network-reachable storage. (supports 1 of 6 shown, est. 1 of 6 residual, gain 0.65 bits, evidence verified)
- [rejected] at `isolation_mechanism`: new value **distributed multi-party key separation** — Key material is split across separate remote encryption machines or servers linked by distinct communication channels so no single component holds the full key. (supports 1 of 6 shown, est. 1 of 6 residual, gain 0.65 bits, evidence verified)
- [rejected] at `asset_supply_policy`: new value **fixed supply with issuance schedule decline** — Native asset supply is capped and new issuance steadily decreases over time, e.g. via scheduled block reward halvings. (supports 3 of 21 shown, est. 3 of 21 residual, gain 0.5917 bits, evidence unverified)
- [rejected] at `asset_supply_policy`: new value **variable supply with monetary expansion** — Native asset supply can be increased or withdrawn by a central authority, enabling money printing and inflation or deflation. (supports 3 of 21 shown, est. 3 of 21 residual, gain 0.5917 bits, evidence verified)
- [rejected] at `key_custody_control_model`: new value **key-management ledger or traceable key record** — Key lifecycle, provenance, or usage is recorded on a blockchain so that key custody events are auditable. (supports 3 of 21 shown, est. 3 of 21 residual, gain 0.5917 bits, evidence verified)
- [rejected] at `cross_chain_interoperability_mechanism`: new value **permissionless relayer network** — Independent, permissionless relayers transport messages or data between blockchains, with multiple relayers working concurrently. (supports 3 of 22 shown, est. 3 of 22 residual, gain 0.5746 bits, evidence verified)
- [rejected] at `cross_chain_interoperability_mechanism`: new child_term_type **message transport layer** — Distinguishes how cross-chain messages are packaged, routed and verified in transit between chains. (supports 3 of 22 shown, est. 3 of 22 residual, gain 0.5746 bits, evidence verified); values: relayed data transport, adapter protocol translation, authenticable message protocol stack, lightweight event broadcast
- [rejected] at `cross_chain_interoperability_mechanism`: new value **federated or hierarchical multi-chain architecture** — Multiple chains are organised under a parent or federated structure that coordinates state transitions across them. (supports 3 of 22 shown, est. 3 of 22 residual, gain 0.5746 bits, evidence verified)
- [rejected] at `key_management_control_model`: new child_term_type **key_volatility_and_power_model** — Distinguishes whether keys are kept in volatile memory cleared on power-down, persistent secure hardware, or transient per-transaction material. (supports 2 of 7 shown, est. 2 of 7 residual, gain 0.5493 bits, evidence verified); values: volatile memory cleared on power-down, persistent secure element, transient per-transaction material
- [rejected] at `ledger_purpose`: new value **supply chain traceability and product provenance** —  (supports 5 of 40 shown, est. 132 of 1057 residual, gain 0.5432 bits, evidence unverified)
- [rejected] at `script_verification_approach`: new value **graph neural network vulnerability detection** — Verifies contract safety by learning vulnerability patterns from graph representations (AST, CFG, opcode graphs) with neural models. (supports 3 of 27 shown, est. 3 of 27 residual, gain 0.5033 bits, evidence verified)
- [rejected] at `script_verification_approach`: new value **zero-knowledge proof circuit verification** — Verifies computation correctness by compiling programs into arithmetic circuits and checking succinct cryptographic proofs of execution. (supports 3 of 27 shown, est. 3 of 27 residual, gain 0.5033 bits, evidence verified)
- [rejected] at `script_verification_approach`: new value **runtime enforcement via off-chain monitoring** — Checks conformance of contract behaviour against a specification at runtime through an external service or monitor that enforces it. (supports 3 of 27 shown, est. 3 of 27 residual, gain 0.5033 bits, evidence verified)
- [rejected] at `script_verification_approach`: new value **type-based interface checking** — Ensures correctness by statically checking interactions with a contract through typed interfaces and module specifications. (supports 3 of 27 shown, est. 3 of 27 residual, gain 0.5033 bits, evidence verified)
- [rejected] at `finality_mechanism`: new value **delayed trusted-authority confirmation** — Finality comes from a fast tentative inscription later bound to a highly trusted, delayed third-party confirmation. (supports 1 of 9 shown, est. 1 of 9 residual, gain 0.5033 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **software engineering / development tooling** — Smart contracts studied or built for code quality, bug detection, clones, or development workflows. (supports 4 of 37 shown, est. 4 of 37 residual, gain 0.4942 bits, evidence verified)
- [rejected] at `validator_selection_mechanism`: new value **credit or reputation-weighted leader or primary election** — Primary or leader is chosen by a credit, reputation, or reliability score rather than purely by fixed rotation or stake. (supports 4 of 38 shown, est. 4 of 38 residual, gain 0.4855 bits, evidence verified)
- [rejected] at `validator_selection_mechanism`: new value **random sampling of a committee or shard subset** — A subset of nodes is randomly sampled to form a committee or shard that performs verification for a round. (supports 4 of 38 shown, est. 4 of 38 residual, gain 0.4855 bits, evidence verified)
- [rejected] at `identity_binding_mechanism`: new value **soulbound token identity** — Identity is bound to the participant via a non-transferable token permanently associated with the holder's wallet or account. (supports 4 of 40 shown, est. 21 of 206 residual, gain 0.4751 bits, evidence unverified)
- [rejected] at `interoperability_type`: new value **cross-chain asset transfer** — Ledger interoperability realised by moving tokens or assets between distinct blockchains, typically via locking, escrow, or burning and minting. (supports 4 of 40 shown, est. 6 of 61 residual, gain 0.4638 bits, evidence verified)
- [rejected] at `ledger_partitioning_topology`: new value **coordination chain over private sidechains** — A public or shared coordination blockchain that orchestrates activities across multiple private blockchains or sidechains. (supports 4 of 40 shown, est. 14 of 138 residual, gain 0.4446 bits, evidence verified)
- [rejected] at `ledger_partitioning_topology`: new value **parallel block production over disjoint transaction sets** — Single or multi-chain design where blocks are produced concurrently by consensus groups over disjoint transaction partitions. (supports 4 of 40 shown, est. 14 of 138 residual, gain 0.4446 bits, evidence verified)
- [rejected] at `key_splitting_scheme`: new child_term_type **Signature authorization policy** — Specifies how multiple signers or verifiers must combine to authorize a signing operation, distinct from how the key itself is divided. (supports 4 of 8 shown, est. 4 of 8 residual, gain 0.4211 bits, evidence unverified); values: m-of-n signatures from independent keys, sequential signature chain, verifier or third-party approval required, signer plus co-signer by policy
- [rejected] at `interoperability_type`: new value **payment channel network routing** — Off-chain multi-hop payment routing across channels linking users, used to interoperate or scale value transfer without on-chain settlement. (supports 3 of 40 shown, est. 5 of 61 residual, gain 0.4091 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **coordination or sidechain anchoring** — A ledger coordinating or anchoring several private or sidechain ledgers through a shared public or parent chain. (supports 3 of 40 shown, est. 5 of 61 residual, gain 0.4091 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **relayer-based message passing** — Cross-chain messages carried between ledgers by permissionless or permissioned relayer applications, rather than by a native protocol. (supports 3 of 40 shown, est. 5 of 61 residual, gain 0.4091 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **energy / utilities** — Smart contracts deployed for energy trading, EV charging, or power grid coordination. (supports 3 of 37 shown, est. 3 of 37 residual, gain 0.406 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **public sector / government** — Smart contracts deployed for government data sharing, e-governance, or public administration services. (supports 3 of 37 shown, est. 3 of 37 residual, gain 0.406 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **charity / donations / crowdfunding** — Smart contracts deployed for charitable giving, donations, or crowdfunding campaigns. (supports 3 of 37 shown, est. 3 of 37 residual, gain 0.406 bits, evidence verified)
- [rejected] at `key_splitting_scheme`: new value **multi-signature (multiple independent signatures required)** — Transaction requires several independent signatures, each from a separately held full private key, rather than a split of one key. (supports 3 of 8 shown, est. 3 of 8 residual, gain 0.4019 bits, evidence verified)
- [rejected] at `key_splitting_scheme`: new value **physical token or certificate held as second factor** — Signing authority is split between a digital key and a physical off-chain artifact such as a paper certificate or code. (supports 3 of 8 shown, est. 3 of 8 residual, gain 0.4019 bits, evidence verified)
- [rejected] at `anonymity_enhancing_status`: new child_term_type **Crypto-asset privacy-typology dimension** — Splits anonymity arising from the asset's own protocol from anonymity obtained by external mixing, tumbling or laundering services used on a transparent ledger. (supports 3 of 8 shown, est. 3 of 8 residual, gain 0.4019 bits, evidence verified); values: protocol-level privacy by design, third-party mixing or tumbling service, no anonymity mechanism
- [rejected] at `anonymity_enhancing_status`: new value **Privacy-focused coin subject to comparative price analysis** — Asset positioned explicitly as a privacy coin whose market value is studied relative to a transparent benchmark coin. (supports 3 of 8 shown, est. 3 of 8 residual, gain 0.4019 bits, evidence verified)
- [rejected] at `smart_contract_usage_domain`: new value **insurance products and policies** — Smart contracts designed to underwrite, administer, or settle insurance products and policies. (supports 3 of 40 shown, est. 32 of 426 residual, gain 0.3847 bits, evidence verified)
- [rejected] at `smart_contract_usage_domain`: new value **electric vehicle charging and mobility** — Ledger applications for EV charging station management, charging rights trading, and related mobility services. (supports 3 of 40 shown, est. 32 of 426 residual, gain 0.3847 bits, evidence verified)
- [rejected] at `smart_contract_usage_domain`: new value **pharmaceutical and health product tracking** — Ledger applications tracking medical products, drugs, or vaccines through their lifecycle. (supports 3 of 40 shown, est. 32 of 426 residual, gain 0.3847 bits, evidence verified)
- [rejected] at `ledger_purpose`: new value **electronic health and medical record management** —  (supports 3 of 40 shown, est. 79 of 1057 residual, gain 0.3834 bits, evidence unverified)
- [rejected] at `key_management_control_model`: new value **multi-node-assisted public key rotation** — Signing authority is migrated to a new public key with the help of a separate service or node group that coordinates the old-to-new key handover. (supports 1 of 7 shown, est. 1 of 7 residual, gain 0.3765 bits, evidence verified)
- [rejected] at `centralisation_locus`: new value **network_or_connectivity_infrastructure** — Centralisation of the peer-to-peer network layer, such as routing paths, relay proxies, or dependence on a few network providers. (supports 3 of 40 shown, est. 5 of 70 residual, gain 0.3712 bits, evidence verified)
- [rejected] at `centralisation_locus`: new value **ai_model_or_development** — Centralisation of control over the development, training, or deployment of AI or software systems by a few organisations. (supports 3 of 40 shown, est. 5 of 70 residual, gain 0.3712 bits, evidence verified)
- [rejected] at `privacy_mechanism_family`: new value **data erasure via key deletion** — Confidentiality or the right to be forgotten is achieved by destroying or deleting the encryption key so stored ciphertext becomes unrecoverable. (supports 3 of 40 shown, est. 8 of 103 residual, gain 0.3688 bits, evidence verified)
- [rejected] at `consensus_finality`: new value **conditional (synchrony-dependent) finality** — Finality holds only under bounded network delay or partial synchrony and may fail or stall otherwise. (supports 3 of 26 shown, est. 3 of 26 residual, gain 0.344 bits, evidence verified)
- [rejected] at `native_vs_token_standard`: new value **NFT (non-fungible token) as a general asset type** — Crypto-asset referred to generically as an NFT or non-fungible token, without specifying the underlying token standard. (supports 4 of 40 shown, est. 6 of 63 residual, gain 0.3212 bits, evidence verified)
- [rejected] at `native_vs_token_standard`: new child_term_type **Ledger deployment scope** — Distinguishes assets confined to one ledger from those spanning public/private ledgers or multiple chains. (supports 4 of 40 shown, est. 6 of 63 residual, gain 0.3212 bits, evidence verified); values: single ledger, multiple ledgers / multi-chain, public-private dual ledger
- [rejected] at `centralisation_level`: new value **decentralised with central trusted authority** — Asset or system is described as decentralised in its core operation but relies on a designated central authority for specific functions such as oversight, clearing, or record auditing. (supports 4 of 40 shown, est. 20 of 195 residual, gain 0.303 bits, evidence verified)
- [rejected] at `centralisation_level`: new child_term_type **Governance model** — Distinguishes the mechanism through which the asset or system's governance decisions are taken. (supports 4 of 40 shown, est. 20 of 195 residual, gain 0.303 bits, evidence unverified); values: on-chain token voting, foundation or company led, community or DAO, designated operator or consortium, no governance
- [rejected] at `unhosted_vs_hosted_wallet`: new child_term_type **wallet_identity_linkage** — Whether a crypto-asset wallet or address is tied to a verified real-world identity, and which party holds that identity linkage. (supports 3 of 16 shown, est. 3 of 16 residual, gain 0.2785 bits, evidence verified); values: pseudonymous (no identity link), identity held by VASP/custodian, identity held by issuer or credential authority, identity held in private/zero-knowledge proof, aggregated multi-chain identity
- [rejected] at `unhosted_vs_hosted_wallet`: new value **managed/meta-transactional wallet** — A wallet whose account is managed by a service provider that submits transactions on the user's behalf while the user interacts via a managed account. (supports 3 of 16 shown, est. 3 of 16 residual, gain 0.2785 bits, evidence verified)
- [rejected] at `wallet_type_storage`: new child_term_type **Wallet trust and security model** — Whether the wallet's security depends on tamper-resistant hardware, software safeguards, or other protective assurances rather than storage connectivity alone. (supports 3 of 9 shown, est. 3 of 9 residual, gain 0.2755 bits, evidence verified); values: tamper-resistant hardware, software-only safeguards, formally verified protocol, no specific security mechanism
- [rejected] at `wallet_type_storage`: new value **cloud or exchange-hosted wallet** — Wallet whose keys are held by a remote cloud service or exchange rather than the user device. (supports 3 of 9 shown, est. 3 of 9 residual, gain 0.2755 bits, evidence verified)
- [rejected] at `privacy_enhancement`: new child_term_type **privacy_protection_target** — Whether the mechanism hides transaction amounts, sender or receiver identity, linkability between transactions, or user data and personal identifiers. (supports 5 of 40 shown, est. 10 of 82 residual, gain 0.1976 bits, evidence unverified); values: transaction amount, sender or receiver identity, transaction linkability, personal data or identifiers, network-level metadata
- [rejected] at `privacy_enhancement`: new value **privacy-preserving identity or credential scheme** — Anonymity is provided through pseudonyms, anonymous credentials or zero-knowledge proofs applied to identity rather than to ledger transactions. (supports 4 of 40 shown, est. 8 of 82 residual, gain 0.1704 bits, evidence verified)
- [rejected] at `script_language_expressiveness`: new value **bytecode-compiled execution (AoT)** — Contract logic is compiled ahead-of-time to bytecode executed by a virtual machine, distinct from interpreted or Turing-complete scripting. (supports 3 of 40 shown, est. 6 of 75 residual, gain 0.1501 bits, evidence verified)