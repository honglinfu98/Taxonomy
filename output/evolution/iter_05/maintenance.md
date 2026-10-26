# Part 2 maintenance: the DAG as label space

8646 tagged items placed on 123/124 nodes (35392 tags, 165143 closure placements).

## Objectives: content-driven vs Part 1 prior

| metric | from tags (empirical) | from is-a weights (Part 1) |
|---|---|---|
| bits per descent (information gain) | 7.2712 | 5.0082 |
| AUC of reach-a-leaf | 0.7734 | 0.8332 |
| expected depth | 3.8959 | 3.0022 |
| effective leaves | 24.792 | 25.719 |
| effective leaves / nodes | 0.1999 | 0.2074 |

## Where descents stop (top stop mass)

- Ledger purpose `ledger_purpose`: 0.2217
- Smart contract usage domain `smart_contract_usage_domain`: 0.1025
- Native asset versus token standard `native_vs_token_standard`: 0.084
- Privacy mechanism family `privacy_mechanism_family`: 0.0434
- Centralisation of control `centralisation_level`: 0.0415
- Identity binding mechanism `identity_binding_mechanism`: 0.0393
- Key custody and control model `key_custody_control_model`: 0.0375
- Interoperability and intraoperability `interoperability_type`: 0.0361
- Smart contract / script language expressiveness `script_language_expressiveness`: 0.0274
- Cross-chain interoperability mechanism `cross_chain_interoperability_mechanism`: 0.0262
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 0.0251
- Privacy and anonymity features `privacy_enhancement`: 0.0245
- Smart contract / distributed ledger application scope `smart_contract_definition_scope`: 0.0232
- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`: 0.021
- Validator selection mechanism `validator_selection_mechanism`: 0.0179

## Node statistics (nodes with items, by closure size)

| node | cat | direct | closure | children | value entropy | dominance | branching gain | residual |
|---|---|---|---|---|---|---|---|---|
| Crypto-asset definitional criteria | asset | 662 | 7078 | 10 | 1.02 | 0.601 | 2.3959 | 81 (0.011) |
| Economic function of the asset | asset | 1057 | 6997 | 9 | 1.446 | 0.663 | 2.7707 | 157 (0.022) |
| Legal classification of crypto-asset | asset | 106 | 6840 | 11 | 0.9628 | 0.766 | 2.7196 | 33 (0.005) |
| Reference asset type | asset | 301 | 6806 | 7 | 1.7156 | 0.603 | 2.2755 | 79 (0.012) |
| Issuer identifiability | asset | 52 | 6699 | 6 | 0.55 | 0.904 | 1.471 | 2 (0.0) |
| Payment stablecoin / e-money / ART reg | asset | 25 | 6697 | 3 | 1.9943 | 0.4 | 0.839 | 7 (0.001) |
| Convertible virtual currency (CVC) sta | asset | 73 | 6351 | 1 | 0.1044 | 0.986 | 0.0493 | 35 (0.006) |
| Recording and cryptographic linkage | asset | 1752 | 6316 | 6 | 0.2342 | 0.962 | 1.733 | 389 (0.062) |
| Governance model of a DLT system | techn | 436 | 6308 | 8 | 1.6213 | 0.561 | 2.758 | 48 (0.008) |
| Ledger access and permissioning | techn | 1611 | 6260 | 14 | 1.6318 | 0.393 | 3.4089 | 115 (0.018) |
| Ledger scope: open or closed access by | techn | 379 | 6145 | 5 | 1.5044 | 0.421 | 2.003 | 75 (0.012) |
| Network topology and node roles | techn | 1072 | 6070 | 7 | 1.08 | 0.644 | 2.3673 | 103 (0.017) |
| Consensus mechanism | techn | 1223 | 5942 | 6 | 1.6746 | 0.433 | 2.3751 | 240 (0.04) |
| Validator reward mechanism | techn | 226 | 5702 | 4 | 0.4526 | 0.925 | 1.1653 | 58 (0.01) |
| Transaction fee regime | techn | 94 | 5644 | 2 | 1.9732 | 0.495 | 0.1051 | 16 (0.003) |
| Native asset presence and type | techn | 212 | 5628 | 4 | 0.9668 | 0.755 | 1.3396 | 41 (0.007) |
| Software architecture (monolithic vs p | techn | 179 | 5563 | 5 | 0.9539 | 0.626 | 2.1244 | 43 (0.008) |
| Ledger storage model (what is stored o | techn | 651 | 5517 | 3 | 1.3658 | 0.645 | 1.5007 | 121 (0.022) |
| Ledger purpose | techn | 5447 | 5447 | 0 | 2.5416 | 0.365 | -0.0 | 5447 (1.0) |
| DLT data structure (blockchain vs non- | techn | 1813 | 4135 | 4 | 0.313 | 0.954 | 1.7344 | 1062 (0.257) |
| Node / DLT network node role | techn | 748 | 2827 | 1 | 2.0956 | 0.337 | 0.7335 | 582 (0.206) |
| Decentralised system certification | techn | 74 | 2663 | 2 | 1.5774 | 0.382 | 0.8536 | 46 (0.017) |
| Source code openness | techn | 21 | 2617 | 2 | 0.7025 | 0.81 | 0.4715 | 7 (0.003) |
| Smart contract / distributed ledger ap | techn | 1443 | 2409 | 2 | 1.1886 | 0.592 | 1.3465 | 363 (0.151) |
| Information and communications technol | techn | 77 | 2245 | 3 | 0.1 | 0.987 | 1.5768 | 59 (0.026) |
| Identity layer and onboarding | techn | 764 | 2185 | 3 | 0.6263 | 0.843 | 1.6773 | 234 (0.107) |
| Redemption mechanism | asset | 33 | 2181 | 4 | 1.8084 | 0.424 | 1.7159 | 3 (0.001) |
| Form of holder claim | asset | 41 | 2178 | 4 | 1.3508 | 0.61 | 1.6081 | 6 (0.003) |
| Smart contract usage domain | techn | 1608 | 1608 | 0 | 2.8442 | 0.254 | -0.0 | 1608 (1.0) |
| Source of yield | asset | 64 | 1538 | 1 | 1.4346 | 0.477 | 0.184 | 43 (0.028) |
| Yield distribution mechanism | asset | 18 | 1495 | 1 | 0.9142 | 0.833 | 0.0627 | 11 (0.007) |
| Centralisation of control | asset | 984 | 1484 | 3 | 1.5456 | 0.461 | 1.429 | 881 (0.594) |
| Identity binding mechanism | techn | 1139 | 1139 | 0 | 2.503 | 0.425 | -0.0 | 1139 (1.0) |
| Data classification (traffic, content, | techn | 2 | 1067 | 1 | -0.0 | 1.0 | 0.0108 | 1 (0.001) |
| Privacy and anonymity features | techn | 489 | 1066 | 2 | 0.9207 | 0.771 | 1.482 | 286 (0.268) |
| Tokenisation form | asset | 429 | 897 | 3 | 2.1622 | 0.304 | 1.5487 | 240 (0.268) |
| Smart contract / script language expre | techn | 391 | 739 | 4 | 0.8696 | 0.819 | 1.7434 | 294 (0.398) |
| Fungibility | asset | 347 | 675 | 1 | 0.7074 | 0.807 | 0.4074 | 55 (0.081) |
| Native asset versus token standard | asset | 481 | 620 | 1 | 1.2423 | 0.693 | 0.8311 | 457 (0.737) |
| Privacy mechanism family | techn | 564 | 567 | 1 | 2.0064 | 0.525 | 0.4872 | 507 (0.894) |
| Crypto-asset service provider or VASP  | actor | 124 | 562 | 16 | 1.8806 | 0.581 | 3.5905 | 92 (0.164) |
| Ledger partitioning or layering topolo | techn | 518 | 520 | 1 | 2.4169 | 0.296 | 0.363 | 484 (0.931) |
| Crypto-asset service type | activ | 220 | 479 | 10 | 2.3759 | 0.394 | 3.2003 | 121 (0.253) |
| Offshore VASP status (activity-based o | actor | 0 | 470 | 2 | - | - | 0.9999 | 0 (0.0) |
| Jurisdictional regime and home or host | actor | 18 | 470 | 5 | 1.2244 | 0.667 | 1.8839 | 11 (0.023) |
| Principal or agent role in transaction | actor | 14 | 459 | 8 | 1.9242 | 0.357 | 2.0902 | 9 (0.02) |
| Financial institution status for AML | actor | 1 | 459 | 3 | -0.0 | 1.0 | 0.1389 | 0 (0.0) |
| Custody model | actor | 52 | 449 | 6 | 1.799 | 0.474 | 2.3633 | 32 (0.071) |
| Trading venue type | actor | 35 | 405 | 1 | 1.7259 | 0.488 | 0.3439 | 26 (0.064) |
| Control or sufficient influence over D | actor | 7 | 379 | 3 | 0.9852 | 0.571 | 1.0876 | 5 (0.013) |
| Interoperability and intraoperability | techn | 304 | 304 | 0 | 2.4311 | 0.393 | -0.0 | 304 (1.0) |
| Centralisation locus | asset | 304 | 304 | 0 | 2.3095 | 0.31 | -0.0 | 304 (1.0) |
| Hosted versus unhosted (self-hosted) w | asset | 240 | 298 | 3 | 1.2349 | 0.576 | 1.6132 | 192 (0.644) |
| Transfer of crypto-assets (travel rule | activ | 38 | 270 | 8 | -0.0 | 1.0 | 2.7734 | 20 (0.074) |
| Infrastructure provider type | actor | 20 | 269 | 2 | 0.569 | 0.9 | 1.0852 | 12 (0.045) |
| Ecosystem participant role | actor | 127 | 257 | 4 | 2.2883 | 0.328 | 2.0157 | 124 (0.482) |
| Money transmission (acceptance and tra | activ | 3 | 250 | 5 | -0.0 | 1.0 | 2.0062 | 2 (0.008) |
| Permitted control over client assets ( | actor | 26 | 250 | 3 | 0.6219 | 0.885 | 1.3712 | 13 (0.052) |
| Public offer or private placement | activ | 18 | 248 | 3 | 0.6144 | 0.889 | 1.0068 | 3 (0.012) |
| Wallet storage mode (hot or cold) | techn | 75 | 247 | 1 | 1.3707 | 0.494 | 0.676 | 44 (0.178) |
| Offer and issuance method (token distr | activ | 43 | 245 | 3 | 1.0406 | 0.791 | 1.7981 | 34 (0.139) |
| Key custody and control model | techn | 203 | 203 | 0 | 1.5193 | 0.582 | -0.0 | 203 (1.0) |
| Wrapped / cross-chain representation | asset | 106 | 163 | 2 | 0.9687 | 0.604 | 1.3709 | 46 (0.282) |
| Finality of agreement | techn | 124 | 149 | 1 | 0.9566 | 0.622 | 0.8086 | 112 (0.752) |
| Peer-to-peer (P2P) transaction | activ | 13 | 147 | 1 | 0.3912 | 0.923 | 0.3323 | 9 (0.061) |
| Payment service and funds transfer | activ | 62 | 138 | 2 | -0.0 | 1.0 | 1.0523 | 22 (0.159) |
| Stablecoin issuer model | actor | 0 | 133 | 1 | - | - | -0.0 | 0 (0.0) |
| Operator of crypto-asset arrangement | actor | 4 | 133 | 2 | 0.8113 | 0.75 | 0.2583 | 4 (0.03) |
| Validator operation capacity (who may  | actor | 50 | 128 | 1 | 0.9044 | 0.68 | 0.8571 | 36 (0.281) |
| Smart contract deployment context | techn | 116 | 116 | 0 | 1.6869 | 0.624 | -0.0 | 116 (1.0) |
| Anti-money laundering obligations | oblig | 50 | 112 | 9 | 1.2865 | 0.647 | 2.2808 | 12 (0.107) |
| Payment settlement mechanism | activ | 83 | 108 | 2 | 1.9382 | 0.404 | 1.5753 | 37 (0.343) |
| Cross-chain interoperability mechanism | techn | 108 | 108 | 0 | 2.2213 | 0.301 | -0.0 | 108 (1.0) |
| Key splitting scheme | techn | 101 | 106 | 2 | 1.8789 | 0.431 | 1.3709 | 68 (0.642) |
| Virtual assets as property or proceeds | oblig | 1 | 100 | 7 | -0.0 | 1.0 | 1.9935 | 1 (0.01) |
| Key management control model | activ | 76 | 100 | 1 | 1.7427 | 0.494 | 0.9044 | 68 (0.68) |
| Freezing and blocking capability | oblig | 6 | 92 | 4 | -0.0 | 1.0 | 1.258 | 4 (0.043) |
| Validator selection mechanism | techn | 92 | 92 | 0 | 2.2118 | 0.286 | -0.0 | 92 (1.0) |
| Illicit finance risk category | oblig | 63 | 86 | 2 | 1.7101 | 0.493 | 1.0269 | 31 (0.36) |
| Staking arrangement (self, delegated,  | activ | 11 | 68 | 1 | 2.1887 | 0.333 | 0.5639 | 9 (0.132) |
| Zero-knowledge proof system variant | techn | 60 | 60 | 0 | 1.4599 | 0.574 | -0.0 | 60 (1.0) |
| Minting mechanism | activ | 59 | 59 | 0 | 2.5202 | 0.324 | -0.0 | 59 (1.0) |
| Asset supply management (monetary poli | techn | 54 | 54 | 0 | 0.8944 | 0.818 | -0.0 | 54 (1.0) |
| Anonymity-enhancing crypto-asset statu | oblig | 35 | 54 | 1 | 1.2907 | 0.639 | 0.8524 | 15 (0.278) |
| Wallet interface or delivery form | techn | 50 | 50 | 0 | 1.958 | 0.434 | -0.0 | 50 (1.0) |
| Fiat-rail integration | activ | 42 | 47 | 1 | 2.0978 | 0.349 | 0.6582 | 39 (0.83) |
| Backing of token | asset | 38 | 46 | 1 | 1.9758 | 0.308 | 0.9986 | 24 (0.522) |
| Key isolation from network connectivit | techn | 42 | 43 | 1 | 1.3777 | 0.511 | 0.6931 | 35 (0.814) |
| Script verification approach | techn | 42 | 42 | 0 | 1.7437 | 0.42 | -0.0 | 42 (1.0) |
| Central bank digital currency status | asset | 39 | 39 | 0 | 0.9257 | 0.659 | -0.0 | 39 (1.0) |
| Deanonymisation / tracing approach | oblig | 39 | 39 | 0 | 2.1738 | 0.318 | -0.0 | 39 (1.0) |
| Key recovery mechanism | techn | 38 | 38 | 0 | 2.1787 | 0.302 | -0.0 | 38 (1.0) |
| Finality mechanism | techn | 37 | 37 | 0 | 1.5845 | 0.595 | -0.0 | 37 (1.0) |
| Settlement finality timing | activ | 37 | 37 | 0 | 1.6256 | 0.568 | -0.0 | 37 (1.0) |
| Sharding partition basis | techn | 36 | 36 | 0 | 1.4688 | 0.528 | -0.0 | 36 (1.0) |
| Key share distribution topology | techn | 32 | 32 | 0 | 1.7927 | 0.406 | -0.0 | 32 (1.0) |
| Cross-chain transfer mechanism | asset | 29 | 29 | 0 | 1.723 | 0.448 | -0.0 | 29 (1.0) |
| Backing mechanism | asset | 22 | 22 | 0 | 1.7081 | 0.409 | -0.0 | 22 (1.0) |
| Share recovery mechanism | techn | 17 | 17 | 0 | 1.0224 | 0.765 | -0.0 | 17 (1.0) |
| Nexus to jurisdiction (services offere | activ | 14 | 14 | 0 | 0.8631 | 0.714 | -0.0 | 14 (1.0) |
| Ancillary asset and network token stat | asset | 10 | 10 | 0 | 0.971 | 0.6 | -0.0 | 10 (1.0) |
| Investment contract (Howey) criteria | oblig | 3 | 9 | 3 | 0.9183 | 0.667 | 1.9656 | 3 (0.333) |
| Security status of digital asset (US e | oblig | 0 | 9 | 2 | - | - | 0.9403 | 0 (0.0) |
| MiFID financial instrument status | oblig | 0 | 9 | 2 | - | - | 1.0 | 0 (0.0) |
| Excluded instrument category (EU scope | oblig | 0 | 9 | 4 | - | - | 1.9626 | 0 (0.0) |
| Reference currency for stablecoin peg  | asset | 8 | 8 | 0 | -0.0 | 1.0 | -0.0 | 8 (1.0) |
| Settlement counterparty | actor | 8 | 8 | 0 | 1.4056 | 0.5 | -0.0 | 8 (1.0) |
| Physical transfer mechanism across air | techn | 8 | 8 | 0 | 1.4355 | 0.556 | -0.0 | 8 (1.0) |
| Address linkage to service provider | actor | 0 | 6 | 1 | - | - | -0.0 | 0 (0.0) |
| Originator and beneficiary role | actor | 0 | 6 | 1 | - | - | -0.0 | 0 (0.0) |
| Consumer or retail versus professional | actor | 5 | 6 | 1 | -0.0 | 1.0 | 0.65 | 5 (0.833) |
| Redemption and reserve adequacy | oblig | 0 | 5 | 4 | - | - | 1.9772 | 0 (0.0) |
| Yield or interest on stablecoin | oblig | 0 | 5 | 2 | - | - | 0.9911 | 0 (0.0) |
| Settlement finality and legal enforcea | oblig | 1 | 5 | 3 | -0.0 | 1.0 | 1.8554 | 1 (0.2) |
| Prudential classification group (Basel | oblig | 1 | 4 | 1 | -0.0 | 1.0 | 0.8113 | 1 (0.25) |
| Traditional finance analogue | oblig | 0 | 4 | 1 | - | - | -0.0 | 0 (0.0) |
| Expressiveness claim basis | techn | 4 | 4 | 0 | 1.5 | 0.5 | -0.0 | 4 (1.0) |
| ICT and operational resilience risk | oblig | 1 | 3 | 1 | -0.0 | 1.0 | 0.9183 | 1 (0.333) |
| Exemption from MSB status | oblig | 1 | 3 | 2 | -0.0 | 1.0 | 0.9183 | 1 (0.333) |
| Pooled investment vehicle structure | actor | 2 | 2 | 0 | -0.0 | 1.0 | -0.0 | 2 (1.0) |
| Safeguarding and custody obligation | oblig | 2 | 2 | 0 | -0.0 | 1.0 | -0.0 | 2 (1.0) |
| Serious crime threshold for predicate  | oblig | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |
| Related person and affiliated person s | actor | 1 | 1 | 0 | -0.0 | 1.0 | -0.0 | 1 (1.0) |

## Maintenance proposals

**Dormant nodes (1)**, no items in this batch: `tax_reporting_status`

**Collapsed nodes (12)**, many items but one value absorbs them (merge or re-split candidates):
- Issuer identifiability `issuer_presence`: 52 items, dominance 0.904 (identifiable issuer)
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`: 1813 items, dominance 0.954 (blockchain (chain of blocks))
- Validator reward mechanism `reward_mechanism`: 226 items, dominance 0.925 (lump-sum reward)
- Infrastructure provider type `infrastructure_provider_type`: 20 items, dominance 0.9 (oracle)
- Peer-to-peer (P2P) transaction `transaction_type_p2p`: 13 items, dominance 0.923 (person-to-person transfer)
- Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`: 38 items, dominance 1.0 (transfer of crypto-assets (covered))
- Payment service and funds transfer `payment_or_transfer_service`: 62 items, dominance 1.0 (transfer of funds)
- Convertible virtual currency (CVC) status `convertible_virtual_currency_status`: 73 items, dominance 0.986 (convertible virtual currency (CVC))
- Recording and cryptographic linkage `digital_asset_recording`: 1752 items, dominance 0.962 (recorded on cryptographically secured distributed ledger)
- Information and communications technology system `ict_system_scope`: 77 items, dominance 0.987 (ICT / computer system)
- Permitted control over client assets (unilateral vs multi-party control) `unhosted_custody_control_policy`: 26 items, dominance 0.885 (multi-party or multi-signature control)
- Public offer or private placement `decentralised_or_centralised_offer_model`: 18 items, dominance 0.889 (offer to the public)

**Highest-gain nodes**:
- Crypto-asset service provider or VASP status `service_provider_status`: 3.5905 bits over 562 items
- Ledger access and permissioning `ledger_access_permission`: 3.4089 bits over 6260 items
- Crypto-asset service type `crypto_asset_service_type`: 3.2003 bits over 479 items
- Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`: 2.7734 bits over 270 items
- Economic function of the asset `crypto_asset_function`: 2.7707 bits over 6997 items
- Governance model of a DLT system `governance_model`: 2.758 bits over 6308 items
- Legal classification of crypto-asset `legal_classification_status`: 2.7196 bits over 6840 items
- Crypto-asset definitional criteria `crypto_asset_scope_criteria`: 2.3959 bits over 7078 items

