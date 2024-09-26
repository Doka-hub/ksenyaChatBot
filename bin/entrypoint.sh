#!/usr/bin/env bash

set -e;

APP_HOST=${APP_HOST:-"0.0.0.0"}
APP_PORT=${APP_PORT:-"8000"}

# if ! [ -z "$APP_MIGRATE" ]; then
  python migrations.py migrate
# fi

#if ! [ -z "$APP_CELERY" ]; then
#  rm -f /tmp/celeryd.pid || true
#  celery $APP_CELERY
#  exit
#fi

gunicorn bot:app --bind ${APP_HOST}:${APP_PORT} --access-logfile - --worker-class aiohttp.GunicornWebWorker
