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
- Create an admin user: `python manage.py createsuperuser`
- Perform the django migrations `python manage.py migrate`
- Load the database schema from mysql-init.sql:  `mysql --defaults-file=my.cnf DATABASENAME < mysql-init.sql` 
- start the internal webserver: `python manage.py runserver`
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

### Other Docs

- Django install docs: https://docs.djangoproject.com/en/stable/intro/install/
- Awesome Django tutorial: https://www.djangoproject.com/start/

## App docs

### Main Views

| url path     | app     | description |
|--------------|-----------|------------|
| /     | camp       | The default camp registration page
| /membership     | membership      | The membership registration page
| /registrar     | registrar    | Registrar / admin functions

## Database tables
https://github.com/jaytifd/tifddb/blob/master/tables.txt

## Database details

TIFD's main event is a once a year folk dance camp.  Each camper, when registring for camp, automatically pays a required $15 membership fee to become a member of the group.  TIFD also offers people not attending camp to sign up for a membership and donate to the group.

There main tables in the database are set up to process camp registrations and membership registrations.

- camp_camper: Essentially a "person".  People who sign up for camp or membership are all "campers". 
- camp_registration
- membership_payments





