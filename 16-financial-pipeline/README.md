# Real-time financial pipeline

Tiger Cloud service `ghw-hackweek` (`p182nhjnby`). The schema follows the [ingest real-time financial data](https://www.tigerdata.com/docs/build/examples/ingest-real-time-financial-data) guide: a `crypto_ticks` hypertable, a `crypto_assets` table, and a `one_day_candle` continuous aggregate.

The guide's websocket is Twelve Data, which needs an API key that is not on this machine. `pipeline.py` uses Binance's public trade stream for `BTC/USD` and `ETH/USD` instead, batches the trades, and inserts them into `crypto_ticks`. A one-minute candle view is there as well, because a short capture does not span a full day.

This run stored 110 Bitcoin ticks and 15 Ethereum ticks. Bitcoin traded between 83830.00 and 83858.06. Ethereum traded between 2544.16 and 2547.82.

`candles.sql` creates both views with `WITH NO DATA`. Refresh each view with its own `tiger db query` call. A combined script wraps them in one transaction, and TimescaleDB rejects that.

Console: https://console.cloud.tigerdata.com/dashboard/services/p182nhjnby

The database password stays in the system keyring and is not in this folder.
