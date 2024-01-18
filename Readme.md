# TIFD database and registration form

## Prerequisites 

- python
- MySQL

## Installing

### Quickstart

- Clone the repo: `https://github.com/jaytifd/tifddb.git`
- `cd tifddb`
- Create a python venv:  `python -m venv django-venv`
- Activate the venv: `source django-venv/bin/activate` or `django-venv\Scripts\activate`
- Install the required packages from requirements.txt:    `pip install -r requirements.txt`
- Edit my.cnf and enter the mysql database name, username, and password.
- Create an admin user: python manage.py createsuperuser
- python manage.py migrate
- Load the database schema from mysql-init.sql:  `mysql --defaults-file=my.cnf DATABASENAME < mysql-init.sql` 
- python manage.py runserver
- App should be available at http://127.0.0.1:8000/

### Linux install example
```
git clone https://github.com/jaytifd/tifddb.git
cd tifddb
python -m venv django-venv
source django-venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --noinput --username admin --email admin@localhost
mysql --defaults-file=my.cnf < mysql-init.sql
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







