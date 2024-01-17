#!/bin/bash  -e
trap "echo ERROR: SCRIPT FAILED!" EXIT

venv="./django-venv"
. $venv/bin/activate

db="tifddb_git"

./clean.sh

DJANGO_SUPERUSER_PASSWORD=admin 

rm -rf */migrations/0*
rm -rf */migrations/__pycache__/

#Let Django create all the tables
python manage.py makemigrations
python manage.py migrate

#Import some necessary data
mysql $db < mysql-init.sql

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
" | mysql $db

echo "done!"
trap - EXIT
