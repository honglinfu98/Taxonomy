# Task B output: is-a hierarchy of term types

For each term type X (child), the most probable parent Y with P(X is-a Y); `none` means X is top-level in its category. Full distributions are in `output/is_a.json`.

## asset

- Reference asset type `asset_reference_type` is-a `legal_classification_status` (p=0.3) — in a cycle, no root
- Issuer identifiability `issuer_presence` is-a `legal_classification_status` (p=0.3) — in a cycle, no root
