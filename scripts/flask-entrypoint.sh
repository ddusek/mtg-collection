#!/usr/bin/env bash

echo -e "Running webserver"

flask run --host=0.0.0.0
redis-server --appendonly yes