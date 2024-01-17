# TIFD database and registration form

## Installing

### Quickstart - using the venv and database stub from this repo 
I am not sure if this will work on non-linux systems

```
source django-venv/bin/activate
python manage.py runserver
```
Then navigate to http://127.0.0.1:8000/ (user admin password admin)

### Detailed install instructions

- install Django: https://docs.djangoproject.com/en/stable/intro/install/
- install the local requirements:  pip -r requirements.txt
- optional but recommended to walk through the Django tutorial: https://www.djangoproject.com/start/
- run the database init script sql-init.sh
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







