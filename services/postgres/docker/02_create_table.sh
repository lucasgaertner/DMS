#!/bin/bash
set -e

POSTGRES="psql -U postgres"
#create a documents database
echo "Creating s documents Table"
$POSTGRES <<-EOSQL
\c documents;
CREATE TABLE IF NOT EXISTS document_informations (
    filename varchar(1000) NOT NULL,
    blob bytea NOT NULL,
    extension varchar(1000) NOT NULL,	
    timestamp timestamp default NULL
);
EOSQL