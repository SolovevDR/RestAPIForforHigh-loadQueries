#!/bin/bash

cd ~
postgres -c log_statement=all
number_of_files=$(ls -A "/var/lib/postgresql/data/" | wc -l)
if [ "$number_of_files" == "0" ]; then
  initdb -D /var/lib/postgresql/data/
fi
pg_ctl -D /var/lib/postgresql/data/ -l ./db_log start

sleep 5
psql -U postgres -d postgres -c "CREATE ROLE ${DB_USER} WITH LOGIN PASSWORD '${DB_PASS}';" || exit 1
createdb -O ${DB_USER} ${DB_NAME} || exit 1

cp /database/pg_hba.conf /var/lib/postgresql/data/
alembic upgrade head
