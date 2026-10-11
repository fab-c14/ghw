-- Financial ticks hypertable from the Tiger Data real-time finance guide.
-- Service: ghw-hackweek (p182nhjnby). Password stays in the system keyring.

CREATE TABLE crypto_ticks (
  time TIMESTAMPTZ,
  symbol TEXT,
  price DOUBLE PRECISION,
  day_volume NUMERIC
) WITH (
  tsdb.hypertable,
  tsdb.segmentby = 'symbol',
  tsdb.orderby = 'time DESC'
);

CREATE TABLE crypto_assets (
  symbol TEXT UNIQUE,
  name TEXT
);

INSERT INTO crypto_assets (symbol, name) VALUES
  ('BTC/USD', 'Bitcoin'),
  ('ETH/USD', 'Ethereum');
