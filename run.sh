#!/bin/bash

SQL_FILE=sample.sql
PY_FILE=sample.py

echo $SQL_FILE
PGPASSWORD=password psql -d mydatabase -U root -h 0.0.0.0 -p 5432 -E -w -f $SQL_FILE
echo

echo $PY_FILE
python $PY_FILE
