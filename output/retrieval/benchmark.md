# Retrieval benchmark

Index: catalogue v6, 33581 items, 149256 tags, 132 nodes. Latencies are per query on one core (best of 5 for the bitset engine, single run for the scans).

## Query latency

| workload | queries | mean result | bitset mean (us) | p95 (us) | flat scan (us) | flat, no closure (us) | speedup vs flat | vs no closure | mismatches |
|---|---|---|---|---|---|---|---|---|---|
| closure (1 node) | 132 | 5082.6 | 2.1 | 2.4 | 22124.7 | 19719.7 | 10461.4x | 9324.2x | 0 |
| direct (node!) | 125 | 1067.9 | 2.1 | 2.4 | 8268.7 | 10350.5 | 3902.8x | 4885.5x | 0 |
| value (node=value) | 463 | 322.4 | 2.9 | 3.3 | 26736.9 | 28564.3 | 9100.1x | 9722.1x | 0 |
| closure, strength >= 0.3 | 132 | 1991.7 | 6.0 | 13.8 | 22522.8 | 20242.8 | 3755.0x | 3374.9x | 0 |
| AND (2 atoms) | 300 | 146.1 | 6.5 | 7.6 | 29789.3 | 30865.3 | 4562.4x | 4727.2x | 0 |
| OR (2 atoms) | 300 | 2455.8 | 6.4 | 7.1 | 53096.3 | 55311.2 | 8348.8x | 8697.1x | 0 |
| AND NOT | 300 | 1479.2 | 9.1 | 10.1 | 30914.9 | 32051.9 | 3384.2x | 3508.7x | 0 |
| 3 atoms, mixed | 200 | 154.5 | 11.1 | 12.5 | 58397.0 | 59764.2 | 5261.8x | 5385.0x | 0 |

## Navigation by facet gain

300 random target items; the collection is narrowed by picking the facet option that contains the target until at most k = 10 items remain (ideal: 11.713 bits).

| policy | mean steps | bits resolved | bits / step | reached k | mean final size | ms / target |
|---|---|---|---|---|---|---|
| gain | 10.24 | 11.69 | 1.14 | 0.77 | 72.3 | 13.2 |
| random | 14.59 | 4.9 | 0.34 | 0.103 | 5206.1 | 22.87 |

Example trace (gain policy): ledger_purpose=data integrity and provenance ; smart_contract_usage_domain: not tagged ; -> ledger_node_role ; identity_binding_mechanism: not tagged ; ledger_node_role=tracking node (non-validating) ; ledger_access_permission: not tagged ; network_topology=decentralised ; service_provider_status: residual ; redemption_mechanism: residual ; ledger_storage_model: not tagged ; -> ledger_storage_model ; dlt_architecture: residual ; consensus_mechanism: not tagged ; ict_system_scope: residual ; digital_asset_recording: not tagged
