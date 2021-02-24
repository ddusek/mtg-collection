#!/usr/bin/env bash

echo -e "Running webserver"

uvicorn mtg_collection.api.app:app --host 0.0.0.0 --reload
