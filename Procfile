web: uwsgi --master --die-on-term --module app:app --http :${PORT:-5000}
dev: FLASK_APP=app/__init__.py FLASK_DEBUG=1 flask run
