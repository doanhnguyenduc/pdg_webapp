#!/bin/bash
export PYTHON_VERSION=3.9
python -m gunicorn --bind 0.0.0.0:8000 app:app