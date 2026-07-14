# Pierce County Data

Both Pierce County sources are `live` tier: normal answers query the official Socrata endpoints at answer time and no snapshots are checked in here.

If the live endpoints drift from the source cards' validation checks (see `scripts/drift.py`), refresh the card fingerprints rather than adding snapshots, unless the portal becomes unreliable enough to justify promoting a checked-in snapshot per `docs/source-data-storage.md`.
