-- One-minute candles so a short live capture still has OHLCV buckets.
-- The guide's daily view is included as well.

CREATE MATERIALIZED VIEW one_minute_candle
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 minute', time) AS bucket,
  symbol,
  FIRST(price, time) AS open,
  MAX(price) AS high,
  MIN(price) AS low,
  LAST(price, time) AS close,
  SUM(day_volume) AS volume
FROM crypto_ticks
GROUP BY bucket, symbol
WITH NO DATA;

CREATE MATERIALIZED VIEW one_day_candle
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 day', time) AS bucket,
  symbol,
  FIRST(price, time) AS open,
  MAX(price) AS high,
  MIN(price) AS low,
  LAST(price, time) AS close,
  LAST(day_volume, time) AS day_volume
FROM crypto_ticks
GROUP BY bucket, symbol
WITH NO DATA;
