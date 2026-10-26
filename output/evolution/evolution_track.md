# Evolution of the taxonomy DAG as content is fed in

Seed v0 is the Part 1 DAG; each later version is produced by one iteration of tagging a disjoint DLT-Corpus batch, measuring the DAG on it, discovering candidates at impure nodes and consolidating the accepted ones. Cumulative items = items tagged before the version existed.

## Structure per version

| version | from iteration | cumulative items | nodes (candidate) | edges | values (candidate) | roots | leaves | max depth | mean parents | prior bits/descent | prior AUC | prior eff. leaves |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v0 | seed | 0 | 93 (0) | 279 | 317 (0) | 5 | 18 | 14 | 3.0 | 4.7155 | 0.8353 | 13.987 |
| v1 | 1 | 300 | 99 (6) | 285 | 351 (34) | 5 | 24 | 14 | 2.88 | 4.8239 | 0.8427 | 18.496 |
| v2 | 2 | 8946 | 107 (14) | 293 | 396 (79) | 5 | 28 | 15 | 2.74 | 4.8413 | 0.8506 | 22.452 |
| v3 | 3 | 17592 | 113 (20) | 300 | 433 (116) | 5 | 30 | 15 | 2.65 | 4.8767 | 0.8427 | 23.087 |
| v4 | 4 | 26238 | 124 (31) | 311 | 491 (174) | 5 | 35 | 15 | 2.51 | 5.0082 | 0.8332 | 25.719 |
| v5 | 5 | 34884 | 128 (35) | 316 | 529 (212) | 5 | 38 | 15 | 2.47 | 5.0241 | 0.8331 | 26.075 |
| v6 | 6 | 36702 | 132 (39) | 320 | 549 (232) | 5 | 40 | 16 | 2.42 | 5.037 | 0.8402 | 26.308 |

## Content-driven objectives per iteration

| iteration | catalogue | items | tags/item | bits/descent | AUC | expected depth | eff. leaves | eff. leaves / nodes | collapsed | targets | candidates | accepted | cost | wall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | v0 | 300 | 3.55 | 6.9161 | 0.7943 | 3.373 | 19.73 | 0.2122 | 3 | 15 | 32 | 8 | $0.1541 | 1.8 min |
| 2 | v1 | 8646 | 4.06 | 6.9602 | 0.7714 | 3.6958 | 21.256 | 0.2147 | 11 | 32 | 81 | 21 | $4.2902 | 33.7 min |
| 3 | v2 | 8646 | 4.11 | 7.0214 | 0.7781 | 3.826 | 21.747 | 0.2032 | 12 | 32 | 87 | 17 | $4.4534 | 12.4 min |
| 4 | v3 | 8646 | 4.16 | 7.2153 | 0.7796 | 3.8027 | 24.68 | 0.2184 | 13 | 42 | 106 | 18 | $4.5899 | 13.2 min |
| 5 | v4 | 8646 | 4.09 | 7.2712 | 0.7734 | 3.8959 | 24.792 | 0.1999 | 12 | 45 | 127 | 24 | $4.7304 | 12.7 min |
| 6 | v5 | 1818 | 4.03 | 7.0636 | 0.7734 | 3.8953 | 22.947 | 0.1793 | 9 | 36 | 79 | 6 | $1.0687 | 2.9 min |

## Discovered term types and their later usage