**Discovery targets (45)**, residual >= threshold:
- Ledger purpose `ledger_purpose`: 5447 residual of 5447 (1.0)
- Smart contract usage domain `smart_contract_usage_domain`: 1608 residual of 1608 (1.0)
- Identity binding mechanism `identity_binding_mechanism`: 1139 residual of 1139 (1.0)
- Centralisation of control `centralisation_level`: 881 residual of 1484 (0.594)
- Privacy mechanism family `privacy_mechanism_family`: 507 residual of 567 (0.894)
- Ledger partitioning or layering topology `ledger_partitioning_topology`: 484 residual of 520 (0.931)
- Native asset versus token standard `native_vs_token_standard`: 457 residual of 620 (0.737)
- Interoperability and intraoperability `interoperability_type`: 304 residual of 304 (1.0)
- Centralisation locus `centralisation_locus`: 304 residual of 304 (1.0)
- Smart contract / script language expressiveness `script_language_expressiveness`: 294 residual of 739 (0.398)
- Key custody and control model `key_custody_control_model`: 203 residual of 203 (1.0)
- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`: 192 residual of 298 (0.644)
- Ecosystem participant role `ecosystem_participant_role`: 124 residual of 257 (0.482)
- Smart contract deployment context `smart_contract_deployment_context`: 116 residual of 116 (1.0)
- Finality of agreement `consensus_finality`: 112 residual of 149 (0.752)
- Cross-chain interoperability mechanism `cross_chain_interoperability_mechanism`: 108 residual of 108 (1.0)
- Validator selection mechanism `validator_selection_mechanism`: 92 residual of 92 (1.0)
- Key splitting scheme `key_splitting_scheme`: 68 residual of 106 (0.642)
- Key management control model `key_management_control_model`: 68 residual of 100 (0.68)
- Zero-knowledge proof system variant `zk_proof_system_variant`: 60 residual of 60 (1.0)
- Minting mechanism `minting_mechanism`: 59 residual of 59 (1.0)
- Asset supply management (monetary policy) `asset_supply_policy`: 54 residual of 54 (1.0)
- Wallet interface or delivery form `wallet_interface_delivery_form`: 50 residual of 50 (1.0)
- Script verification approach `script_verification_approach`: 42 residual of 42 (1.0)
- Central bank digital currency status `central_bank_digital_currency`: 39 residual of 39 (1.0)
- Fiat-rail integration `fiat_rail_integration`: 39 residual of 47 (0.83)
- Deanonymisation / tracing approach `deanonymisation_tracing_approach`: 39 residual of 39 (1.0)
- Key recovery mechanism `key_recovery_mechanism`: 38 residual of 38 (1.0)
- Finality mechanism `finality_mechanism`: 37 residual of 37 (1.0)
- Payment settlement mechanism `payment_settlement_mechanism`: 37 residual of 108 (0.343)
- Settlement finality timing `settlement_finality_timing`: 37 residual of 37 (1.0)
- Sharding partition basis `sharding_partition_basis`: 36 residual of 36 (1.0)
- Key isolation from network connectivity `key_isolation_from_network`: 35 residual of 43 (0.814)
- Key share distribution topology `key_share_distribution_topology`: 32 residual of 32 (1.0)
- Illicit finance risk category `risk_type_illicit_finance`: 31 residual of 86 (0.36)
- Cross-chain transfer mechanism `cross_chain_transfer_mechanism`: 29 residual of 29 (1.0)
- Backing of token `backing_of_token`: 24 residual of 46 (0.522)
- Backing mechanism `backing_mechanism`: 22 residual of 22 (1.0)
- Share recovery mechanism `share_recovery_mechanism`: 17 residual of 17 (1.0)
- Nexus to jurisdiction (services offered in jurisdiction) `service_location_nexus`: 14 residual of 14 (1.0)
- Ancillary asset and network token status `ancillary_asset_status`: 10 residual of 10 (1.0)
- Reference currency for stablecoin peg (currency vs other) `native_vs_stable_price_reference_asset_currency`: 8 residual of 8 (1.0)
- Settlement counterparty `settlement_counterparty`: 8 residual of 8 (1.0)
- Physical transfer mechanism across air gap `physical_transfer_mechanism_air_gap`: 8 residual of 8 (1.0)
- Consumer or retail versus professional user `consumer_vs_professional_status`: 5 residual of 6 (0.833)

## Discovery (Task E) candidates

- [ACCEPTED] at `service_location_nexus`: new value **physical point-of-sale or kiosk deployment in jurisdiction** — Crypto-asset services delivered through physical terminals, kiosks or ATMs located in the jurisdiction, creating a local nexus. (supports 5 of 14 shown, est. 5 of 14 residual, gain 0.9403 bits, evidence verified)
- [ACCEPTED] at `backing_mechanism`: new value **tokenized real-world asset in vault or escrow** — Backing asset is a physical or real-world item held in a vault, escrow account, or custodial store and represented one-to-one by an on-chain token. (supports 5 of 22 shown, est. 5 of 22 residual, gain 0.7732 bits, evidence verified)
- [ACCEPTED] at `key_custody_control_model`: new value **multi-party cryptographic co-signing of redemption** — Signing authority is split across parties via MPC or threshold signatures, with no single party holding a complete key, specifically for redeeming or transferring assets. (supports 8 of 40 shown, est. 41 of 203 residual, gain 0.7259 bits, evidence verified)
- [ACCEPTED] at `key_isolation_from_network`: new child_term_type **isolation_mechanism** — Specifies the hardware or logical mechanism that keeps keys separated from network-exposed processing, such as secure elements, enclaves, or HSMs. (supports 7 of 35 shown, est. 7 of 35 residual, gain 0.5876 bits, evidence verified); values: secure element/chip, trusted execution environment or secure enclave, hardware security module, network-disabled device, software-only isolation
- [ACCEPTED] at `zk_proof_system_variant`: new value **zk-SNARK with trusted setup** — Succinct non-interactive argument of knowledge whose construction requires a trusted setup ceremony for common reference string generation. (supports 5 of 40 shown, est. 8 of 60 residual, gain 0.5665 bits, evidence verified)
- [ACCEPTED] at `key_recovery_mechanism`: new value **recovery key / escrow-based recovery** — Recovery is performed by a dedicated recovery key or escrowed key held separately from the owner keys and used to re-authorise or re-encrypt access. (supports 5 of 38 shown, est. 5 of 38 residual, gain 0.5618 bits, evidence verified)
- [ACCEPTED] at `validator_selection_mechanism`: new value **capability-score threshold plus random selection** — Nodes are first filtered by a computed capability, credit, or trust score threshold, then selected randomly from the qualifying set. (supports 5 of 40 shown, est. 12 of 92 residual, gain 0.5586 bits, evidence verified)
- [ACCEPTED] at `validator_selection_mechanism`: new value **score-based endorsement** — Nodes are chosen to form a committee or endorse blocks according to an aggregated trust, credit, or evaluation score computed by peers. (supports 5 of 40 shown, est. 12 of 92 residual, gain 0.5586 bits, evidence verified)
- [ACCEPTED] at `validator_selection_mechanism`: new value **shareholder or bid-based voting** — Validators are chosen by votes or bids weighted by shares, tokens, or auction offers held by candidate nodes. (supports 5 of 40 shown, est. 12 of 92 residual, gain 0.5586 bits, evidence verified)
- [ACCEPTED] at `cross_chain_interoperability_mechanism`: new value **notary or multi-signature attestation** — Cross-chain state or value is moved via a committee, notary group, or threshold signature attesting to source-chain events. (supports 5 of 40 shown, est. 14 of 108 residual, gain 0.5564 bits, evidence verified)
- [ACCEPTED] at `cross_chain_interoperability_mechanism`: new value **hashed timelock contract (HTLC) swap** — Assets are exchanged across chains using hashlocks and timelocks so that either both transfers complete or neither does. (supports 5 of 40 shown, est. 14 of 108 residual, gain 0.5564 bits, evidence verified)
- [ACCEPTED] at `deanonymisation_tracing_approach`: new value **graph neural network representation learning** — Learns node or subgraph embeddings from transaction graphs with neural architectures such as GNNs, GAT, or attention models to classify addresses. (supports 5 of 39 shown, est. 5 of 39 residual, gain 0.5525 bits, evidence verified)
- [ACCEPTED] at `interoperability_type`: new value **external data oracle relay** — Ledger obtains external or cross-chain state via a dedicated oracle or relay that verifies source-chain data for the target chain. (supports 5 of 40 shown, est. 38 of 304 residual, gain 0.5436 bits, evidence verified)
- [ACCEPTED] at `smart_contract_usage_domain`: new value **supply chain traceability and provenance** — Ledger applications that track goods, food, or pharmaceuticals across supply chain stages to verify origin and authenticity. (supports 5 of 40 shown, est. 201 of 1608 residual, gain 0.5436 bits, evidence verified)
- [ACCEPTED] at `smart_contract_usage_domain`: new value **peer-to-peer energy trading** — Ledger applications enabling prosumers and consumers to trade electricity directly, often via auctions or microgrid markets. (supports 5 of 40 shown, est. 201 of 1608 residual, gain 0.5436 bits, evidence verified)
- [ACCEPTED] at `identity_binding_mechanism`: new value **DID-anchored verifiable credential** —  (supports 5 of 40 shown, est. 142 of 1139 residual, gain 0.5426 bits, evidence verified)
- [ACCEPTED] at `script_verification_approach`: new value **deductive / theorem-proving verification** — Correctness is established by interactive or automated proof assistants reasoning over the code's semantics with Hoare logic, invariants, or weakest preconditions. (supports 5 of 40 shown, est. 5 of 42 residual, gain 0.5266 bits, evidence verified)
- [ACCEPTED] at `ledger_partitioning_topology`: new value **main-chain with slave/side-chain attached** — A primary chain with one or more subsidiary chains that are anchored to or validated through the mainchain. (supports 5 of 40 shown, est. 60 of 484 residual, gain 0.5032 bits, evidence verified)
- [ACCEPTED] at `key_isolation_from_network`: new child_term_type **key_distribution_method** — Describes the channel used to carry keys, signatures, or transaction data across the isolation boundary. (supports 5 of 35 shown, est. 5 of 35 residual, gain 0.4816 bits, evidence verified); values: QR code or optical, USB or wired cable, NFC or contactless, Bluetooth or wireless short-range, manual entry or paper
- [ACCEPTED] at `consensus_finality`: new child_term_type **Finality guarantee mode** — Describes the form of finality a protocol provides: absolute, probabilistic with confirmation depth, or conditional on a quorum or synchrony assumption. (supports 5 of 40 shown, est. 14 of 112 residual, gain 0.4086 bits, evidence verified); values: absolute finality, probabilistic finality, quorum-conditional finality, no finality (forks possible)
- [ACCEPTED] at `key_management_control_model`: new value **key-derivation from parent key or device-bound seed** — Signing authority is controlled by deriving child or wallet keys from a parent key, seed, or physically unclonable function response rather than storing a standalone key. (supports 5 of 40 shown, est. 8 of 68 residual, gain 0.3553 bits, evidence verified)
- [ACCEPTED] at `unhosted_vs_hosted_wallet`: new child_term_type **key_splitting_scheme** — Describes whether and how a private key is fragmented, shared, or held in a single location. (supports 5 of 40 shown, est. 24 of 192 residual, gain 0.3231 bits, evidence verified); values: single whole key, fragmented / secret-shared key, multi-signature across parties, threshold signature across devices, key derived from biometrics or hardware
- [ACCEPTED] at `key_splitting_scheme`: new child_term_type **Key share cryptographic primitive** — Distinguishes the mathematical scheme underlying the key split, such as Shamir secret sharing, threshold signatures, or MPC protocols. (supports 5 of 40 shown, est. 8 of 68 residual, gain 0.3037 bits, evidence verified); values: Shamir secret sharing, threshold ECDSA/signature scheme, MPC protocol, identity-based or threshold encryption, Merkle-tree or hash-based key management
- [ACCEPTED] at `script_language_expressiveness`: new value **Bitcoin script with transaction-chaining state machine** — Restricted base script whose expressiveness is extended by chaining transactions to emulate state machines or complex logic across multiple transactions. (supports 5 of 40 shown, est. 37 of 294 residual, gain 0.2112 bits, evidence verified)
- [rejected] at `settlement_counterparty`: new child_term_type **settlement rail** — Classifies the infrastructure over which fiat funds are actually moved to the merchant or seller. (supports 4 of 8 shown, est. 4 of 8 residual, gain 1.0 bits, evidence verified); values: card network clearing, bank wire or ACH, blockchain ledger, payment platform balance, unspecified or not described
- [rejected] at `settlement_counterparty`: new value **blockchain ledger network** — The fiat settlement or value transfer is carried out by a distributed ledger network or its treasury accounts rather than by a bank or payment platform. (supports 3 of 8 shown, est. 3 of 8 residual, gain 0.9544 bits, evidence verified)
- [rejected] at `settlement_counterparty`: new value **zero-knowledge or proof-based issuer** — Settlement is authorized and verified by a cryptographic proof exchanged among customer, merchant, and issuer, with funds moved by the issuer system. (supports 3 of 8 shown, est. 3 of 8 residual, gain 0.9544 bits, evidence verified)
- [rejected] at `physical_transfer_mechanism_air_gap`: new value **machine-readable code display (QR-based)** — Data crosses the boundary as QR or other machine-readable codes displayed on one device and scanned by the other, which is already partly covered by optical codes but is one-directional or multi-step in these texts. (supports 3 of 8 shown, est. 3 of 8 residual, gain 0.9544 bits, evidence verified)
- [rejected] at `physical_transfer_mechanism_air_gap`: new value **secure isolated chamber / enclosure** — Data is transferred within or through a physically enclosed isolation chamber or sealed hardware module rather than a discrete transfer medium. (supports 3 of 8 shown, est. 3 of 8 residual, gain 0.9544 bits, evidence verified)
- [rejected] at `physical_transfer_mechanism_air_gap`: new child_term_type **transfer direction across boundary** — Distinguishes whether data flows only into the key device, only out of it, or in both directions across the air gap. (supports 3 of 8 shown, est. 3 of 8 residual, gain 0.9544 bits, evidence verified); values: inbound only, outbound only, bidirectional, none
- [rejected] at `ancillary_asset_status`: new child_term_type **Token issuance and minting trigger** — Classifies how new tokens come into existence, such as on-demand minting, event-triggered minting, or pre-sale allocation. (supports 3 of 10 shown, est. 3 of 10 residual, gain 0.8813 bits, evidence verified); values: event-triggered minting, on-demand minting, pre-sale allocation, mining or validation reward, not applicable
- [rejected] at `consumer_vs_professional_status`: new value **investor / speculative holder** — Person acquiring crypto-assets primarily for investment or speculative return rather than consumption or trade. (supports 3 of 5 shown, est. 3 of 5 residual, gain 0.8091 bits, evidence verified)
- [rejected] at `service_location_nexus`: new value **unregulated or unlicensed local market activity** — Crypto-asset trading or pricing occurring in a jurisdiction with no applicable regulation, so nexus is contested or absent. (supports 3 of 14 shown, est. 3 of 14 residual, gain 0.7496 bits, evidence verified)
- [rejected] at `share_recovery_mechanism`: new value **distributed seed phrase portion recombination** — Recovery by retrieving a necessary and sufficient number of portions of a seed phrase stored across multiple devices. (supports 3 of 17 shown, est. 3 of 17 residual, gain 0.6723 bits, evidence verified)
- [rejected] at `share_recovery_mechanism`: new value **co-signer or backup key recovery** — Recovery of a lost key using a recovery key, recovery signer, or backup key held by a separate party or service. (supports 3 of 17 shown, est. 3 of 17 residual, gain 0.6723 bits, evidence verified)
- [rejected] at `share_recovery_mechanism`: new value **child key derivation reconstruction** — Recovery of a parent key from child keys derived from it, so that the child set collectively enables reconstruction. (supports 3 of 17 shown, est. 3 of 17 residual, gain 0.6723 bits, evidence verified)
- [rejected] at `cross_chain_transfer_mechanism`: new value **hashlock/timelock atomic swap (HTLC)** — Atomic exchange enforced by hashlocks and timelocks, not by a bridge custodian or minted representation. (supports 4 of 29 shown, est. 4 of 29 residual, gain 0.5788 bits, evidence verified)
- [rejected] at `cross_chain_transfer_mechanism`: new value **burn-and-mint transfer** — Asset is destroyed on the origin chain and a corresponding asset is minted on the destination chain. (supports 4 of 29 shown, est. 4 of 29 residual, gain 0.5788 bits, evidence verified)
- [rejected] at `backing_mechanism`: new value **cryptoasset-backed via staking or bridge** — Token is backed by cryptoassets locked or staked on another blockchain or in a smart contract rather than off-chain reserves. (supports 3 of 22 shown, est. 3 of 22 residual, gain 0.5746 bits, evidence verified)
- [rejected] at `cross_chain_interoperability_mechanism`: new value **lock-and-mint or burn-and-mint asset representation** — Tokens are locked or burned on the source chain and an equivalent representation is minted on the target chain. (supports 5 of 40 shown, est. 14 of 108 residual, gain 0.5564 bits, evidence unverified)
- [rejected] at `key_share_distribution_topology`: new value **among threshold-vault participants** — Key shares are held by parties in a threshold vault or multi-party computation scheme, with no single holder able to reconstruct the key. (supports 4 of 32 shown, est. 4 of 32 residual, gain 0.5436 bits, evidence verified)
- [rejected] at `key_share_distribution_topology`: new value **across user and recovery parties** — Key shares or key fragments are held by a user together with recovery or escrow parties to enable key recovery. (supports 4 of 32 shown, est. 4 of 32 residual, gain 0.5436 bits, evidence verified)
- [rejected] at `key_share_distribution_topology`: new child_term_type **holder_trust_relationship** — Whether shareholders are mutually distrusting peers, a single trust point, or a designated recovery or escrow party. (supports 4 of 32 shown, est. 4 of 32 residual, gain 0.5436 bits, evidence verified); values: mutually distrusting peers, single trusted point, designated recovery party, user-controlled holders
- [rejected] at `finality_mechanism`: new value **mined-block-count measure voting** — Finality is decided by votes on finality proposals weighted by counts of blocks each node mined within the chain. (supports 4 of 37 shown, est. 4 of 37 residual, gain 0.4942 bits, evidence verified)
- [rejected] at `settlement_finality_timing`: new value **off-chain or custodial (no on-chain operation)** — Settlement finality is achieved off the blockchain ledger, for example within a custodial wallet or payment channel, bypassing on-chain confirmation. (supports 4 of 37 shown, est. 4 of 37 residual, gain 0.4942 bits, evidence verified)
- [rejected] at `settlement_finality_timing`: new value **confirmation-depth or consensus-dependent** — Finality is reached only after a number of block confirmations or a consensus threshold is met, rather than instantly. (supports 4 of 37 shown, est. 4 of 37 residual, gain 0.4942 bits, evidence verified)
- [rejected] at `settlement_finality_timing`: new value **dispute-window or hold-period deferred** — Finality is deferred until a dispute resolution period, hold, or authorization window elapses or is cleared. (supports 4 of 37 shown, est. 4 of 37 residual, gain 0.4942 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **energy / utilities** — Smart contracts deployed for peer-to-peer energy trading, microgrids, and electricity markets. (supports 4 of 40 shown, est. 12 of 116 residual, gain 0.4798 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **legal / contract management** — Smart contracts digitising legal agreements, procurement, and construction contract processes. (supports 4 of 40 shown, est. 12 of 116 residual, gain 0.4798 bits, evidence verified)
- [rejected] at `cross_chain_transfer_mechanism`: new value **cross-chain smart contract invocation** — Mechanism that lets a contract on one chain call or read state of a contract on another chain, without transferring the asset. (supports 3 of 29 shown, est. 3 of 29 residual, gain 0.4798 bits, evidence verified)
- [rejected] at `cross_chain_transfer_mechanism`: new value **stablecoin/asset-backed token minting** — Tokens minted on one chain are backed by reserves or staked collateral held on another chain. (supports 3 of 29 shown, est. 3 of 29 residual, gain 0.4798 bits, evidence verified)
- [rejected] at `central_bank_digital_currency`: new child_term_type **CBDC design architecture** — Splits CBDC proposals by whether end users hold claims on the central bank directly or only through intermediaries. (supports 4 of 39 shown, est. 4 of 39 residual, gain 0.4771 bits, evidence verified); values: retail CBDC, wholesale CBDC, not specified
- [rejected] at `deanonymisation_tracing_approach`: new value **risk-based transaction screening and wallet flagging** — Scores or flags wallets and transactions for criminal association using blacklists, labels, or risk rules to support compliance and quarantine decisions. (supports 4 of 39 shown, est. 4 of 39 residual, gain 0.4771 bits, evidence verified)
- [rejected] at `cross_chain_interoperability_mechanism`: new value **zero-knowledge proof verification of cross-chain transactions** — Cross-chain transfers or state are validated on the target chain using zk-SNARK or similar succinct proofs of source-chain data. (supports 4 of 40 shown, est. 11 of 108 residual, gain 0.4748 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **performance-metric-gated release** — New units are minted or released when a measured performance, workload, or achievement metric is met, rather than by consensus, collateral, or governance. (supports 4 of 40 shown, est. 6 of 59 residual, gain 0.4743 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **proof of energy generation minting** — New tokens are minted in proportion to verified physical energy production or capture, such as solar power or captured greenhouse gases. (supports 4 of 40 shown, est. 6 of 59 residual, gain 0.4743 bits, evidence verified)
- [rejected] at `minting_mechanism`: new value **physical-action-based minting** — New units are created in response to verified physical events, goods, or actions such as inventory production, ticket purchases, or receipts. (supports 4 of 40 shown, est. 6 of 59 residual, gain 0.4743 bits, evidence verified)
- [rejected] at `wallet_interface_delivery_form`: new value **tokenised physical object (gemstone, card, or item with embedded keys)** — Key material is carried by a physical item such as an etched gemstone, token, or object that also serves as an access or ownership proof for a digital asset. (supports 4 of 40 shown, est. 5 of 50 residual, gain 0.469 bits, evidence verified)
- [rejected] at `wallet_interface_delivery_form`: new value **payment card with secure element** — Key material is stored in an EMV or contactless payment card's secure element and accessed via NFC or point-of-sale terminals. (supports 4 of 40 shown, est. 5 of 50 residual, gain 0.469 bits, evidence verified)
- [rejected] at `wallet_interface_delivery_form`: new value **SIM or embedded secure element** — Key material resides in a SIM, embedded secure chip, or integrated circuit inside a device rather than a separate wallet product. (supports 4 of 40 shown, est. 5 of 50 residual, gain 0.469 bits, evidence verified)
- [rejected] at `zk_proof_system_variant`: new child_term_type **Trusted setup requirement** — Distinguishes proof systems by whether they need a trusted, possibly multi-party, setup to generate public parameters. (supports 4 of 40 shown, est. 6 of 60 residual, gain 0.469 bits, evidence unverified); values: trusted setup required, transparent (no trusted setup), universal/updatable setup, unspecified
- [rejected] at `interoperability_type`: new value **notary group cross-chain relay** — Cross-chain transfers are validated and forwarded by a committee or group of notary nodes rather than by direct chain-to-chain verification. (supports 4 of 40 shown, est. 30 of 304 residual, gain 0.4648 bits, evidence verified)
- [rejected] at `centralisation_locus`: new value **mining_pool_concentration** — Centralisation arises from concentration of hash power among a few mining pools rather than individual miners. (supports 4 of 40 shown, est. 30 of 304 residual, gain 0.4648 bits, evidence verified)
- [rejected] at `centralisation_locus`: new value **governance_token_voting_power** — Centralisation of decision-making power via concentrated governance token holdings and delegation in DAOs. (supports 4 of 40 shown, est. 30 of 304 residual, gain 0.4648 bits, evidence verified)
- [rejected] at `key_custody_control_model`: new value **hardware-secured key in a payment card or secure element** — The private key is held inside a tamper-resistant chip on a physical card or device that signs transactions on request. (supports 4 of 40 shown, est. 20 of 203 residual, gain 0.4643 bits, evidence verified)
- [rejected] at `script_verification_approach`: new value **machine-learning-based detection** — Vulnerabilities are detected by training neural or graph models on code or bytecode representations rather than by rule-based or search-based analysis. (supports 4 of 40 shown, est. 4 of 42 residual, gain 0.4537 bits, evidence verified)
- [rejected] at `ledger_partitioning_topology`: new value **application-specific app chain split from parent** — A chain created by splitting an existing blockchain to serve one high-volume application while the original chain continues. (supports 4 of 40 shown, est. 48 of 484 residual, gain 0.4341 bits, evidence verified)
- [rejected] at `ledger_partitioning_topology`: new value **parent-child generational chain** — A successor chain spawned from a parent chain that retains machine-readable links to it, reducing active ledger size. (supports 4 of 40 shown, est. 48 of 484 residual, gain 0.4341 bits, evidence verified)
- [rejected] at `ledger_partitioning_topology`: new value **forest of linked blockchains** — A collection of many individual blockchains aggregated into a virtualized structure sharing a consensus pool. (supports 4 of 40 shown, est. 48 of 484 residual, gain 0.4341 bits, evidence verified)
- [rejected] at `sharding_partition_basis`: new value **trust or reputation score** — Shards are formed by partitioning nodes according to computed trust, reputation, or consensus-agreement scores. (supports 3 of 36 shown, est. 3 of 36 residual, gain 0.4138 bits, evidence verified)
- [rejected] at `sharding_partition_basis`: new value **cryptographic key or hash-of-identifier mapping** — Shard assignment is determined by hashing a transaction, key, or identifier into a shard index. (supports 3 of 36 shown, est. 3 of 36 residual, gain 0.4138 bits, evidence verified)
- [rejected] at `sharding_partition_basis`: new value **transaction sensitivity or type class** — Transactions are routed to shards according to their sensitivity level, business type, or application category. (supports 3 of 36 shown, est. 3 of 36 residual, gain 0.4138 bits, evidence verified)
- [rejected] at `finality_mechanism`: new value **stake-weighted voting with epoch-based notarization** — Finality arises from notarized chains and vote aggregation over stake or epochs in proof-of-stake committees. (supports 3 of 37 shown, est. 3 of 37 residual, gain 0.406 bits, evidence verified)
- [rejected] at `finality_mechanism`: new value **cross-chain witness or atomic commit** — Finality for a transaction spanning shards or chains is established by atomic commit or a witness network rather than a single ledger. (supports 3 of 37 shown, est. 3 of 37 residual, gain 0.406 bits, evidence verified)
- [rejected] at `finality_mechanism`: new value **receipt or certificate attestation** — Finality is evidenced by signed receipts or certification authority attestations over a root hash of executed transactions. (supports 3 of 37 shown, est. 3 of 37 residual, gain 0.406 bits, evidence verified)
- [rejected] at `key_recovery_mechanism`: new value **puzzle or time-lock based recovery** — Key material is published or stored in a ledger as a cryptographic puzzle or time-locked artefact that the user solves to regain access. (supports 3 of 38 shown, est. 3 of 38 residual, gain 0.3985 bits, evidence verified)
- [rejected] at `key_recovery_mechanism`: new value **biometric or DNA-based key recovery** — Recovery material is derived from the user's biometric or DNA features rather than from a memorised or stored secret. (supports 3 of 38 shown, est. 3 of 38 residual, gain 0.3985 bits, evidence verified)
- [rejected] at `fiat_rail_integration`: new value **cryptocurrency-to-fiat conversion at settlement** — Crypto is converted to fiat by an exchange or intermediary, and the fiat is then pushed to the payee via a payment network. (supports 4 of 39 shown, est. 4 of 39 residual, gain 0.3959 bits, evidence verified)
- [rejected] at `fiat_rail_integration`: new child_term_type **fiat_settlement_timing** — Describes whether fiat settlement occurs in real time, deferred on a net basis, or via on-chain token representation. (supports 4 of 39 shown, est. 4 of 39 residual, gain 0.3959 bits, evidence verified); values: real-time push, deferred net settlement, on-chain token representation, no fiat settlement
- [rejected] at `smart_contract_deployment_context`: new value **lending / credit** — Smart contracts coordinating loan requests, collateralised lending, and micro-lending. (supports 3 of 40 shown, est. 9 of 116 residual, gain 0.3936 bits, evidence verified)
- [rejected] at `central_bank_digital_currency`: new value **central bank-backed stablecoin or fiat-backed token** — A digital token endorsed or backed by a central bank or sovereign authority that is not itself a CBDC liability. (supports 3 of 39 shown, est. 3 of 39 residual, gain 0.3912 bits, evidence verified)
- [rejected] at `deanonymisation_tracing_approach`: new value **off-chain intelligence and identity correlation** — Links blockchain addresses to real-world identities by correlating them with external data such as personal information, IP addresses, or service provider records. (supports 3 of 39 shown, est. 3 of 39 residual, gain 0.3912 bits, evidence verified)
- [rejected] at `interoperability_type`: new value **cross-chain query language** — Ledger exposes data from other blockchains through a query language or query interface spanning multiple chains. (supports 3 of 40 shown, est. 23 of 304 residual, gain 0.3867 bits, evidence verified)
- [rejected] at `ledger_purpose`: new value **supply chain traceability and product provenance** —  (supports 3 of 40 shown, est. 409 of 5447 residual, gain 0.3846 bits, evidence unverified)
- [rejected] at `identity_binding_mechanism`: new value **genetic or DNA-based binding** — Participant identity is bound to the ledger via a hashed genetic sequence or other biological trait. (supports 3 of 40 shown, est. 85 of 1139 residual, gain 0.383 bits, evidence verified)
- [rejected] at `asset_supply_policy`: new value **supply reduced by burning** — Total supply is reduced over time by permanently destroying (burning) already-issued tokens, in addition to any issuance rules. (supports 3 of 40 shown, est. 4 of 54 residual, gain 0.3809 bits, evidence verified)
- [rejected] at `asset_supply_policy`: new value **supply policy-adjusted (algorithmic)** — Total supply is expanded or contracted by protocol rules responding to market conditions such as exchange rate or price targets. (supports 3 of 40 shown, est. 4 of 54 residual, gain 0.3809 bits, evidence verified)
- [rejected] at `asset_supply_policy`: new value **supply issued against physical or electronic resources** — New units are minted in proportion to verified real-world or network resources provided, such as energy or compute. (supports 3 of 40 shown, est. 4 of 54 residual, gain 0.3809 bits, evidence verified)
- [rejected] at `asset_supply_policy`: new value **supply released by performance milestones** — A reserve of tokens is issued in tranches only when predefined performance metrics or milestones are met. (supports 3 of 40 shown, est. 4 of 54 residual, gain 0.3809 bits, evidence verified)
- [rejected] at `key_custody_control_model`: new value **offline-encrypted key with QR or non-network signing channel** — Key material is kept offline and transaction signing exchanges occur via QR codes or other non-networked channels rather than electronic transmission. (supports 3 of 40 shown, est. 15 of 203 residual, gain 0.3803 bits, evidence verified)
- [rejected] at `key_custody_control_model`: new value **key encrypted under biometric or user-credential factor** — The private key is encrypted or released only upon biometric or credential authentication of the user, rather than being held in plain form. (supports 3 of 40 shown, est. 15 of 203 residual, gain 0.3803 bits, evidence verified)
- [rejected] at `script_verification_approach`: new value **runtime monitoring** — Correctness is enforced or checked during execution by monitoring transactions against specified properties. (supports 3 of 40 shown, est. 3 of 42 residual, gain 0.3712 bits, evidence verified)
- [rejected] at `script_verification_approach`: new value **mutation testing** — Test suite quality is assessed by injecting artificial faults (mutants) and measuring whether tests detect them. (supports 3 of 40 shown, est. 3 of 42 residual, gain 0.3712 bits, evidence verified)
- [rejected] at `key_management_control_model`: new child_term_type **Signing authorization topology** — Distinguishes how multiple approvals are combined to authorize a signature on custodied assets. (supports 5 of 40 shown, est. 8 of 68 residual, gain 0.3553 bits, evidence unverified); values: m-of-n multi-signature script, threshold signature shares, policy-driven approver workflow, verification network threshold check
- [rejected] at `zk_proof_system_variant`: new value **Zero-knowledge Succinct Non-Interactive Argument of Knowledge (generic, unspecified variant)** — Generic zk-SNARK framework or circuit-based proof used without specifying a particular construction. (supports 3 of 40 shown, est. 4 of 60 residual, gain 0.3534 bits, evidence unverified)
- [rejected] at `consensus_finality`: new value **retrospective ledger rewrite** — Settlement is deterministic only until a chain reorganisation or double-spend window closes, after which history can be rewritten retrospectively. (supports 4 of 40 shown, est. 11 of 112 residual, gain 0.3483 bits, evidence verified)
- [rejected] at `native_vs_token_standard`: new value **NFT application-layer token (ERC-721 as design choice)** — Crypto-asset realised as a non-fungible token instance used to represent records, identity, or access rights within an application, not as a native protocol asset. (supports 4 of 40 shown, est. 46 of 457 residual, gain 0.3472 bits, evidence verified)
- [rejected] at `privacy_mechanism_family`: new value **trusted execution environment** — Confidentiality provided by hardware-isolated enclaves that process data inside protected memory regions. (supports 3 of 40 shown, est. 38 of 507 residual, gain 0.3435 bits, evidence verified)
- [rejected] at `privacy_mechanism_family`: new value **chameleon signature** — Signature scheme with a trapdoor allowing redaction or modification of signed content while preserving verifiability, used for privacy-preserving edits. (supports 3 of 40 shown, est. 38 of 507 residual, gain 0.3435 bits, evidence verified)
- [rejected] at `key_isolation_from_network`: new value **intermittent/opportunistic connectivity** — Key-holding environment connects to a network only intermittently or opportunistically, e.g. when connectivity is available, rather than always-online or always-offline. (supports 3 of 35 shown, est. 3 of 35 residual, gain 0.3435 bits, evidence unverified)
- [rejected] at `backing_of_token`: new value **backed by a fractionalised or tokenised real-world asset title** — Token value rests on fractional ownership or a digital title to a specific physical or real-world asset. (supports 4 of 24 shown, est. 4 of 24 residual, gain 0.3391 bits, evidence verified)
- [rejected] at `key_management_control_model`: new value **policy-gated custodial vault with rule-based access** — Private keys held in logically separated vaults, each governed by a policy map defining access and approval rules before any signing action. (supports 4 of 40 shown, est. 7 of 68 residual, gain 0.3252 bits, evidence verified)
- [rejected] at `identity_binding_mechanism`: new value **physical unclonable function (PUF) binding** — Identity is bound to a device or chip through a physically unclonable hardware fingerprint. (supports 2 of 40 shown, est. 57 of 1139 residual, gain 0.2866 bits, evidence verified)
- [rejected] at `centralisation_locus`: new value **geographic_location_concentration** — Centralisation locus is the geographic distribution of validators or nodes in physical space. (supports 2 of 40 shown, est. 15 of 304 residual, gain 0.2836 bits, evidence verified)
- [rejected] at `backing_of_token`: new value **backed by revenue, data or other economic streams** — Token value is tied to a non-commodity income stream or data asset rather than to physical or financial reserves. (supports 3 of 24 shown, est. 3 of 24 residual, gain 0.2836 bits, evidence verified)
- [rejected] at `backing_of_token`: new value **backed by an intermediary or cross-chain collateral pool** — Token value is secured by collateral held by intermediaries or locked assets on another chain. (supports 3 of 24 shown, est. 3 of 24 residual, gain 0.2836 bits, evidence verified)
- [rejected] at `key_splitting_scheme`: new value **distributed key generation (DKG)** — Signing key shares are jointly generated by the parties so that no single party ever holds the complete key. (supports 4 of 40 shown, est. 7 of 68 residual, gain 0.278 bits, evidence verified)
- [rejected] at `key_splitting_scheme`: new value **physical key-part storage (cards/seed splitting)** — Key material is split into physical segments or seed parts stored on separate media or devices such as cards or hardware wallets. (supports 4 of 40 shown, est. 7 of 68 residual, gain 0.278 bits, evidence verified)
- [rejected] at `unhosted_vs_hosted_wallet`: new value **hybrid multi-party / platform-controlled wallet** — Keys or signing authority are split or delegated between a platform operator and the user, so neither alone controls the asset. (supports 4 of 40 shown, est. 19 of 192 residual, gain 0.2768 bits, evidence unverified)
- [rejected] at `unhosted_vs_hosted_wallet`: new child_term_type **wallet_settlement_layer** — Distinguishes on-chain blockchain settlement from internal or off-chain ledgers used by wallet operators. (supports 4 of 40 shown, est. 19 of 192 residual, gain 0.2768 bits, evidence verified); values: on-chain settlement, off-chain internal ledger, side-chain settlement
- [rejected] at `centralisation_level`: new child_term_type **control_mechanism_type** — Distinguishes how central or distributed control is actually exercised, such as voting, keys, or a trusted authority. (supports 4 of 40 shown, est. 88 of 881 residual, gain 0.2765 bits, evidence verified); values: token-weighted voting, private key holder, trusted central authority, smart contract rules, multi-party consensus
- [rejected] at `risk_type_illicit_finance`: new value **abnormal/fraudulent transaction detection via ML on wallet features** — Machine-learning or graph-based detection of anomalous or fraudulent transactions using wallet and transaction features. (supports 4 of 31 shown, est. 4 of 31 residual, gain 0.2 bits, evidence verified)
- [rejected] at `sharding_partition_basis`: new value **time or spatial data dimension** — Data is partitioned across shards by time intervals or geographic/spatial dimensions of the records. (supports 1 of 36 shown, est. 1 of 36 residual, gain 0.1831 bits, evidence verified)
- [rejected] at `script_language_expressiveness`: new child_term_type **script_execution_model** — Whether scripts run directly on the ledger's nodes, are executed off-chain with proofs posted on-chain, or are executed in parallel across execution nodes. (supports 4 of 40 shown, est. 29 of 294 residual, gain 0.1798 bits, evidence verified); values: on-chain interpreted, off-chain execution with on-chain verification, parallel or asynchronous execution
- [rejected] at `smart_contract_deployment_context`: new value **gaming / lotteries** — Smart contracts running games of chance, lotteries, and gambling draws. (supports 1 of 40 shown, est. 3 of 116 residual, gain 0.1732 bits, evidence verified)
- [rejected] at `smart_contract_deployment_context`: new value **credentials / education** — Smart contracts for issuing and verifying learning records and e-portfolios. (supports 1 of 40 shown, est. 3 of 116 residual, gain 0.1732 bits, evidence verified)
- [rejected] at `risk_type_illicit_finance`: new value **transaction destination risk scoring** — Risk assessment of crypto-asset transfers by scoring destination addresses and transaction patterns to flag illicit flows. (supports 3 of 31 shown, est. 3 of 31 residual, gain 0.1653 bits, evidence unverified)
- [rejected] at `payment_settlement_mechanism`: new value **bidirectional payment channel** — Settlement via off-chain bidirectional channels that are opened and closed on-chain, typically with channel balances updated by signed state. (supports 3 of 37 shown, est. 3 of 37 residual, gain 0.1241 bits, evidence verified)
- [rejected] at `payment_settlement_mechanism`: new child_term_type **Payment-channel network routing** — Splits payments that traverse intermediary nodes over a channel network from direct two-party or single-hop settlement. (supports 3 of 37 shown, est. 3 of 37 residual, gain 0.1241 bits, evidence verified); values: direct single-hop, multi-hop routed, not applicable
- [rejected] at `payment_settlement_mechanism`: new value **offline or cold-signed payment** — Payment authorised and prepared without network connectivity, with broadcast to the ledger occurring later. (supports 3 of 37 shown, est. 3 of 37 residual, gain 0.1241 bits, evidence verified)
- [rejected] at `payment_settlement_mechanism`: new value **cheque or deferred-claim instrument** — Payment settled by a drawer-signed instrument that the payee later redeems against a locked output. (supports 3 of 37 shown, est. 3 of 37 residual, gain 0.1241 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **mining pool participant / hashpower contributor** — Actor who contributes computational hashpower to a mining pool or distributed computation in exchange for shared rewards, distinct from solo validators. (supports 4 of 40 shown, est. 12 of 124 residual, gain 0.1096 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **oracle operator / data provider** — Actor who supplies off-chain data to blockchain smart contracts through oracle nodes or networks. (supports 4 of 40 shown, est. 12 of 124 residual, gain 0.1096 bits, evidence verified)
- [rejected] at `centralisation_level`: new value **redactable by key holder** — Blockchain where a single private key holder can alter blocks while others cannot, a controlled-mutability model. (supports 1 of 40 shown, est. 22 of 881 residual, gain 0.0994 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **ICO / token sale founder or investor** — Actor who launches a token offering or invests in one, as fundraiser or subscriber, distinct from issuers of stablecoins. (supports 3 of 40 shown, est. 9 of 124 residual, gain 0.0897 bits, evidence verified)
- [rejected] at `ecosystem_participant_role`: new value **ecosystem community / blockchain scene participant** — Actor participating in informal blockchain communities, events, or social networks rather than technical or financial roles. (supports 3 of 40 shown, est. 9 of 124 residual, gain 0.0897 bits, evidence verified)
- [rejected] at `risk_type_illicit_finance`: new value **illegal withdrawal / double payment** — Blocking unauthorised or duplicate withdrawals and payments from exchange or virtual-asset accounts. (supports 1 of 31 shown, est. 1 of 31 residual, gain 0.0741 bits, evidence verified)