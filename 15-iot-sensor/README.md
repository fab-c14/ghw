# Simulated IoT sensor dataset

Tiger Cloud service `ghw-hackweek` (`p182nhjnby`), following the [simulate IoT sensor data](https://www.tigerdata.com/docs/build/examples/simulate-iot-sensor-data) guide.

`setup.sql` creates four sensors and the `sensor_data` hypertable, then inserts a reading every five minutes for the last 24 hours. That is 1,156 rows. `proof.sql` lists the sensors and the latest 30-minute average temperature and CPU by location.

Console: https://console.cloud.tigerdata.com/dashboard/services/p182nhjnby

The database password stays in the system keyring and is not in this folder.
