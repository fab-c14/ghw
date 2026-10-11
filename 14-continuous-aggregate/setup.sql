-- Hourly continuous aggregate on the conditions hypertable.
-- WITH NO DATA so it can be created inside a transaction, then refreshed.
-- Service: ghw-hackweek (p182nhjnby). Password stays in the system keyring.

CREATE MATERIALIZED VIEW conditions_summary_hourly
WITH (timescaledb.continuous) AS
SELECT
  device,
  time_bucket(INTERVAL '1 hour', time) AS bucket,
  AVG(temperature) AS avg_temperature,
  MAX(temperature) AS max_temperature,
  MIN(temperature) AS min_temperature
FROM conditions
GROUP BY device, bucket
WITH NO DATA;
