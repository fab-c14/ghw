SELECT hypertable_name, num_dimensions
FROM timescaledb_information.hypertables
WHERE hypertable_name = 'conditions';

SELECT show_chunks('conditions') AS chunk;

SELECT time, location, device, temperature, humidity
FROM conditions
ORDER BY time DESC;
