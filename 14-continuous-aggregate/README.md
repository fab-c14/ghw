# Hourly continuous aggregate

Tiger Cloud service `ghw-hackweek` (`p182nhjnby`), following the [create a continuous aggregate](https://www.tigerdata.com/docs/build/continuous-aggregates/create-a-continuous-aggregate) guide.

`setup.sql` creates `conditions_summary_hourly` on the `conditions` hypertable. It buckets temperature by device and hour, and stores the average, max, and min. `refresh.sql` materializes the existing rows. `policy.sql` refreshes the view every hour, covering the last three days and stopping one hour short of now. `proof.sql` reads the view.

The refresh returned three hourly buckets for `sensor-1`: 22.1, 22.3, and 22.2. The policy job id is 1002. The materialized hypertable is `_materialized_hypertable_2`.

Console: https://console.cloud.tigerdata.com/dashboard/services/p182nhjnby

The database password stays in the system keyring and is not in this folder.
