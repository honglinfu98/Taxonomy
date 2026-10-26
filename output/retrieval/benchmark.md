# Retrieval benchmark

Index: catalogue v2, 8205 items, 35884 tags, 107 nodes. Latencies are per query on one core (best of 5 for the bitset engine, single run for the scans).

## Query latency

| workload | queries | mean result | bitset mean (us) | p95 (us) | flat scan (us) | flat, no closure (us) | speedup vs flat | vs no closure | mismatches |
|---|---|---|---|---|---|---|---|---|---|
| closure (1 node) | 107 | 1473.6 | 2.1 | 2.3 | 5130.6 | 4514.8 | 2438.6x | 2145.9x | 0 |
| direct (node!) | 91 | 360.2 | 2.1 | 2.6 | 1991.2 | 2505.8 | 935.0x | 1176.7x | 0 |
| value (node=value) | 285 | 125.9 | 2.8 | 3.2 | 6488.3 | 6948.6 | 2285.6x | 2447.8x | 0 |
| closure, strength >= 0.3 | 107 | 579.3 | 4.9 | 10.1 | 5422.9 | 4816.9 | 1111.0x | 986.8x | 0 |
| AND (2 atoms) | 300 | 63.4 | 5.6 | 6.4 | 7315.1 | 7491.7 | 1304.4x | 1335.9x | 0 |
| OR (2 atoms) | 300 | 1070.7 | 5.7 | 6.6 | 12533.7 | 12783.4 | 2192.4x | 2236.1x | 0 |
| AND NOT | 300 | 475.9 | 6.9 | 7.8 | 7485.4 | 7621.4 | 1090.5x | 1110.3x | 0 |
| 3 atoms, mixed | 200 | 52.7 | 9.9 | 11.2 | 14204.3 | 14479.1 | 1436.8x | 1464.6x | 0 |

## Navigation by facet gain

300 random target items; the collection is narrowed by picking the facet option that contains the target until at most k = 10 items remain (ideal: 9.68 bits).

| policy | mean steps | bits resolved | bits / step | reached k | mean final size | ms / target |
|---|---|---|---|---|---|---|
| gain | 8.2 | 10.22 | 1.25 | 0.863 | 18.2 | 4.37 |
| random | 14.26 | 5.7 | 0.4 | 0.2 | 792.5 | 9.07 |

Example trace (gain policy): ledger_purpose=value transfer ; service_provider_status: residual ; smart_contract_usage_domain: not tagged ; dlt_network_access_scope: residual ; -> claim_form ; crypto_asset_function=good, collectible or non-commodity asset ; crypto_asset_scope_criteria=DLT-recorded digital representation of value or right
