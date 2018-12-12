#!/bin/sh

/usr/local/bin/gunicorn --reload --access-logfile - -b 0.0.0.0:8000 "api:create_app()"