| term type | discovered in | version | parent(s) | items tagged on it in later iterations |
|---|---|---|---|---|
| `privacy_mechanism_family` | iteration 1 | v1 | privacy_enhancement | iter_2: 613, iter_3: 567, iter_4: 569, iter_5: 564, iter_6: 110 |
| `smart_contract_deployment_context` | iteration 1 | v1 | script_language_expressiveness | iter_2: 161, iter_3: 142, iter_4: 83, iter_5: 116, iter_6: 37 |
| `smart_contract_usage_domain` | iteration 1 | v1 | smart_contract_definition_scope | iter_2: 1347, iter_3: 1416, iter_4: 1471, iter_5: 1608, iter_6: 426 |
| `identity_binding_mechanism` | iteration 1 | v1 | digital_identity_layer | iter_2: 994, iter_3: 1281, iter_4: 1200, iter_5: 1139, iter_6: 206 |
| `ledger_purpose` | iteration 1 | v1 | digital_asset_recording | iter_2: 4890, iter_3: 5629, iter_4: 5004, iter_5: 5447, iter_6: 1057 |
| `ledger_partitioning_topology` | iteration 1 | v1 | dlt_architecture | iter_2: 340, iter_3: 513, iter_4: 547, iter_5: 518, iter_6: 147 |
| `cross_chain_transfer_mechanism` | iteration 2 | v2 | wrapped_or_bridged_asset | iter_3: 86, iter_4: 51, iter_5: 29, iter_6: 0 |
| `key_custody_control_model` | iteration 2 | v2 | wallet_type_storage | iter_3: 277, iter_4: 267, iter_5: 203, iter_6: 21 |
| `finality_mechanism` | iteration 2 | v2 | consensus_finality | iter_3: 21, iter_4: 17, iter_5: 37, iter_6: 9 |
| `key_isolation_from_network` | iteration 2 | v2 | unhosted_vs_hosted_wallet | iter_3: 55, iter_4: 60, iter_5: 42, iter_6: 10 |
| `payment_settlement_mechanism` | iteration 2 | v2 | payment_or_transfer_service | iter_3: 71, iter_4: 120, iter_5: 83, iter_6: 9 |
| `key_splitting_scheme` | iteration 2 | v2 | unhosted_custody_control_policy | iter_3: 111, iter_4: 97, iter_5: 101, iter_6: 12 |
| `expressiveness_claim_basis` | iteration 2 | v2 | script_language_expressiveness | iter_3: 2, iter_4: 8, iter_5: 4, iter_6: 1 |
| `key_management_control_model` | iteration 2 | v2 | crypto_asset_service_type | iter_3: 35, iter_4: 81, iter_5: 76, iter_6: 7 |
| `zk_proof_system_variant` | iteration 3 | v3 | privacy_mechanism_family | iter_4: 36, iter_5: 60, iter_6: 7 |
| `key_share_distribution_topology` | iteration 3 | v3 | key_management_control_model, key_splitting_scheme | iter_4: 19, iter_5: 32, iter_6: 4 |
| `fiat_rail_integration` | iteration 3 | v3 | payment_settlement_mechanism | iter_4: 30, iter_5: 42, iter_6: 4 |
| `key_recovery_mechanism` | iteration 3 | v3 | unhosted_vs_hosted_wallet | iter_4: 42, iter_5: 38, iter_6: 2 |
| `script_verification_approach` | iteration 3 | v3 | script_language_expressiveness | iter_4: 51, iter_5: 42, iter_6: 27 |
| `backing_of_token` | iteration 3 | v3 | tokenisation_form | iter_4: 25, iter_5: 38, iter_6: 4 |
| `deanonymisation_tracing_approach` | iteration 4 | v4 | anonymity_enhancing_status | iter_5: 39, iter_6: 11 |
| `backing_mechanism` | iteration 4 | v4 | backing_of_token | iter_5: 22, iter_6: 6 |
| `settlement_finality_timing` | iteration 4 | v4 | payment_settlement_mechanism | iter_5: 37, iter_6: 6 |
| `settlement_counterparty` | iteration 4 | v4 | fiat_rail_integration | iter_5: 8, iter_6: 0 |
| `physical_transfer_mechanism_air_gap` | iteration 4 | v4 | key_isolation_from_network | iter_5: 8, iter_6: 3 |
| `validator_selection_mechanism` | iteration 4 | v4 | consensus_participant_validator_capacity | iter_5: 92, iter_6: 38 |
| `sharding_partition_basis` | iteration 4 | v4 | ledger_partitioning_topology | iter_5: 36, iter_6: 9 |
| `wallet_interface_delivery_form` | iteration 4 | v4 | unhosted_vs_hosted_wallet | iter_5: 50, iter_6: 9 |
| `share_recovery_mechanism` | iteration 4 | v4 | key_splitting_scheme | iter_5: 17, iter_6: 1 |
| `centralisation_locus` | iteration 4 | v4 | centralisation_level | iter_5: 304, iter_6: 70 |
| `cross_chain_interoperability_mechanism` | iteration 4 | v4 | wrapped_or_bridged_asset | iter_5: 108, iter_6: 22 |
| `isolation_mechanism` | iteration 5 | v5 | key_isolation_from_network | iter_6: 6 |
| `key_distribution_method` | iteration 5 | v5 | key_isolation_from_network, physical_transfer_mechanism_air_gap | iter_6: 3 |
| `finality_guarantee_mode` | iteration 5 | v5 | consensus_finality | iter_6: 4 |
| `key_share_cryptographic_primitive` | iteration 5 | v5 | key_splitting_scheme | iter_6: 6 |
| `zk_proof_application_role` | iteration 6 | v6 | zk_proof_system_variant | none yet |
| `key_storage_medium` | iteration 6 | v6 | key_custody_control_model | none yet |
| `ledger_parent_child_coupling` | iteration 6 | v6 | ledger_partitioning_topology | none yet |
| `finality_guarantee_source` | iteration 6 | v6 | consensus_finality | none yet |

## Nodes by category per version

| version | asset | technology | actor | activity | obligation_or_risk |
|---|---|---|---|---|---|
| v0 | 21 | 24 | 19 | 10 | 19 |
| v1 | 21 | 30 | 19 | 10 | 19 |
| v2 | 22 | 35 | 19 | 12 | 19 |
| v3 | 23 | 39 | 19 | 13 | 19 |
| v4 | 25 | 45 | 20 | 14 | 20 |
| v5 | 25 | 49 | 20 | 14 | 20 |
| v6 | 25 | 53 | 20 | 14 | 20 |
