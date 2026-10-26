# Task B output: is-a hierarchy of term types

Consolidated DAG per category. Each child keeps the most probable parents that are >= 0.25, exceed its own P(none) and do not create a cycle; the first is the primary parent used for the tree below, further parents are listed as *also under*. Roots are children with no kept parent. Full distributions: `output/is_a.json`; all weighted edges: `output/is_a_edges.csv`.

## asset

21 term types, 5 roots, 3 with more than one parent.

- Hosted versus unhosted (self-hosted) wallet `unhosted_vs_hosted_wallet`  (root, P(none)=0.30)
- Source of yield `yield_source`  (root, P(none)=0.25)
  - Yield distribution mechanism `yield_distribution_mechanism`  (p=0.45)
- Economic function of the asset `crypto_asset_function`  (root, P(none)=0.20)
  - Legal classification of crypto-asset `legal_classification_status`  (p=0.34)
    - Reference asset type `asset_reference_type`  (p=0.30)
      - Reference currency for stablecoin peg (currency vs other) `native_vs_stable_price_reference_asset_currency`  (p=0.62)
      - Payment stablecoin / e-money / ART regulatory class `stablecoin_regulatory_class`  (p=0.45)
      - Redemption mechanism `redemption_mechanism`  (p=0.42)
      - Tokenisation form `tokenisation_form`  (p=0.32)
    - Issuer identifiability `issuer_presence`  (p=0.30)
      - Centralisation of control `centralisation_level`  (p=0.42)
  - Ancillary asset and network token status `ancillary_asset_status`  (p=0.30); also under `issuer_presence` (p=0.25)
- Form of holder claim `claim_form`  (root, P(none)=0.10)
- Crypto-asset definitional criteria `crypto_asset_scope_criteria`  (root, P(none)=0.05)
  - Recording and cryptographic linkage `digital_asset_recording`  (p=0.81)
  - Central bank digital currency status `central_bank_digital_currency`  (p=0.56)
  - Fungibility `fungibility`  (p=0.55)
  - Convertible virtual currency (CVC) status `convertible_virtual_currency_status`  (p=0.55)
  - Native asset versus token standard `native_vs_token_standard`  (p=0.30); also under `digital_asset_recording` (p=0.25)
    - Wrapped / cross-chain representation `wrapped_or_bridged_asset`  (p=0.45); also under `tokenisation_form` (p=0.25)

## technology

24 term types, 9 roots, 2 with more than one parent.

- Software architecture (monolithic vs polylithic) `software_architecture`  (root, P(none)=0.82)
- Smart contract / distributed ledger application scope `smart_contract_definition_scope`  (root, P(none)=0.78)
  - Smart contract / script language expressiveness `script_language_expressiveness`  (p=0.42)
    - Interoperability and intraoperability `interoperability_type`  (p=0.46)
  - Source code openness `code_license_openness`  (p=0.36)
- Wallet storage mode (hot or cold) `wallet_type_storage`  (root, P(none)=0.73)
- Information and communications technology system `ict_system_scope`  (root, P(none)=0.55)
  - Data classification (traffic, content, subscriber) `traffic_and_subscriber_data_class`  (p=0.56)
- Ledger access and permissioning `ledger_access_permission`  (root, P(none)=0.50)
  - Ledger scope: open or closed access by design `dlt_network_access_scope`  (p=0.80)
    - Network topology and node roles `network_topology`  (p=0.38); also under `ledger_access_permission` (p=0.30)
      - Node / DLT network node role `ledger_node_role`  (p=0.50)
  - Identity layer and onboarding `digital_identity_layer`  (p=0.55)
  - Governance model of a DLT system `governance_model`  (p=0.42)
    - Decentralised system certification `decentralised_system_status`  (p=0.42); also under `ledger_access_permission` (p=0.30)
- Consensus mechanism `consensus_mechanism`  (root, P(none)=0.50)
  - Finality of agreement `consensus_finality`  (p=0.62)
  - Validator reward mechanism `reward_mechanism`  (p=0.55)
    - Transaction fee regime `fee_structure`  (p=0.55)
- Native asset presence and type `native_asset_type`  (root, P(none)=0.40)
  - Asset supply management (monetary policy) `asset_supply_policy`  (p=0.60)
- Privacy and anonymity features `privacy_enhancement`  (root, P(none)=0.30)
- DLT data structure (blockchain vs non-chain DLT) `dlt_architecture`  (root, P(none)=0.20)
  - Ledger storage model (what is stored on chain) `ledger_storage_model`  (p=0.42)

## actor

19 term types, 6 roots, 5 with more than one parent.

