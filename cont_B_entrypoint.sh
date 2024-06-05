#!/bin/bash

set -e

/wait-for-it-master/wait-for-it.sh -h pgsql -p 5432 -t 60

python Postgres_logic/insert_data.py

#start gunicorn with config
exec gunicorn --config gunicorn_conf.py application:application