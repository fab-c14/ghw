# Vector search on the hack week notes

Tiger Cloud service `ghw-hackweek` (`p182nhjnby`). `setup.sql` enables pgvector and pgvectorscale, then creates `hackweek_notes` with a 768-dimension `embedding` column and a timestamp.

`embed.py` embeds four notes with the local `nomic-embed-text` model and inserts them. The notes describe the office sensor, the IoT sensors, the hourly temperature rollup, and the crypto trades. A StreamingDiskANN index, `hackweek_notes_embedding_idx`, uses cosine distance.

`search.py` embeds the question “how warm was the office temperature sensor” and orders notes by cosine distance. The closest note is the office sensor at 0.2285. The crypto note is the farthest at 0.5602. The same search with `time >= 2026-10-11 16:00:00+00` drops the 14:35 office note and returns the IoT sensors first.

Console: https://console.cloud.tigerdata.com/dashboard/services/p182nhjnby

The database password stays in the system keyring and is not in this folder.