- Consumer or retail versus professional user `consumer_vs_professional_status`  (root, P(none)=0.88)
- Operator of crypto-asset arrangement `crypto_asset_operator`  (root, P(none)=0.58)
- Pooled investment vehicle structure `fund_or_pooled_vehicle`  (root, P(none)=0.32)
- Crypto-asset service provider or VASP status `service_provider_status`  (root, P(none)=0.23)
  - Infrastructure provider type `infrastructure_provider_type`  (p=0.62)
  - Offshore VASP status (activity-based or location-based) `offshore_vasp_status`  (p=0.62)
  - Trading venue type `exchange_venue_type`  (p=0.55); also under `actor_role_in_service` (p=0.25)
  - Control or sufficient influence over DeFi arrangement `decentralised_control_status_actor`  (p=0.55)
  - Jurisdictional regime and home or host state `regulatory_regime_scope_jurisdictional`  (p=0.51); also under `offshore_vasp_status` (p=0.26)
  - Principal or agent role in transaction `actor_role_in_service`  (p=0.50)
    - Originator and beneficiary role `party_role_transfer`  (p=0.42); also under `service_provider_status` (p=0.30)
  - Financial institution status for AML `regulatory_perimeter_fi_status`  (p=0.42)
  - Stablecoin issuer model `stablecoin_issuer_model`  (p=0.40); also under `ecosystem_participant_role` (p=0.25)
- Ecosystem participant role `ecosystem_participant_role`  (root, P(none)=0.15)
  - Related person and affiliated person status `related_person_affiliation`  (p=0.52)
  - Validator operation capacity (who may run a node) `consensus_participant_validator_capacity`  (p=0.42)
- Custody model `custodian_or_custody_model`  (root, P(none)=0.12)
  - Permitted control over client assets (unilateral vs multi-party control) `unhosted_custody_control_policy`  (p=0.62)
    - Address linkage to service provider `self_hosted_address_status`  (p=0.43); also under `custodian_or_custody_model` (p=0.31)

## activity

10 term types, 2 roots, 2 with more than one parent.

- Crypto-asset service type `crypto_asset_service_type`  (root, P(none)=0.10)
  - Transfer of crypto-assets (travel rule scope) `transfer_of_crypto_assets`  (p=0.55)
    - Peer-to-peer (P2P) transaction `transaction_type_p2p`  (p=0.55)
    - Payment service and funds transfer `payment_or_transfer_service`  (p=0.50)
    - Money transmission (acceptance and transmission of value) `regulated_transmission_of_value`  (p=0.42); also under `crypto_asset_service_type` (p=0.25)
  - Staking arrangement (self, delegated, custodial, liquid) `staking_arrangement`  (p=0.50)
    - Minting mechanism `minting_mechanism`  (p=0.29); also under `offer_and_issuance_method` (p=0.29)
  - Nexus to jurisdiction (services offered in jurisdiction) `service_location_nexus`  (p=0.45)
- Public offer or private placement `decentralised_or_centralised_offer_model`  (root, P(none)=0.05)
  - Offer and issuance method (token distribution) `offer_and_issuance_method`  (p=0.55)

## obligation_or_risk

19 term types, 4 roots, 2 with more than one parent.

- Redemption and reserve adequacy `redemption_risk_criteria`  (root, P(none)=1.00)
  - Settlement finality and legal enforceability `settlement_finality_legal_test`  (p=0.52)
  - Yield or interest on stablecoin `stablecoin_interest_restriction`  (p=0.50)
  - Traditional finance analogue `tradfi_analogue`  (p=0.50)
  - Prudential classification group (Basel) `prudential_classification_group`  (p=0.42)
- ICT and operational resilience risk `operational_resilience_risk`  (root, P(none)=0.22)
- Excluded instrument category (EU scope exclusions) `excluded_instrument_category`  (root, P(none)=0.15)
  - MiFID financial instrument status `financial_instrument_status`  (p=0.62)
    - Security status of digital asset (US exclusions) `securities_status_digital_asset`  (p=0.25)
      - Investment contract (Howey) criteria `investment_contract_howey`  (p=0.55)
- Anti-money laundering obligations `aml_obligations_applicability`  (root, P(none)=0.12)
  - Anonymity-enhancing crypto-asset status `anonymity_enhancing_status`  (p=0.62)
  - Virtual assets as property or proceeds of crime `virtual_asset_property_status`  (p=0.62)
    - Serious crime threshold for predicate offences `serious_crime_threshold`  (p=0.42); also under `risk_type_illicit_finance` (p=0.28)
  - Illicit finance risk category `risk_type_illicit_finance`  (p=0.62)
  - Exemption from MSB status `regulated_status_cvc_mst_exemption`  (p=0.62)
    - Tax reporting obligation status (CARF) `tax_reporting_status`  (p=0.36); also under `aml_obligations_applicability` (p=0.34)
  - Freezing and blocking capability `sanctions_and_freezing_capability`  (p=0.55)
    - Safeguarding and custody obligation `custody_safeguarding_obligation`  (p=0.30)
