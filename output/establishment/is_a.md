# Task B output: is-a DAG of term types

Each child's weights over its candidate parents sum to 1 (the model's `none` entry is removed and recorded as P(none)). Every weighted edge is kept unless it would close a cycle; edges are taken greedily by weight, so a mutual pair resolves to the stronger direction. The first kept parent is the tree position; further parents appear as *also under*. Roots have no kept parent. Full distributions: `output/is_a.json`; DAG as nodes/edges/metrics: `output/taxonomy_dag.json`, `output/is_a.dot`; metrics when hiding edges below a weight: `output/dag_metrics.json`.

**Overall.** 93 nodes, 279 is-a edges, 5 roots, 18 leaves, max depth 14; information gain 90.50 bits total, 4.72 bits per descent; AUC 0.835, expected depth 2.81; effective leaves 14.0, 12 leaves hold 90% of descents.
Edges dropped to keep the graph acyclic: 119.

Exact ties resolved by id order (review): `offer_and_issuance_method` is-a `decentralised_or_centralised_offer_model` (0.58, reverse equal)

## asset

21 nodes, 68 is-a edges, 1 roots, 5 leaves, max depth 9; information gain 22.40 bits total, 4.17 bits per descent; AUC 0.773, expected depth 2.54; effective leaves 3.2, 3 leaves hold 90% of descents.

