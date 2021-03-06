#!/usr/bin/env bash

echo -e "Running webserver"

uvicorn mtg_collection.api.app:app --host 0.0.0.0 --port 8000 --reload --ssl-keyfile localhost+2-key.pem --ssl-certfile localhost+2.pem