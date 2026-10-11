# First hypertable

Tiger Cloud service `ghw-hackweek` (`p182nhjnby`), following the [your first hypertable](https://www.tigerdata.com/docs/build/how-to/your-first-hypertable) guide.

`setup.sql` creates `conditions` as a hypertable partitioned on `time`, segmented by `device`. Three office readings were inserted. `proof.sql` shows the hypertable, its chunk, and the rows newest first.

Console: https://console.cloud.tigerdata.com/dashboard/services/p182nhjnby

The database password stays in the system keyring and is not in this folder.
