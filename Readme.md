# TIFD database and registration form

## Installing

### Quickstart

- clone the repo
- create a python venv
- activate the venv
- install the required packages
- edit my.cnf and enter the mysql database info
- load the database schema from mysql-init.sql
- python manage.py runserver
- app should be available at http://127.0.0.1:8000/


```
git clone https://github.com/jaytifd/tifddb.git
python -m venv django-venv
source django-venv/bin/activate
pip install -r requirements.txt
mysql < mysql-init.sql
python manage.py runserver

```

### Detailed install instructions

- install Django: https://docs.djangoproject.com/en/stable/intro/install/
- install the local requirements:  pip -r requirements.txt
- optional but recommended to walk through the Django tutorial: https://www.djangoproject.com/start/
- load the db schema (currently Django is not managing the database tables).
- start django `python manage.py runserver`
- Then navigate to http://127.0.0.1:8000/   (user admin password admin)

## Main Views

| url path     | app     | description |
|--------------|-----------|------------|
| /     | camp       | The default camp registration page
| /membership     | membership      | The membership registration page
| /registrar     | registrar    | Registrar / admin functions

## Database tables
https://github.com/jaytifd/tifddb/blob/master/tables.txt