- Crypto-asset definitional criteria `crypto_asset_scope_criteria`  (root); IG 2.94 bits
  - Recording and cryptographic linkage `digital_asset_recording`  (w=0.87); also under `convertible_virtual_currency_status` (p=0.02), `crypto_asset_function` (p=0.01); IG 2.04 bits
  - Central bank digital currency status `central_bank_digital_currency`  (w=0.75); also under `digital_asset_recording` (p=0.11), `legal_classification_status` (p=0.08), `issuer_presence` (p=0.05)
  - Fungibility `fungibility`  (w=0.73); also under `crypto_asset_function` (p=0.16), `legal_classification_status` (p=0.07), `digital_asset_recording` (p=0.04)
  - Convertible virtual currency (CVC) status `convertible_virtual_currency_status`  (w=0.69); also under `legal_classification_status` (p=0.12), `crypto_asset_function` (p=0.10), `stablecoin_regulatory_class` (p=0.05), `asset_reference_type` (p=0.04)
  - Native asset versus token standard `native_vs_token_standard`  (w=0.38); also under `digital_asset_recording` (p=0.32), `tokenisation_form` (p=0.10), `fungibility` (p=0.08)
    - Wrapped / cross-chain representation `wrapped_or_bridged_asset`  (w=0.50); also under `tokenisation_form` (p=0.28), `redemption_mechanism` (p=0.13), `claim_form` (p=0.09)
  - Economic function of the asset `crypto_asset_function`  (w=0.25); IG 2.81 bits
    - Legal classification of crypto-asset `legal_classification_status`  (w=0.39); IG 3.20 bits
      - Issuer identifiability `issuer_presence`  (w=0.35); also under `crypto_asset_scope_criteria` (p=0.12), `crypto_asset_function` (p=0.06); IG 2.15 bits
        - Centralisation of control `centralisation_level`  (w=0.57); also under `redemption_mechanism` (p=0.27), `yield_distribution_mechanism` (p=0.16); IG 0.72 bits
          - Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`  (w=0.43); also under `claim_form` (p=0.29), `issuer_presence` (p=0.14), `digital_asset_recording` (p=0.14)
      - Reference asset type `asset_reference_type`  (w=0.32); also under `crypto_asset_function` (p=0.11); IG 2.48 bits
        - Reference currency for stablecoin peg (currency vs other) `native_vs_stable_price_reference_asset_currency`  (w=0.67); also under `stablecoin_regulatory_class` (p=0.22), `crypto_asset_scope_criteria` (p=0.07), `legal_classification_status` (p=0.04)
        - Payment stablecoin / e-money / ART regulatory class `stablecoin_regulatory_class`  (w=0.46); also under `legal_classification_status` (p=0.15), `issuer_presence` (p=0.05); IG 1.38 bits
        - Redemption mechanism `redemption_mechanism`  (w=0.44); also under `stablecoin_regulatory_class` (p=0.21), `legal_classification_status` (p=0.06); IG 1.95 bits
        - Tokenisation form `tokenisation_form`  (w=0.34); also under `claim_form` (p=0.19), `crypto_asset_scope_criteria` (p=0.16), `digital_asset_recording` (p=0.11); IG 0.84 bits
      - Form of holder claim `claim_form`  (w=0.24); also under `redemption_mechanism` (p=0.22), `issuer_presence` (p=0.22), `asset_reference_type` (p=0.17), `crypto_asset_function` (p=0.14); IG 1.90 bits
    - Ancillary asset and network token status `ancillary_asset_status`  (w=0.32); also under `issuer_presence` (p=0.26), `legal_classification_status` (p=0.16), `crypto_asset_scope_criteria` (p=0.16), `centralisation_level` (p=0.11)
    - Source of yield `yield_source`  (w=0.24); also under `legal_classification_status` (p=0.20), `asset_reference_type` (p=0.13)
      - Yield distribution mechanism `yield_distribution_mechanism`  (w=0.50); also under `claim_form` (p=0.22), `redemption_mechanism` (p=0.17)

## technology

24 nodes, 75 is-a edges, 1 roots, 4 leaves, max depth 14; information gain 23.13 bits total, 5.47 bits per descent; AUC 0.754, expected depth 3.94; effective leaves 2.6, 2 leaves hold 90% of descents.

- Governance model of a DLT system `governance_model`  (root); IG 2.41 bits
  - Ledger access and permissioning `ledger_access_permission`  (w=1.00); IG 3.33 bits
    - Ledger scope: open or closed access by design `dlt_network_access_scope`  (w=0.82); also under `governance_model` (p=0.06); IG 1.95 bits
      - Network topology and node roles `network_topology`  (w=0.43); also under `ledger_access_permission` (p=0.34); IG 2.36 bits
        - Consensus mechanism `consensus_mechanism`  (w=1.00); IG 2.18 bits
          - Finality of agreement `consensus_finality`  (w=0.78); also under `network_topology` (p=0.10), `ledger_access_permission` (p=0.06), `reward_mechanism` (p=0.04), `dlt_architecture` (p=0.03)
          - Validator reward mechanism `reward_mechanism`  (w=0.69); IG 1.47 bits
            - Transaction fee regime `fee_structure`  (w=0.81); also under `consensus_mechanism` (p=0.04); IG 0.94 bits
            - Native asset presence and type `native_asset_type`  (w=0.25); also under `ledger_access_permission` (p=0.17), `fee_structure` (p=0.17), `governance_model` (p=0.08); IG 1.14 bits
              - Asset supply management (monetary policy) `asset_supply_policy`  (w=0.68); also under `reward_mechanism` (p=0.23), `fee_structure` (p=0.09)
        - Node / DLT network node role `ledger_node_role`  (w=0.56); also under `consensus_mechanism` (p=0.22), `dlt_network_access_scope` (p=0.09), `ledger_access_permission` (p=0.08), `ledger_storage_model` (p=0.06)
          - Information and communications technology system `ict_system_scope`  (w=0.22); also under `network_topology` (p=0.18), `dlt_network_access_scope` (p=0.09), `ledger_access_permission` (p=0.07); IG 0.77 bits
            - Data classification (traffic, content, subscriber) `traffic_and_subscriber_data_class`  (w=0.95); also under `ledger_storage_model` (p=0.05)
        - Software architecture (monolithic vs polylithic) `software_architecture`  (w=0.44); also under `governance_model` (p=0.28), `consensus_mechanism` (p=0.22), `native_asset_type` (p=0.06); IG 2.30 bits
          - Ledger storage model (what is stored on chain) `ledger_storage_model`  (w=0.14); also under `ledger_access_permission` (p=0.12), `native_asset_type` (p=0.09); IG 0.83 bits
            - DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`  (w=0.53); also under `consensus_mechanism` (p=0.23), `software_architecture` (p=0.15), `ledger_access_permission` (p=0.10); IG 1.04 bits
    - Identity layer and onboarding `digital_identity_layer`  (w=0.60); also under `dlt_network_access_scope` (p=0.22), `governance_model` (p=0.11), `ict_system_scope` (p=0.04); IG 0.93 bits
    - Wallet storage mode (hot or cold) `wallet_type_storage`  (w=0.46); also under `privacy_enhancement` (p=0.19), `digital_identity_layer` (p=0.15), `dlt_architecture` (p=0.12), `code_license_openness` (p=0.08)
    - Privacy and anonymity features `privacy_enhancement`  (w=0.43); also under `digital_identity_layer` (p=0.29), `traffic_and_subscriber_data_class` (p=0.14), `ict_system_scope` (p=0.14)
  - Decentralised system certification `decentralised_system_status`  (w=0.50); also under `ledger_access_permission` (p=0.36), `network_topology` (p=0.14); IG 0.88 bits
  - Source code openness `code_license_openness`  (w=0.24); also under `software_architecture` (p=0.15), `ledger_access_permission` (p=0.11), `decentralised_system_status` (p=0.11); IG 0.60 bits
    - Smart contract / distributed ledger application scope `smart_contract_definition_scope`  (w=0.45); also under `dlt_architecture` (p=0.36), `software_architecture` (p=0.18)
      - Smart contract / script language expressiveness `script_language_expressiveness`  (w=0.49); also under `software_architecture` (p=0.23), `native_asset_type` (p=0.06), `decentralised_system_status` (p=0.05)
        - Interoperability and intraoperability `interoperability_type`  (w=0.59); also under `network_topology` (p=0.14), `governance_model` (p=0.11), `ledger_access_permission` (p=0.08), `dlt_network_access_scope` (p=0.07)

