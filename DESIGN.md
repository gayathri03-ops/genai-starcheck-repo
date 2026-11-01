# StarWise design

Tells shoppers what a BEE star label really means and checks sellers' energy-saving claims.

## API endpoints

| Method | Path | What it does | Status |
|---|---|---|---|
| GET | /health | Liveness: process is up. Touches nothing. | done |
| GET | /ready | Readiness: runs `SELECT 1` on Postgres, 3 s timeout. 503 if the database is down. | done |
| POST | /chat | Streams an answer as server-sent events. Logs tokens, latency and cost per call. | done |
| GET | /usage | Calls, tokens and cost per UTC day, read from `logs/cost.jsonl`. | done |
| POST | /decode | Label decoder: appliance + stars + label year -> energy band, yearly units, still current? | planned |

## LLM calls

- `/chat` talks to an `LLMProvider` interface, never to a vendor SDK.
- Providers: `FakeProvider` (tests, CI), `OpenAICompatProvider` (hosted or local models), `FallbackProvider` (main, then backup).
- Retries only on timeouts, connection errors, 429 and 5xx, with capped exponential backoff and full jitter. Never on 400, 401, 403, 404. Never after text has been streamed.
- The fallback model answers only on `LLMUnavailable` and only before any text was sent.

## Tables (Postgres + pgvector)

Planned for Week 3. Today the database only needs to start and answer `/ready`.

| Table | Columns | Purpose |
|---|---|---|
| documents | id, appliance, title, source_url, language, effective_from, valid_until, sha256, downloaded_on | One row per BEE document, with its validity period |
| chunks | id, document_id, page, text, embedding (vector) | Text pieces and their embeddings for search |
| star_levels | id, document_id, appliance, star, min_value, max_value, unit, label_year | Star tables for the label decoder |

## Files written by the app

- `logs/cost.jsonl`: one JSON line per LLM call (provider, model, tokens, latency, cost, ok, fallback_used). Not committed.