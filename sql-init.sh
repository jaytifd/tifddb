#!/bin/bash  -e
trap "echo ERROR: SCRIPT FAILED!" EXIT

venv="./django-venv"
. $venv/bin/activate


DJANGO_SUPERUSER_PASSWORD=admin 
sqlite_prog="sqlite3"
sqlite_db="db.sqlite3"

if [ -e $sqlite_db ]; then
    echo Are you sure?  This removes the old database!
    rm -i $sqlite_db
fi
rm -rf */migrations/0*
rm -rf */migrations/__pycache__/

#Let Django create all the tables
python manage.py makemigrations
python manage.py migrate

#Import some necessary data
sqlite3 $sqlite_db < sql_init.txt

#set the Django admin account
echo
echo "creating superuser account [admin/$DJANGO_SUPERUSER_PASSWORD]"
DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD python manage.py createsuperuser --noinput --username admin --email admin@localhost

#open the form
thisyear=$(date +"%Y")
open="$thisyear-01-01"
close="$thisyear-12-31"

echo "
update camp_dates set date='$open' where id=2;
update camp_dates set date='$close' where id=4;
" | $sqlite_prog db.sqlite3 

echo "done!"
trap - EXIT