## actor

19 nodes, 58 is-a edges, 1 roots, 3 leaves, max depth 12; information gain 18.87 bits total, 6.02 bits per descent; AUC 0.767, expected depth 3.30; effective leaves 2.6, 3 leaves hold 90% of descents.

- Crypto-asset service provider or VASP status `service_provider_status`  (root); IG 3.84 bits
  - Infrastructure provider type `infrastructure_provider_type`  (w=0.70); also under `custodian_or_custody_model` (p=0.07); IG 0.97 bits
  - Offshore VASP status (activity-based or location-based) `offshore_vasp_status`  (w=0.69); IG 0.69 bits
  - Jurisdictional regime and home or host state `regulatory_regime_scope_jurisdictional`  (w=0.60); also under `offshore_vasp_status` (p=0.30); IG 2.10 bits
  - Principal or agent role in transaction `actor_role_in_service`  (w=0.59); also under `regulatory_perimeter_fi_status` (p=0.12); IG 2.69 bits
    - Originator and beneficiary role `party_role_transfer`  (w=0.47); also under `service_provider_status` (p=0.33), `self_hosted_address_status` (p=0.13), `regulatory_regime_scope_jurisdictional` (p=0.07)
      - Consumer or retail versus professional user `consumer_vs_professional_status`  (w=0.33); also under `service_provider_status` (p=0.25), `actor_role_in_service` (p=0.25), `regulatory_perimeter_fi_status` (p=0.17)
    - Pooled investment vehicle structure `fund_or_pooled_vehicle`  (w=0.38); also under `service_provider_status` (p=0.31), `regulatory_perimeter_fi_status` (p=0.31)
  - Control or sufficient influence over DeFi arrangement `decentralised_control_status_actor`  (w=0.58); also under `actor_role_in_service` (p=0.16), `custodian_or_custody_model` (p=0.11), `exchange_venue_type` (p=0.08); IG 1.36 bits
  - Trading venue type `exchange_venue_type`  (w=0.56); also under `actor_role_in_service` (p=0.26), `custodian_or_custody_model` (p=0.08), `regulatory_regime_scope_jurisdictional` (p=0.04)
  - Financial institution status for AML `regulatory_perimeter_fi_status`  (w=0.48); also under `regulatory_regime_scope_jurisdictional` (p=0.23), `offshore_vasp_status` (p=0.07); IG 1.47 bits
  - Stablecoin issuer model `stablecoin_issuer_model`  (w=0.44); also under `ecosystem_participant_role` (p=0.28), `regulatory_regime_scope_jurisdictional` (p=0.11)
  - Custody model `custodian_or_custody_model`  (w=0.25); also under `actor_role_in_service` (p=0.07); IG 2.12 bits
    - Permitted control over client assets (unilateral vs multi-party control) `unhosted_custody_control_policy`  (w=0.70); also under `service_provider_status` (p=0.23), `decentralised_control_status_actor` (p=0.05); IG 0.77 bits
      - Address linkage to service provider `self_hosted_address_status`  (w=0.47); also under `custodian_or_custody_model` (p=0.33), `service_provider_status` (p=0.17)
    - Operator of crypto-asset arrangement `crypto_asset_operator`  (w=0.29); also under `stablecoin_issuer_model` (p=0.24), `ecosystem_participant_role` (p=0.24), `service_provider_status` (p=0.12), `regulatory_regime_scope_jurisdictional` (p=0.12); IG 0.95 bits
  - Ecosystem participant role `ecosystem_participant_role`  (w=0.24); also under `infrastructure_provider_type` (p=0.24), `decentralised_control_status_actor` (p=0.18), `actor_role_in_service` (p=0.14); IG 1.91 bits
    - Related person and affiliated person status `related_person_affiliation`  (w=0.58); also under `decentralised_control_status_actor` (p=0.22), `crypto_asset_operator` (p=0.13), `actor_role_in_service` (p=0.03), `consumer_vs_professional_status` (p=0.02)
    - Validator operation capacity (who may run a node) `consensus_participant_validator_capacity`  (w=0.48); also under `crypto_asset_operator` (p=0.23), `infrastructure_provider_type` (p=0.16), `unhosted_custody_control_policy` (p=0.14)

