"""Embed hack week notes with the local nomic-embed-text model and store them."""

import json
import os
import subprocess
import tempfile
import urllib.request
from pathlib import Path

TIGER = r"C:\Users\plesi\AppData\Local\Programs\TigerCLI\tiger.exe"
SERVICE = "p182nhjnby"
NOTES = [
    (
        "2026-10-11 14:35:00+00",
        "office sensor",
        "sensor-1 in the office read 22.1 degrees and 45 percent humidity",
    ),
    (
        "2026-10-11 16:30:00+00",
        "iot sensors",
        "floor and ceiling sensors reported temperature and cpu over the last day",
    ),
    (
        "2026-10-11 16:35:00+00",
        "hourly rollup",
        "the continuous aggregate stores hourly average minimum and maximum temperature",
    ),
    (
        "2026-10-11 17:01:00+00",
        "crypto trades",
        "bitcoin traded around 83830 dollars and ethereum around 2544",
    ),
]


def embed(text):
    body = json.dumps({"model": "nomic-embed-text", "input": "search_document: " + text}).encode()
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/embed",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = json.load(response)
    vector = payload["embeddings"][0]
    if len(vector) != 768:
        raise SystemExit(f"expected 768 dimensions, got {len(vector)}")
    return vector


def main():
    values = []
    for stamp, topic, body in NOTES:
        vector = embed(body)
        literal = "[" + ",".join(f"{number:.8f}" for number in vector) + "]"
        safe_topic = topic.replace("'", "''")
        safe_body = body.replace("'", "''")
        values.append(f"('{stamp}','{safe_topic}','{safe_body}','{literal}')")
        print(topic, len(vector))
    sql = (
        "INSERT INTO hackweek_notes (time, topic, body, embedding) VALUES\n"
        + ",\n".join(values)
        + ";\n"
    )
    out = Path(__file__).with_name("insert.sql")
    out.write_text(sql, encoding="utf-8")
    fd, name = tempfile.mkstemp(suffix=".sql")
    os.close(fd)
    temp = Path(name)
    temp.write_text(sql, encoding="utf-8")
    try:
        subprocess.run([TIGER, "db", "query", SERVICE, "-f", str(temp)], check=True)
    finally:
        try:
            temp.unlink(missing_ok=True)
        except OSError:
            pass


if __name__ == "__main__":
    main()
