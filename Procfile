web: gunicorn pugdit.wsgi
worker: celery worker -A pugdit.celery --loglevel=info --logfile=worker.log -B
