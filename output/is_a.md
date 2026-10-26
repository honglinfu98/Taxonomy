# Task B output: is-a DAG of term types

Each child's distribution over candidate parents + `none` sums to 1. Edges kept: P(X is-a Y) >= 0.4, above the child's own P(none), acyclic, taken greedily by probability (a mutual pair resolves to the stronger direction). The first kept parent is the tree position; further parents appear as *also under*. Roots have no kept parent. Full distributions: `output/is_a.json`; DAG as nodes/edges/metrics: `output/taxonomy_dag.json`, `output/is_a.dot`; metrics across thresholds: `output/dag_metrics.json`.

**Overall.** 93 nodes, 55 is-a edges, 38 roots, 65 leaves, max depth 2; information gain 17.52 bits total, 0.43 bits per descent; AUC 0.817, expected depth 0.64; effective leaves 51.4, 43 leaves hold 90% of descents.

Exact ties resolved by id order (review): `ledger_storage_model` is-a `dlt_architecture` (0.42, reverse equal); `offer_and_issuance_method` is-a `decentralised_or_centralised_offer_model` (0.55, reverse equal)

## asset

21 nodes, 10 is-a edges, 11 roots, 16 leaves, max depth 1; information gain 3.54 bits total, 0.32 bits per descent; AUC 0.773, expected depth 0.45; effective leaves 13.8, 12 leaves hold 90% of descents.

- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`  (root, P(none)=0.30)
- Source of yield `yield_source`  (root, P(none)=0.25)
  - Yield distribution mechanism `yield_distribution_mechanism`  (p=0.45)
- Native asset versus token standard `native_vs_token_standard`  (root, P(none)=0.21)
  - Wrapped / cross-chain representation `wrapped_or_bridged_asset`  (p=0.45)
- Economic function of the asset `crypto_asset_function`  (root, P(none)=0.20)
- Issuer identifiability `issuer_presence`  (root, P(none)=0.15)
  - Centralisation of control `centralisation_level`  (p=0.42)
- Legal classification of crypto-asset `legal_classification_status`  (root, P(none)=0.13)
- Form of holder claim `claim_form`  (root, P(none)=0.10)
- Reference asset type `asset_reference_type`  (root, P(none)=0.05); IG 1.56 bits
  - Reference currency for stablecoin peg (currency vs other) `native_vs_stable_price_reference_asset_currency`  (p=0.62)
  - Payment stablecoin / e-money / ART regulatory class `stablecoin_regulatory_class`  (p=0.45)
  - Redemption mechanism `redemption_mechanism`  (p=0.42)
- Crypto-asset definitional criteria `crypto_asset_scope_criteria`  (root, P(none)=0.05); IG 1.98 bits
  - Recording and cryptographic linkage `digital_asset_recording`  (p=0.81)
  - Central bank digital currency status `central_bank_digital_currency`  (p=0.56)
  - Fungibility `fungibility`  (p=0.55)
  - Convertible virtual currency (CVC) status `convertible_virtual_currency_status`  (p=0.55)
- Tokenisation form `tokenisation_form`  (root, P(none)=0.05)
- Ancillary asset and network token status `ancillary_asset_status`  (root, P(none)=0.05)

## technology

24 nodes, 13 is-a edges, 11 roots, 14 leaves, max depth 2; information gain 2.53 bits total, 0.23 bits per descent; AUC 0.763, expected depth 0.79; effective leaves 12.9, 11 leaves hold 90% of descents.

- Software architecture (monolithic vs polylithic) `software_architecture`  (root, P(none)=0.82)
- Smart contract / distributed ledger application scope `smart_contract_definition_scope`  (root, P(none)=0.78)
  - Smart contract / script language expressiveness `script_language_expressiveness`  (p=0.42)
    - Interoperability and intraoperability `interoperability_type`  (p=0.46)
- Wallet storage mode (hot or cold) `wallet_type_storage`  (root, P(none)=0.73)
- Information and communications technology system `ict_system_scope`  (root, P(none)=0.55)
  - Data classification (traffic, content, subscriber) `traffic_and_subscriber_data_class`  (p=0.56)
- Ledger access and permissioning `ledger_access_permission`  (root, P(none)=0.50); IG 1.53 bits
  - Ledger scope: open or closed access by design `dlt_network_access_scope`  (p=0.80)
  - Identity layer and onboarding `digital_identity_layer`  (p=0.55)
  - Governance model of a DLT system `governance_model`  (p=0.42)
    - Decentralised system certification `decentralised_system_status`  (p=0.42)
- Consensus mechanism `consensus_mechanism`  (root, P(none)=0.50); IG 1.00 bits
  - Finality of agreement `consensus_finality`  (p=0.62)
  - Validator reward mechanism `reward_mechanism`  (p=0.55)
    - Transaction fee regime `fee_structure`  (p=0.55)
- Native asset presence and type `native_asset_type`  (root, P(none)=0.40)
  - Asset supply management (monetary policy) `asset_supply_policy`  (p=0.60)
- Privacy and anonymity features `privacy_enhancement`  (root, P(none)=0.30)
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`  (root, P(none)=0.20)
  - Ledger storage model (what is stored on chain) `ledger_storage_model`  (p=0.42)
- Network topology and node roles `network_topology`  (root, P(none)=0.12)
  - Node / DLT network node role `ledger_node_role`  (p=0.50)
