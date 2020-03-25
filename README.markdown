# My Website!
## Dependencies
* For debian based systems
### install the following for weasyprint
sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
### Done!
## Gunicorn Command
```
gunicorn -c gunicorn_conf.py -w 5 -k gevent --worker-connections 1000 wvr.wsgi
```
## Daphne Command
```
daphne -b 127.0.0.1 -p 8000 wvr.asgi:application
```
## Roadmap
* Add expiration and admin features to F1L3

# Bugs
* csrf middleware
