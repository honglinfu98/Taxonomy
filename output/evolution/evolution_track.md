# Evolution of the taxonomy DAG as content is fed in

Seed v0 is the Part 1 DAG; each later version is produced by one iteration of tagging a disjoint DLT-Corpus batch, measuring the DAG on it, discovering candidates at impure nodes and consolidating the accepted ones. Cumulative items = items tagged before the version existed.

## Structure per version

| version | from iteration | cumulative items | nodes (candidate) | edges | values (candidate) | roots | leaves | max depth | mean parents | prior bits/descent | prior AUC | prior eff. leaves |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v0 | seed | 0 | 93 (0) | 279 | 317 (0) | 5 | 18 | 14 | 3.0 | 4.7155 | 0.8353 | 13.987 |
| v1 | 1 | 300 | 99 (6) | 285 | 351 (34) | 5 | 24 | 14 | 2.88 | 4.8239 | 0.8427 | 18.496 |
| v2 | 2 | 8946 | 107 (14) | 293 | 396 (79) | 5 | 28 | 15 | 2.74 | 4.8413 | 0.8506 | 22.452 |

## Content-driven objectives per iteration

| iteration | catalogue | items | tags/item | bits/descent | AUC | expected depth | eff. leaves | eff. leaves / nodes | collapsed | targets | candidates | accepted | cost | wall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | v0 | 300 | 3.55 | 6.9161 | 0.7943 | 3.373 | 19.73 | 0.2122 | 3 | 15 | 32 | 8 | $0.1541 | 1.8 min |
| 2 | v1 | 8646 | 4.06 | 6.9602 | 0.7714 | 3.6958 | 21.256 | 0.2147 | 11 | 32 | 81 | 21 | $4.2902 | 33.7 min |

## Discovered term types and their later usage

| term type | discovered in | version | parent(s) | items tagged on it in later iterations |
|---|---|---|---|---|
| `privacy_mechanism_family` | iteration 1 | v1 | privacy_enhancement | iter_2: 613 |
| `smart_contract_deployment_context` | iteration 1 | v1 | script_language_expressiveness | iter_2: 161 |
| `smart_contract_usage_domain` | iteration 1 | v1 | smart_contract_definition_scope | iter_2: 1347 |
| `identity_binding_mechanism` | iteration 1 | v1 | digital_identity_layer | iter_2: 994 |
| `ledger_purpose` | iteration 1 | v1 | digital_asset_recording | iter_2: 4890 |
| `ledger_partitioning_topology` | iteration 1 | v1 | dlt_architecture | iter_2: 340 |
| `cross_chain_transfer_mechanism` | iteration 2 | v2 | wrapped_or_bridged_asset | none yet |
| `key_custody_control_model` | iteration 2 | v2 | wallet_type_storage | none yet |
| `finality_mechanism` | iteration 2 | v2 | consensus_finality | none yet |
| `key_isolation_from_network` | iteration 2 | v2 | unhosted_vs_hosted_wallet | none yet |
| `payment_settlement_mechanism` | iteration 2 | v2 | payment_or_transfer_service | none yet |
| `key_splitting_scheme` | iteration 2 | v2 | unhosted_custody_control_policy | none yet |
| `expressiveness_claim_basis` | iteration 2 | v2 | script_language_expressiveness | none yet |
| `key_management_control_model` | iteration 2 | v2 | crypto_asset_service_type | none yet |

## Nodes by category per version

| version | asset | technology | actor | activity | obligation_or_risk |
|---|---|---|---|---|---|
| v0 | 21 | 24 | 19 | 10 | 19 |
| v1 | 21 | 30 | 19 | 10 | 19 |
| v2 | 22 | 35 | 19 | 12 | 19 |
