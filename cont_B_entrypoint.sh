#!/bin/bash

#start gunicorn with config
exec gunicorn --config gunicorn_conf.py application:app