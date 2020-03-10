#!/bin/sh
set -e
FLASK_APP=blog.app flask db upgrade
make compile
PORT=${PORT:-5000}
exec gunicorn -b :${PORT} --access-logfile - --error-logfile - -w 4 "blog.app:create_app()"