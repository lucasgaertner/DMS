#!/bin/bash
set -e

POSTGRES="psql -U postgres"

#create a documents database
echo "Creating s documents database"
$POSTGRES <<-EOSQL
CREATE DATABASE documents OWNER postgres;
EOSQL
