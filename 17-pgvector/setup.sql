-- Vector search beside the hack week time-series data.
-- Service: ghw-hackweek (p182nhjnby). Password stays in the system keyring.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE hackweek_notes (
  time TIMESTAMPTZ NOT NULL,
  topic TEXT NOT NULL,
  body TEXT NOT NULL,
  embedding vector(768)
);
