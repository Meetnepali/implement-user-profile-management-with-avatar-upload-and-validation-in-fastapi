#!/bin/bash
set -eux
bash install.sh
source venv/bin/activate
exec uvicorn main:app --host 0.0.0.0 --port 8000
