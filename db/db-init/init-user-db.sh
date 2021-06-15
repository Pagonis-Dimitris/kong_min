#!/bin/bash
set -e

echo "Creating db ..."

function create_kong_user_and_database() {
	local database=kong
	local owner=kong
	echo "  Creating user and database '$database'"
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	    CREATE USER $owner;
	    CREATE DATABASE $database;
      ALTER USER $owner WITH PASSWORD 'kong';
	    GRANT ALL PRIVILEGES ON DATABASE $database TO $owner;
EOSQL
}

if psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -c 'SELECT datname FROM pg_catalog.pg_database' | grep 'database'; then
  echo "DB is already created"
else
  create_kong_user_and_database
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE realestate;
    GRANT ALL PRIVILEGES ON DATABASE realestate TO postgres;
    CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
    ALTER DATABASE realestate SET datestyle TO "ISO, DMY";
EOSQL
  echo "DB is now created!"
fi