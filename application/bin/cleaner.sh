#! /usr/bin/env bash

rm -rf db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./venv/*" -delete
