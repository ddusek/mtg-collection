#!/usr/bin/env bash

echo "Export Flask environment"
export FLASK_ENV=development

echo "Export Flask app"
export FLASK_APP=api/cards_api.py

echo "Run Flask"
flask run --debugger --host=0.0.0.0
