#!/bin/bash
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
source "${SCRIPTPATH}/wait-for-postgres.sh"
source "${SCRIPTPATH}/wait-for-kong.sh"

python3 manage.py migrate
python3 manage.py collectstatic --clear --noinput
gunicorn --log-level debug -w $N_WORKERS -b 0.0.0.0:5000 core.wsgi
