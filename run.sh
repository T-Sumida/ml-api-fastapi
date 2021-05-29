#!/bin/bash

set -eu

HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}
APP_NAME=${APP_NAME:-"app.main:app"}

uvicorn ${APP_NAME} --host ${HOST} --port ${PORT}