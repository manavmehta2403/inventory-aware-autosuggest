# Inventory-aware autosuggest

**Typo-tolerant discovery with fresh inventory signals, not dead-end suggestions.**

An independent Python demonstration using synthetic records. Not employer source code or a production service.

## Pipeline

Query → normalization → fresh inventory filter → prefix/fuzzy ranking → top-k results.

- Accent/case normalization and RapidFuzz typo matching.
- Unavailable, stale and future-dated records excluded.
- Bounded LRU cache expires before inventory becomes stale.
- Inventory replacement invalidates cached results.
- No supplier calls on each query; no secrets or external services required.
- Eight deterministic tests for ranking, freshness, normalization, cache safety and input validation.

## Run (Python 3.10+)

```sh
python -m venv .venv
# Activate the environment for your operating system.
python -m pip install -r requirements.txt
python autosuggest.py
python -m unittest -v
```

Output: `['Paris Riverside Stay']`. The unavailable record is excluded.

## Trade-offs

A fresh snapshot is a discovery signal, **not a booking guarantee**. Revalidate dates, party size, price and inventory when booking. No 99% bookability or sub-50ms benchmark is claimed.

This single-threaded demo scans a small in-memory catalogue. Production requires indexed retrieval, ingestion, shared caches, concurrency controls and instrumentation.

## Provenance

Local source inspection showed OpenSearch contextual completion queries and progressive fuzzy fallback. This freshly written example uses different code and fake data. Snapshot filtering and bounded caching are demo features, not claims verified in the inspected source. No employer code, credentials, endpoints or Git history are included.

[Manav Mehta](https://github.com/manavmehta2403) · [LinkedIn](https://www.linkedin.com/in/manavmehta2403/)
