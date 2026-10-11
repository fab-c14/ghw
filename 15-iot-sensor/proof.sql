SELECT id, type, location
FROM sensors
ORDER BY id;

SELECT count(*) AS reading_count
FROM sensor_data;

SELECT hypertable_name
FROM timescaledb_information.hypertables
WHERE hypertable_name = 'sensor_data';

SELECT
  sensors.location,
  time_bucket('30 minutes', sensor_data.time) AS period,
  round(AVG(temperature)::numeric, 2) AS avg_temp,
  round(AVG(cpu)::numeric, 3) AS avg_cpu
FROM sensor_data
JOIN sensors ON sensor_data.sensor_id = sensors.id
GROUP BY period, sensors.location
ORDER BY period DESC, sensors.location
LIMIT 6;
