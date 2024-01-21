# TIFD database and registration form

## Database details

TIFD's main event is a once a year folk dance camp.  This is the code for the online registration form.  The form supports multiple adult and child campers to register at the same time provided they live at the same address. Each camper, when registering for camp, automatically pays a required $15 membership fee to become a member of the group.  TIFD also offers people not attending camp to sign up for a membership and donate to the group throgh separate registration form. The camp registration form has many options and things to pay for such as t-shirt, upgraded housing, etc.  It also collects a bunch of information such as dietary restrictions, camp band instruments played, mobility issues.  It also provides the camper the option to donate to TIFD and requires them to acknowledge a safety agreement before completing the form.  Payments can be accepted via PayPal or by mailing a check.  PayPal registrations are handled automatically via PayPal's IPN.  Check registrations are handled as automatically as possible - generally just entering the check number.

The app has a backend reporting function that provides details of camp registrations, lets the registrar manage registrations and process payments.

There are hree main tables in the database:
- **camp_camper**: Essentially a "person".  Can be adult or child.  People who sign up for camp or membership are all essentially "campers" in the database.  They are also **ephemeral** meaning that every year their info is re-entered - there is no link from one year to the next. The membership report searches for campers where now() is between membership_valid_from and membership_valid_to and tries to filter out duplicates.  
- **camp_registration**: A container that holds multiple campers.  In the past this was called mebership_unit - aka one or more people living at the same address.  Linked this way because the TIFD newsletter used to be a physical mailer. It has the campers' address, shopping cart total, donations and a foreign key to membership_payments.
- **membership_payments**: An itemized accounting of the things a member paid for and a link to either a check # or a paypal_ipn entry. Categories such as housing_fee, registration_fee, membership_fee are all broken out.  Info taken fomm camp_amper (registration type, housing option) and from camp_registration (donations, paypal_fee) are saved here.

## Database table schema
https://github.com/jaytifd/tifddb/blob/master/tables.txt

## Prerequisites 

- python
- MySQL


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







