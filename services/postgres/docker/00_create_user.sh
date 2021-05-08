#!/bin/bash
set -e

POSTGRES="psql -U postgres"

echo "Creating database role: documents"

$POSTGRES <<-EOSQL
CREATE USER postgres WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	NOINHERIT
	NOREPLICATION
	PASSWORD '$SHARED_PASSWORD';
	
CREATE DATABASE documents OWNER postgres;
\c documents;
CREATE TABLE IF NOT EXISTS document_informations (
	id SERIAL,
    filename varchar(1000) NOT NULL,
    blob bytea NOT NULL,
    extension varchar(100),	
    timestamp date,
	content text,
);	
EOSQL
