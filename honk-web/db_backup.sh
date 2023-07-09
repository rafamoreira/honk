#/bin/bash

filename=$(date +%s)

docker exec -t honk bash -c "sqlite3 /app/sqlite_data/db.sqlite3 '.backup /sqlite_backups/$filename.sqlite3'"
