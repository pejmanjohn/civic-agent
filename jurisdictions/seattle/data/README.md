# Seattle Data

Seattle currently uses live Socrata access instead of checked-in data snapshots.

Primary source:

- `https://data.seattle.gov/resource/8u2j-imqx.json`
- `https://data.seattle.gov/resource/8u2j-imqx.csv?$limit=50000`

Snapshot policy:

- Keep live queries as the default while the Socrata source remains clean and small.
- Add checked-in snapshots if the public API changes, rate limits become an issue, or downstream tools need deterministic offline tests.
- Any future snapshot should include raw data, normalized data, summary stats, and provenance.
