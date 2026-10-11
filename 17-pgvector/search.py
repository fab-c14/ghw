"""Run a cosine search for the office-sensor note, including a time filter."""

import json
import os
import subprocess
import tempfile
import urllib.request
from pathlib import Path

TIGER = r"C:\Users\plesi\AppData\Local\Programs\TigerCLI\tiger.exe"
SERVICE = "p182nhjnby"
QUERY = "how warm was the office temperature sensor"


def embed(text):
    body = json.dumps({"model": "nomic-embed-text", "input": "search_query: " + text}).encode()
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/embed",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = json.load(response)
    return payload["embeddings"][0]


def run(sql):
    fd, name = tempfile.mkstemp(suffix=".sql")
    os.close(fd)
    path = Path(name)
    path.write_text(sql, encoding="utf-8")
    try:
        result = subprocess.run(
            [TIGER, "db", "query", SERVICE, "-f", str(path), "-o", "json"],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
    return result.stdout


def main():
    literal = "[" + ",".join(f"{number:.8f}" for number in embed(QUERY)) + "]"
    nearest = f"""
SELECT topic, time, round((embedding <=> '{literal}'::vector)::numeric, 4) AS distance
FROM hackweek_notes
ORDER BY embedding <=> '{literal}'::vector
LIMIT 4;
"""
    filtered = f"""
SELECT topic, time, round((embedding <=> '{literal}'::vector)::numeric, 4) AS distance
FROM hackweek_notes
WHERE time >= '2026-10-11 16:00:00+00'
ORDER BY embedding <=> '{literal}'::vector
LIMIT 3;
"""
    out = Path(tempfile.gettempdir()) / "ghw-vector-proof.json"
    payload = {"nearest": json.loads(run(nearest)), "since_16": json.loads(run(filtered))}
    out.write_text(json.dumps(payload), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
