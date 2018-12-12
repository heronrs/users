#!/bin/sh

/usr/local/bin/gunicorn --reload -b 0.0.0.0:8000 "api:create_app()"