## activity

10 nodes, 31 is-a edges, 1 roots, 2 leaves, max depth 7; information gain 9.23 bits total, 3.88 bits per descent; AUC 0.741, expected depth 2.32; effective leaves 2.0, 2 leaves hold 90% of descents.

- Crypto-asset service type `crypto_asset_service_type`  (root); IG 2.86 bits
  - Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`  (w=0.57); IG 2.19 bits
    - Peer-to-peer (P2P) transaction `transaction_type_p2p`  (w=0.73); also under `regulated_transmission_of_value` (p=0.13), `crypto_asset_service_type` (p=0.08), `offer_and_issuance_method` (p=0.01)
    - Payment service and funds transfer `payment_or_transfer_service`  (w=0.56); also under `crypto_asset_service_type` (p=0.22), `regulated_transmission_of_value` (p=0.17), `transaction_type_p2p` (p=0.06)
    - Money transmission (acceptance and transmission of value) `regulated_transmission_of_value`  (w=0.44); also under `crypto_asset_service_type` (p=0.26); IG 2.25 bits
  - Staking arrangement (self, delegated, custodial, liquid) `staking_arrangement`  (w=0.57); also under `offer_and_issuance_method` (p=0.11), `regulated_transmission_of_value` (p=0.06), `transfer_of_crypto_assets` (p=0.03)
    - Minting mechanism `minting_mechanism`  (w=0.38); also under `offer_and_issuance_method` (p=0.38), `crypto_asset_service_type` (p=0.12), `transfer_of_crypto_assets` (p=0.06), `decentralised_or_centralised_offer_model` (p=0.06)
  - Nexus to jurisdiction (services offered in jurisdiction) `service_location_nexus`  (w=0.56); also under `regulated_transmission_of_value` (p=0.13), `payment_or_transfer_service` (p=0.13), `decentralised_or_centralised_offer_model` (p=0.11), `transfer_of_crypto_assets` (p=0.07)
  - Public offer or private placement `decentralised_or_centralised_offer_model`  (w=0.21); also under `regulated_transmission_of_value` (p=0.11), `transfer_of_crypto_assets` (p=0.04); IG 1.00 bits
    - Offer and issuance method (token distribution) `offer_and_issuance_method`  (w=0.58); also under `crypto_asset_service_type` (p=0.11), `transfer_of_crypto_assets` (p=0.04); IG 0.94 bits

## obligation_or_risk

19 nodes, 47 is-a edges, 1 roots, 4 leaves, max depth 12; information gain 16.86 bits total, 4.05 bits per descent; AUC 0.881, expected depth 1.93; effective leaves 4.0, 4 leaves hold 90% of descents.

- Anti-money laundering obligations `aml_obligations_applicability`  (root); IG 2.94 bits
  - Exemption from MSB status `regulated_status_cvc_mst_exemption`  (w=0.78); also under `investment_contract_howey` (p=0.12); IG 0.75 bits
    - Tax reporting obligation status (CARF) `tax_reporting_status`  (w=0.52); also under `aml_obligations_applicability` (p=0.48)
  - Anonymity-enhancing crypto-asset status `anonymity_enhancing_status`  (w=0.70); also under `risk_type_illicit_finance` (p=0.20), `sanctions_and_freezing_capability` (p=0.06), `virtual_asset_property_status` (p=0.04)
  - Illicit finance risk category `risk_type_illicit_finance`  (w=0.67); also under `sanctions_and_freezing_capability` (p=0.13), `virtual_asset_property_status` (p=0.09); IG 0.96 bits
  - Virtual assets as property or proceeds of crime `virtual_asset_property_status`  (w=0.66); IG 2.41 bits
    - Serious crime threshold for predicate offences `serious_crime_threshold`  (w=0.48); also under `risk_type_illicit_finance` (p=0.32), `sanctions_and_freezing_capability` (p=0.11), `aml_obligations_applicability` (p=0.09)
    - Excluded instrument category (EU scope exclusions) `excluded_instrument_category`  (w=0.14); IG 1.13 bits
      - MiFID financial instrument status `financial_instrument_status`  (w=0.69); IG 0.99 bits
        - Security status of digital asset (US exclusions) `securities_status_digital_asset`  (w=0.29); also under `excluded_instrument_category` (p=0.08); IG 0.54 bits
          - Investment contract (Howey) criteria `investment_contract_howey`  (w=0.61); also under `financial_instrument_status` (p=0.22), `excluded_instrument_category` (p=0.06); IG 1.56 bits
    - Yield or interest on stablecoin `stablecoin_interest_restriction`  (w=0.11); also under `securities_status_digital_asset` (p=0.09), `investment_contract_howey` (p=0.09); IG 0.50 bits
      - Redemption and reserve adequacy `redemption_risk_criteria`  (w=1.00); IG 1.88 bits
        - Traditional finance analogue `tradfi_analogue`  (w=0.62); also under `stablecoin_interest_restriction` (p=0.12), `settlement_finality_legal_test` (p=0.12), `investment_contract_howey` (p=0.12)
        - Settlement finality and legal enforceability `settlement_finality_legal_test`  (w=0.57); also under `virtual_asset_property_status` (p=0.09), `excluded_instrument_category` (p=0.07); IG 1.51 bits
          - ICT and operational resilience risk `operational_resilience_risk`  (w=0.28); also under `redemption_risk_criteria` (p=0.18), `prudential_classification_group` (p=0.15), `aml_obligations_applicability` (p=0.13)
        - Prudential classification group (Basel) `prudential_classification_group`  (w=0.45); also under `settlement_finality_legal_test` (p=0.21), `tradfi_analogue` (p=0.11)
  - Freezing and blocking capability `sanctions_and_freezing_capability`  (w=0.59); also under `virtual_asset_property_status` (p=0.22); IG 1.68 bits
    - Safeguarding and custody obligation `custody_safeguarding_obligation`  (w=0.36); also under `operational_resilience_risk` (p=0.26), `aml_obligations_applicability` (p=0.24), `regulated_status_cvc_mst_exemption` (p=0.14)
