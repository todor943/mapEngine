#/bin/bash
# gunicorn --threads 10 -b 0.0.0.0:80 -b 0.0.0.0:443 MapEngine.wsgi
# gunicorn --certfile=certs/selfsigned.crt --keyfile=certs/selfsigned.key --threads 10 -b 0.0.0.0:80 MapEngine.wsgi
gunicorn --certfile=certs/selfsigned.crt --keyfile=certs/selfsigned.key --threads 10 -b 0.0.0.0:80 MapEngine.wsgi
