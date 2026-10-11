SELECT view_name, materialization_hypertable_name
FROM timescaledb_information.continuous_aggregates
WHERE view_name = 'conditions_summary_hourly';

SELECT device, bucket, avg_temperature, max_temperature, min_temperature
FROM conditions_summary_hourly
ORDER BY bucket DESC;
