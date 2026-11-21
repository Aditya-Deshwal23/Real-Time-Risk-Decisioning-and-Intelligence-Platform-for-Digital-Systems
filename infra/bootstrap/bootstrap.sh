#!/bin/sh
set -eu

export PGPASSWORD="$POSTGRES_PASSWORD"

psql \
  --host 127.0.0.1 \
  --set ON_ERROR_STOP=1 \
  --set VERDICT_OWNER_PASSWORD="$VERDICT_OWNER_PASSWORD" \
  --set VERDICT_APP_PASSWORD="$VERDICT_APP_PASSWORD" \
  --set VERDICT_WORKER_PASSWORD="$VERDICT_WORKER_PASSWORD" \
  --set KEYCLOAK_PASSWORD="$KEYCLOAK_PASSWORD" \
  --username "$POSTGRES_USER" \
  --dbname postgres \
  --file /bootstrap/bootstrap.sql

psql \
  --host 127.0.0.1 \
  --set ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" \
  --dbname verdict <<'SQL'
ALTER SCHEMA public OWNER TO verdict_owner;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM verdict_app;
REVOKE ALL ON SCHEMA public FROM verdict_worker;
GRANT USAGE ON SCHEMA public TO verdict_app;
GRANT USAGE ON SCHEMA public TO verdict_worker;
GRANT CONNECT ON DATABASE verdict TO verdict_app;
GRANT CONNECT ON DATABASE verdict TO verdict_worker;
ALTER DEFAULT PRIVILEGES FOR ROLE verdict_owner IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO verdict_app;
ALTER DEFAULT PRIVILEGES FOR ROLE verdict_owner IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO verdict_app;
ALTER DEFAULT PRIVILEGES FOR ROLE verdict_owner IN SCHEMA public
  GRANT SELECT ON TABLES TO verdict_worker;
SQL