- Source code openness `code_license_openness`  (root, P(none)=0.08)

## actor

19 nodes, 13 is-a edges, 6 roots, 14 leaves, max depth 2; information gain 3.98 bits total, 0.66 bits per descent; AUC 0.782, expected depth 0.69; effective leaves 9.5, 9 leaves hold 90% of descents.

- Consumer or retail versus professional user `consumer_vs_professional_status`  (root, P(none)=0.88)
- Operator of crypto-asset arrangement `crypto_asset_operator`  (root, P(none)=0.58)
- Pooled investment vehicle structure `fund_or_pooled_vehicle`  (root, P(none)=0.32)
- Crypto-asset service provider or VASP status `service_provider_status`  (root, P(none)=0.23); IG 2.98 bits
  - Infrastructure provider type `infrastructure_provider_type`  (p=0.62)
  - Offshore VASP status (activity-based or location-based) `offshore_vasp_status`  (p=0.62)
  - Trading venue type `exchange_venue_type`  (p=0.55)
  - Control or sufficient influence over DeFi arrangement `decentralised_control_status_actor`  (p=0.55)
  - Jurisdictional regime and home or host state `regulatory_regime_scope_jurisdictional`  (p=0.51)
  - Principal or agent role in transaction `actor_role_in_service`  (p=0.50)
    - Originator and beneficiary role `party_role_transfer`  (p=0.42)
  - Financial institution status for AML `regulatory_perimeter_fi_status`  (p=0.42)
  - Stablecoin issuer model `stablecoin_issuer_model`  (p=0.40)
- Ecosystem participant role `ecosystem_participant_role`  (root, P(none)=0.15); IG 0.99 bits
  - Related person and affiliated person status `related_person_affiliation`  (p=0.52)
  - Validator operation capacity (who may run a node) `consensus_participant_validator_capacity`  (p=0.42)
- Custody model `custodian_or_custody_model`  (root, P(none)=0.12)
  - Permitted control over client assets (unilateral vs multi-party control) `unhosted_custody_control_policy`  (p=0.62)
    - Address linkage to service provider `self_hosted_address_status`  (p=0.43)

## activity

10 nodes, 7 is-a edges, 3 roots, 7 leaves, max depth 2; information gain 3.16 bits total, 0.72 bits per descent; AUC 0.772, expected depth 0.79; effective leaves 4.9, 5 leaves hold 90% of descents.

- Minting mechanism `minting_mechanism`  (root, P(none)=0.24)
- Crypto-asset service type `crypto_asset_service_type`  (root, P(none)=0.10); IG 1.58 bits
  - Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`  (p=0.55); IG 1.58 bits
    - Peer-to-peer (P2P) transaction `transaction_type_p2p`  (p=0.55)
    - Payment service and funds transfer `payment_or_transfer_service`  (p=0.50)
    - Money transmission (acceptance and transmission of value) `regulated_transmission_of_value`  (p=0.42)
  - Staking arrangement (self, delegated, custodial, liquid) `staking_arrangement`  (p=0.50)
  - Nexus to jurisdiction (services offered in jurisdiction) `service_location_nexus`  (p=0.45)
- Public offer or private placement `decentralised_or_centralised_offer_model`  (root, P(none)=0.05)
  - Offer and issuance method (token distribution) `offer_and_issuance_method`  (p=0.55)

## obligation_or_risk

19 nodes, 12 is-a edges, 7 roots, 14 leaves, max depth 2; information gain 4.32 bits total, 0.62 bits per descent; AUC 0.843, expected depth 0.60; effective leaves 10.7, 11 leaves hold 90% of descents.

- Redemption and reserve adequacy `redemption_risk_criteria`  (root, P(none)=1.00); IG 2.00 bits
  - Settlement finality and legal enforceability `settlement_finality_legal_test`  (p=0.52)
  - Yield or interest on stablecoin `stablecoin_interest_restriction`  (p=0.50)
  - Traditional finance analogue `tradfi_analogue`  (p=0.50)
  - Prudential classification group (Basel) `prudential_classification_group`  (p=0.42)
- Tax reporting obligation status (CARF) `tax_reporting_status`  (root, P(none)=0.30)
- ICT and operational resilience risk `operational_resilience_risk`  (root, P(none)=0.22)
- Safeguarding and custody obligation `custody_safeguarding_obligation`  (root, P(none)=0.16)
- Excluded instrument category (EU scope exclusions) `excluded_instrument_category`  (root, P(none)=0.15)
  - MiFID financial instrument status `financial_instrument_status`  (p=0.62)
- Security status of digital asset (US exclusions) `securities_status_digital_asset`  (root, P(none)=0.13)
  - Investment contract (Howey) criteria `investment_contract_howey`  (p=0.55)
- Anti-money laundering obligations `aml_obligations_applicability`  (root, P(none)=0.12); IG 2.32 bits
  - Anonymity-enhancing crypto-asset status `anonymity_enhancing_status`  (p=0.62)
  - Virtual assets as property or proceeds of crime `virtual_asset_property_status`  (p=0.62)
    - Serious crime threshold for predicate offences `serious_crime_threshold`  (p=0.42)
  - Illicit finance risk category `risk_type_illicit_finance`  (p=0.62)
  - Exemption from MSB status `regulated_status_cvc_mst_exemption`  (p=0.62)
  - Freezing and blocking capability `sanctions_and_freezing_capability`  (p=0.55)
