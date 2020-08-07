#!/bin/bash
set -e

POSTGRES="psql -U postgres"

#create a shared database
echo "Creating s shared database"
$POSTGRES <<-EOSQL
CREATE DATABASE shared OWNER shared;
EOSQL
