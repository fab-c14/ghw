"""Batch real-time trades into crypto_ticks.

Twelve Data needs an API key that is not on this machine. This pipeline uses
Binance's public trade websocket instead, and writes the same hypertable the
Tiger Data guide defines. The database password stays in the system keyring.
"""

import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from websocket import create_connection

TIGER = r"C:\Users\plesi\AppData\Local\Programs\TigerCLI\tiger.exe"
SERVICE = "p182nhjnby"
STREAM = "wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade"
SYMBOLS = {"BTCUSDT": "BTC/USD", "ETHUSDT": "ETH/USD"}
BATCH_SIZE = 25
TARGET_ROWS = 80


def insert(rows):
    values = []
    for stamp, symbol, price, volume in rows:
        values.append(
            "('%s','%s',%s,%s)"
            % (stamp.isoformat(), symbol, float(price), float(volume))
        )
    sql = (
        "INSERT INTO crypto_ticks (time, symbol, price, day_volume) VALUES "
        + ",".join(values)
        + ";"
    )
    fd, name = tempfile.mkstemp(suffix=".sql")
    os.close(fd)
    path = Path(name)
    path.write_text(sql, encoding="utf-8")
    try:
        result = subprocess.run(
            [TIGER, "db", "query", SERVICE, "-f", str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(result.stdout.strip())
    finally:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass


def main():
    ws = create_connection(STREAM, timeout=15)
    batch = []
    stored = 0
    try:
        while stored < TARGET_ROWS:
            payload = json.loads(ws.recv())
            trade = payload.get("data", {})
            if trade.get("e") != "trade":
                continue
            symbol = SYMBOLS.get(trade.get("s"))
            if symbol is None:
                continue
            stamp = datetime.fromtimestamp(trade["T"] / 1000, tz=timezone.utc)
            batch.append((stamp, symbol, trade["p"], trade["q"]))
            if len(batch) >= BATCH_SIZE:
                insert(batch)
                stored += len(batch)
                print(f"inserted {stored}")
                batch = []
        if batch:
            insert(batch)
            stored += len(batch)
            print(f"inserted {stored}")
    finally:
        ws.close()


if __name__ == "__main__":
    main()
