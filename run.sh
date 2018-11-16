#!/bin/bash

GUNICORN_CMD_ARGS="--bind=0.0.0.0:9210 --timeout 60 --workers=1 --log-level=info" gunicorn main:api
