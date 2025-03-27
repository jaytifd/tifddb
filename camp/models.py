from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator

from localflavor.us.forms import USStateSelect, USZipCodeField, USStateField
from localflavor.us.us_states import STATE_CHOICES
from localflavor.ca.ca_provinces import PROVINCE_CHOICES 

from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField
from simple_history.models import HistoricalRecords
from decimal import Decimal
import datetime

virtual_camp=False
now = datetime.datetime.now()

BOOL_CHOICES = (
            (0, 'No'),
            (1, 'Yes'), 
            )

REGISTRATION_SOURCE = (
            (0, 'Camp'),
            (1, 'Membership'), 
            )

REPORT_TYPES = (
            ('camp', 'Camp'),
            ('membership', 'Membership'), 
            ('unlisted', 'unlisted'),
            )

ADULT_OR_CHILD = (
            ('adult', 'adult'),
            ('child', 'child'), 
            )

REGISTRATION_PAID_STATUS=(5,6,8,)
REGISTRATION_OPEN_STATUS=(1,2,3,4,7,9,11)

COUNTRIES=(
("AF","Afghanistan"),
("AX","Aland Islands"),
("AL","Albania"),
("DZ","Algeria"),
("AS","American Samoa"),
("AD","Andorra"),
("AO","Angola"),
("AI","Anguilla"),
("AQ","Antarctica"),
("AG","Antigua and Barbuda"),
("AR","Argentina"),
("AM","Armenia"),
("AW","Aruba"),
("AU","Australia"),
("AT","Austria"),
("AZ","Azerbaijan"),
("BS","Bahamas"),
("BH","Bahrain"),
("BD","Bangladesh"),
("BB","Barbados"),
("BY","Belarus"),
("BE","Belgium"),
("BZ","Belize"),
("BJ","Benin"),
("BM","Bermuda"),
("BT","Bhutan"),
("BO","Bolivia, Plurinational State of"),
("BQ","Bonaire, Sint Eustatius and Saba"),
("BA","Bosnia and Herzegovina"),
("BW","Botswana"),
("BV","Bouvet Island"),
("BR","Brazil"),
("IO","British Indian Ocean Territory"),
("BN","Brunei Darussalam"),
("BG","Bulgaria"),
("BF","Burkina Faso"),
("BI","Burundi"),
("KH","Cambodia"),
("CM","Cameroon"),
("CA","Canada"),
("CV","Cape Verde"),
("KY","Cayman Islands"),
("CF","Central African Republic"),
("TD","Chad"),
("CL","Chile"),
("CN","China"),
("CX","Christmas Island"),
("CC","Cocos (Keeling) Islands"),
("CO","Colombia"),
("KM","Comoros"),
("CG","Congo"),
("CD","Congo, The Democratic Republic of the"),
("CK","Cook Islands"),
("CR","Costa Rica"),
("CI","Côte d'Ivoire"),
("HR","Croatia"),
("CU","Cuba"),
("CW","Curaçao"),
("CY","Cyprus"),
("CZ","Czech Republic"),
("DK","Denmark"),
("DJ","Djibouti"),
("DM","Dominica"),
("DO","Dominican Republic"),
("EC","Ecuador"),
("EG","Egypt"),
("SV","El Salvador"),
("GQ","Equatorial Guinea"),
("ER","Eritrea"),
("EE","Estonia"),
("ET","Ethiopia"),
("FK","Falkland Islands (Malvinas)"),
("FO","Faroe Islands"),
("FJ","Fiji"),
("FI","Finland"),
("FR","France"),
("GF","French Guiana"),
("PF","French Polynesia"),
("TF","French Southern Territories"),
("GA","Gabon"),
("GM","Gambia"),
("GE","Georgia"),
("DE","Germany"),
("GH","Ghana"),
("GI","Gibraltar"),
("GR","Greece"),
("GL","Greenland"),
("GD","Grenada"),
("GP","Guadeloupe"),
("GU","Guam"),
("GT","Guatemala"),
("GG","Guernsey"),
("GN","Guinea"),
("GW","Guinea-Bissau"),
("GY","Guyana"),
("HT","Haiti"),
("HM","Heard Island and McDonald Islands"),
("VA","Holy See (Vatican City State)"),
("HN","Honduras"),
("HK","Hong Kong"),
("HU","Hungary"),
("IS","Iceland"),
("IN","India"),
("ID","Indonesia"),
("IR","Iran, Islamic Republic of"),
("IQ","Iraq"),
("IE","Ireland"),
("IM","Isle of Man"),
("IL","Israel"),
("IT","Italy"),
("JM","Jamaica"),
("JP","Japan"),
("JE","Jersey"),
("JO","Jordan"),
("KZ","Kazakhstan"),
("KE","Kenya"),
("KI","Kiribati"),
("KP","Korea, Democratic People's Republic of"),
("KR","Korea, Republic of"),
("KW","Kuwait"),
("KG","Kyrgyzstan"),
("LA","Lao People's Democratic Republic"),
("LV","Latvia"),
("LB","Lebanon"),
("LS","Lesotho"),
("LR","Liberia"),
("LY","Libya"),
("LI","Liechtenstein"),
("LT","Lithuania"),
("LU","Luxembourg"),
("MO","Macao"),
("MK","Macedonia, Republic of"),
("MG","Madagascar"),
("MW","Malawi"),
("MY","Malaysia"),
("MV","Maldives"),
("ML","Mali"),
("MT","Malta"),
("MH","Marshall Islands"),
("MQ","Martinique"),
("MR","Mauritania"),
("MU","Mauritius"),
("YT","Mayotte"),
("MX","Mexico"),
("FM","Micronesia, Federated States of"),
("MD","Moldova, Republic of"),
("MC","Monaco"),
("MN","Mongolia"),
("ME","Montenegro"),
("MS","Montserrat"),
("MA","Morocco"),
("MZ","Mozambique"),
("MM","Myanmar"),
("NA","Namibia"),
("NR","Nauru"),
("NP","Nepal"),
("NL","Netherlands"),
("NC","New Caledonia"),
("NZ","New Zealand"),
("NI","Nicaragua"),
("NE","Niger"),
("NG","Nigeria"),
("NU","Niue"),
("NF","Norfolk Island"),
("MP","Northern Mariana Islands"),
("NO","Norway"),
("OM","Oman"),
("PK","Pakistan"),
("PW","Palau"),
("PS","Palestinian Territory, Occupied"),
("PA","Panama"),
("PG","Papua New Guinea"),
("PY","Paraguay"),
("PE","Peru"),
("PH","Philippines"),
("PN","Pitcairn"),
("PL","Poland"),
("PT","Portugal"),
("PR","Puerto Rico"),
("QA","Qatar"),
("RE","Réunion"),
("RO","Romania"),
("RU","Russian Federation"),
("RW","Rwanda"),
("BL","Saint Barthélemy"),
("SH","Saint Helena, Ascension and Tristan da Cunha"),
("KN","Saint Kitts and Nevis"),
("LC","Saint Lucia"),
("MF","Saint Martin (French part)"),
("PM","Saint Pierre and Miquelon"),
("VC","Saint Vincent and the Grenadines"),
("WS","Samoa"),
("SM","San Marino"),
("ST","Sao Tome and Principe"),
("SA","Saudi Arabia"),
("SN","Senegal"),
("RS","Serbia"),
("SC","Seychelles"),
("SL","Sierra Leone"),
("SG","Singapore"),
("SX","Sint Maarten (Dutch part)"),
("SK","Slovakia"),
("SI","Slovenia"),
("SB","Solomon Islands"),
("SO","Somalia"),
("ZA","South Africa"),
("GS","South Georgia and the South Sandwich Islands"),
("ES","Spain"),
("LK","Sri Lanka"),
("SD","Sudan"),
("SR","Suriname"),
("SS","South Sudan"),
("SJ","Svalbard and Jan Mayen"),
("SZ","Swaziland"),
("SE","Sweden"),
("CH","Switzerland"),
("SY","Syrian Arab Republic"),
("TW","Taiwan, Province of China"),
("TJ","Tajikistan"),
("TZ","Tanzania, United Republic of"),
("TH","Thailand"),
("TL","Timor-Leste"),
("TG","Togo"),
("TK","Tokelau"),
("TO","Tonga"),
("TT","Trinidad and Tobago"),
("TN","Tunisia"),
("TR","Turkey"),
("TM","Turkmenistan"),
("TC","Turks and Caicos Islands"),
("TV","Tuvalu"),
("UG","Uganda"),
("UA","Ukraine"),
("AE","United Arab Emirates"),
("GB","United Kingdom"),
("US","United States"),
("UM","United States Minor Outlying Islands"),
("UY","Uruguay"),
("UZ","Uzbekistan"),
("VU","Vanuatu"),
("VE","Venezuela, Bolivarian Republic of"),
("VN","Viet Nam"),
("VG","Virgin Islands, British"),
("VI","Virgin Islands, U.S."),
("WF","Wallis and Futuna"),
("YE","Yemen"),
("ZM","Zambia"),
("ZW","Zimbabwe"),
)


#MariaDB [tifddb1]> select * from camp_registration_status;
#+----+----------------------------+-----------------------------------------------------------------------------------------+---------------+
#| id | status                     | description                                                                             | display_order |
#+----+----------------------------+-----------------------------------------------------------------------------------------+---------------+
#|  1 | Incomplete                 | User has saved the first page, not the second (no agree checkbox)                       |            10 |
#|  2 | NotPaid                    | User has saved the 2nd page (confirmed alcohol policy), not selected a payment type yet |            20 |
#|  3 | Waiting for PayPal payment | User pushed the PayPal button and we have not yet confirmed their paypal payment        |            30 |
#|  4 | Waiting for check payment  | User pressed the check payment button and we have not yet approved their payment        |            40 |
#|  5 | Registrar Approved         | Registrar confirmed payment                                                             |           100 |
#|  6 | Paypal IPN confirmed       | We received a successful IPN response from PayPal                                       |            60 |
#|  7 | Paypal IPN error           | Error code when something went wrong with paypal IPN (set in camp/signals.py)           |          NULL |
#|  8 | PAID via registrar         | Registrar has processed payment and the registration is paid in full                    |            50 |
#|  9 | Imported from old DB       |                                                                                         |          NULL |
#| 10 | Invalid                    | A generic status to put registrations that would otherwise be deleted                   |             5 |
#| 11 | Refunded                   | A refund was issued from paypal                                                         |             4 |
#+----+----------------------------+-----------------------------------------------------------------------------------------+---------------+



PAYMENT_TYPES = (
    (1, "Check"),
    (2, "Cash"),
    (3, "PayPal"),
    #(10, "Refund"),
  )

class MembershipType(models.Model):
    membertype = models.CharField("Membership Type",db_column='membertype', max_length=100, blank=False, null=False)  # Field name made lowercase.
    display_order = models.IntegerField()
    def __str__(self):
        return str(self.membertype)
    class Meta:
        verbose_name_plural = u'__constants: Member Types'
        db_table = 'membership_type'
        ordering = ['display_order']


class CampRegistrationStatus(models.Model):
    status = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-display_order']
        managed = False
        db_table = 'camp_registration_status'
        verbose_name = "Registration statuses"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.status

class MembershipRegistrationTypes(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False)
    price=models.DecimalField(max_digits=7, decimal_places=2, blank=False,null=False)
    slug = models.CharField(max_length=255, blank=False, null=False)
    display_order = models.IntegerField(blank=False, null=False)
    cart_description = models.CharField(max_length=255, blank=False, null=False)
    adult_or_child = models.CharField(max_length=255,blank=False, null=False)
    active = models.BooleanField("Include on regform?",max_length=1, default=1, blank=False, null=False )
    class Meta:
        ordering = ['-display_order']
        managed = False
        db_table = 'membership_registration_types'
    def __str__(self):
        return self.description

class CampRegistrationTypes(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False)
    price=models.DecimalField(max_digits=7, decimal_places=2, blank=False,null=False)
    slug = models.CharField("slug - either \"registration\" or \"membership\"",max_length=255, blank=False, null=False)
    display_order = models.IntegerField(blank=False, null=False)
    cart_description = models.CharField(max_length=255, blank=False, null=False)
    adult_or_child = models.CharField(max_length=255,blank=False, null=False)
    active = models.BooleanField("Include on regform?",max_length=1, default=1, blank=False, null=False )
    history = HistoricalRecords()

    def __str__(self):
        #more cusom stuff for the virtual camp
        if self.id==113:
            return str(self.description )
        else:
            return str("$" + str(self.price) + " " + self.description)
        
    class Meta:
        managed = False
        ordering = ['-slug','-display_order','-active']
        db_table = 'camp_registration_types'
        verbose_name = "registration types"
        verbose_name_plural=verbose_name

class CampRebates(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False)
    price=models.DecimalField(max_digits=7, decimal_places=2, blank=False,null=False)
    slug = models.CharField(max_length=255, blank=False, null=False)
    display_order = models.IntegerField(blank=False, null=False)
    cart_description = models.CharField(max_length=255, blank=False, null=False)
    def __str__(self):
        return str("$" + str(self.price) + " " + str(self.description))
    class Meta:
        managed = False
        ordering = ['display_order']
        db_table = 'camp_rebates'
        verbose_name = "Membership rebates"
        verbose_name_plural=verbose_name

class CampRegistration(models.Model):
    YOUR_STATE_CHOICES = list(STATE_CHOICES) + list(PROVINCE_CHOICES)
    #YOUR_STATE_CHOICES.sort()
    YOUR_STATE_CHOICES.insert(0, (' ', 'None'))
    YOUR_STATE_CHOICES.insert(0, (' ', '-----'))
    YOUR_STATE_CHOICES.append((' ', '------'))

    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address1 = models.CharField('Mailing address - street', max_length=255, blank=False, null=True)
    address2 = models.CharField('Mailing address - apt/unit', max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=False, null=True)
    state = models.CharField(max_length=255, blank=False, null=True, default="", choices=YOUR_STATE_CHOICES)
    zip = models.CharField(max_length=255, blank=False, null=True)
    country = models.CharField('Country',max_length=255, blank=True, null=True, choices = COUNTRIES, default="US")
    donation_bobbi_gillotti = models.DecimalField("Bobbi Gillotti fund donation", validators=[MinValueValidator(Decimal('0.00'))], max_digits=7, decimal_places=2, blank=True, null=True, default='')
    donation_floor_fund = models.DecimalField("Floor fund donation", max_digits=7, validators=[MinValueValidator(Decimal('0.00'))], decimal_places=2, blank=True, null=True, default='')
    donation_camp_fund = models.DecimalField("Floor fund donation", max_digits=7, validators=[MinValueValidator(Decimal('0.00'))], decimal_places=2, blank=True, null=True, default='')
    donation_live_music = models.DecimalField("Live music donation", max_digits=7, validators=[MinValueValidator(Decimal('0.00'))], decimal_places=2, blank=True, null=True, default='')
    donation_tifd = models.DecimalField("TIFD fund donation", max_digits=7, validators=[MinValueValidator(Decimal('0.00'))], decimal_places=2, blank=True, null=True, default='')
    donation_chuck = models.DecimalField("Donation in remembrance of Chuck Roth", max_digits=7, validators=[MinValueValidator(Decimal('0.00'))], decimal_places=2, blank=True, null=True, default='')
    payment = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    camper_note = models.TextField(blank=True, null=True)
    adjustment_note = models.TextField(blank=True, null=True)
    email_confirmation_sent = models.BooleanField("Email conf sent?",max_length=1, blank=True, null=True, default=0)
    auction_items = models.TextField(blank=True, null=True)
    session = models.TextField(blank=True, null=True)
    payment_type = models.CharField(max_length=255, blank=True, null=True)
    cart_total=models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=False, default=0)
    membership_fee_gross=models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=True)
    late_fee=models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=True)
    adjustment=models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=True)
    paypal_fee=models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=True)
    shipping_fee=models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=True)
    paypal_gross=models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=True)
    agreecheckbox = models.BooleanField("Safety policy checkbox",max_length=255, blank=False, null=False)
    registrar_approval_note = models.TextField("Registrar confirmation email",blank=True, null=True)
    rebate= models.ForeignKey(CampRebates, on_delete=models.DO_NOTHING, related_name="rebate_from_registration", blank=True, null=True)
    registration_status= models.ForeignKey(CampRegistrationStatus, on_delete=models.DO_NOTHING, blank=True, null=True, default=1)
    year = models.IntegerField(blank=False, null=True, default=datetime.datetime.now().year)
    postmark = models.DateField(blank=True, null=True)
    registration_source = models.IntegerField(blank=False, null=False, default=0, choices=REGISTRATION_SOURCE) ## 0=camp, 1=membership
    history = HistoricalRecords()
    campers=CampRegistrationStatus.objects.raw('SELECT * FROM camp_camper')

    persons={}
    try:
        for x in campers:
            if x.registration_id in persons.keys():
                persons[x.registration_id]+= ", " + str(x.first_name) + " " + str(x.last_name)
            else:
                persons[x.registration_id]=str(x.first_name) + " " + str(x.last_name)
    except:
        pass

    class Meta:
        managed = False
        db_table = 'camp_registration'
        verbose_name=" Camp Registrations - All years"
        verbose_name_plural=verbose_name
        ordering = ['-id']

    def __str__(self):
        if self.address1 is None:
            self.stret = ""
        if self.city is None:
            self.city = ""
        if self.state is None:
            self.state = ""

        try:
            personstring=str(self.persons[self.id])
        except:
            personstring=".."

        return str( str(self.pk) +  " " + str(personstring) + " @" + str(self.address1) )

class MembershipAddress(models.Model):
    #this contains legacy membership address info migrated from the old database
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    address1 = models.CharField(max_length=255, blank=False, null=False)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=False, null=False)
    state = models.CharField(max_length=255, blank=False, null=False)
    registration=models.ForeignKey(CampRegistration, on_delete=models.DO_NOTHING, blank=False, null=False)
    zip = models.CharField(max_length=255, blank=False, null=False)
    country = models.CharField(max_length=255, blank=True, null=True)
    newsletter_hardcopy = models.BooleanField(blank=False, null=False)
    notes = models.TextField(blank=True, null=True)
    all_persons=MembershipType.objects.raw('SELECT * FROM membership_person')
    persons={}
    try:
        for x in all_persons:
            if x.membership_address_id in persons.keys():
                persons[x.membership_address_id]+= ", " + str(x.first_name) + " " + str(x.last_name)
            else:
                persons[x.membership_address_id]=str(x.first_name) + " " + str(x.last_name)
    except:
        pass

    class Meta:
        managed = False
        db_table = 'membership_address'

    def __str__(self):
        try:
            namestring=self.persons[self.id]
        except:
            namestring="NoPerson"

        return str(namestring) + "  |  " + str(self.address1) + " "  + str(self.city) + " " + str(self.state)

class MembershipPerson(models.Model):
    #this contains legacy membership address info migrated from the old database
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    member_year = models.IntegerField(blank=False, null=True)
    membership_address= models.ForeignKey(MembershipAddress, on_delete=models.DO_NOTHING, blank=False, null=False)
    membership_type= models.ForeignKey(MembershipType, on_delete=models.DO_NOTHING, blank=False, null=False)  ### this is the legacy field
    email = models.CharField("email address", max_length=255, blank=True, null=True)
    email2 = models.CharField(max_length=255, blank=True, null=True)
    #phone = models.CharField("Phone Number",validators=[MinLengthValidator(limit_value=10,message="Phone number should have at least 10 numbers.  Missing area code?")],max_length=30, blank=True, null=True)
    phone = PhoneNumberField(blank=False, null=False)
    #these are legacy
    work_phone = models.CharField(max_length=255, blank=True, null=True)
    cell_phone = models.CharField(max_length=255, blank=True, null=True)
    home_phone = models.CharField(max_length=255, blank=True, null=True)
    membership_valid_from = models.DateField(blank=True, null=True)
    membership_valid_to = models.DateField(blank=True, null=True)
    member_since = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    dancegroups = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    flags = models.CharField(max_length=255, blank=True, null=True)
    email_newsletter = models.IntegerField(blank=True, null=True)
    legacy_pubemail1 = models.IntegerField(blank=True, null=True)
    legacy_pubemail2 = models.IntegerField(blank=True, null=True)
    legacy_agecategory = models.CharField(max_length=255, blank=True, null=True)
    last_camp = models.IntegerField(blank=True, null=True)
    legacy_dob = models.DateField(blank=True, null=True)
    registration=models.ForeignKey(CampRegistration, on_delete=models.DO_NOTHING, blank=True, null=True)
    registration_type=models.ForeignKey(MembershipRegistrationTypes, on_delete=models.DO_NOTHING, default=1)
    membership_years = models.IntegerField(blank=True, null=True, default=1)

    class Meta:
        managed = False
        db_table = 'membership_person'
        #ordering = ['last_name']
    def __str__(self):
        return str(self.first_name) + " "  + str(self.last_name)



class CampHousingTypes(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False)
    price=models.DecimalField(max_digits=7, decimal_places=2, blank=False,null=False)
    slug = models.CharField(max_length=255, blank=False, null=False)
    display_order = models.IntegerField(blank=False, null=False)
    cart_description = models.CharField(max_length=255, blank=False, null=False)
    short_description = models.CharField(max_length=20, blank=False, null=False)
    active = models.BooleanField("Include on regform?",max_length=1, default=1, blank=False, null=False )
    history = HistoricalRecords()
    def __str__(self):
        return str("$" + str(self.price) + " " + self.description )
    class Meta:
        managed = False
        ordering = ['display_order']
        verbose_name = "housing choices"
        db_table = 'camp_housing_types'
        verbose_name_plural=verbose_name

class CampShirtTypes(models.Model):
    cut = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    cart_description = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    price=models.DecimalField(max_digits=7, decimal_places=2, blank=False,null=False)
    def __str__(self):
        return str("$" + str(self.price) + " " + self.description )

    class Meta:
        managed = False
        ordering = ['display_order']
        verbose_name = "Shirt options"
        verbose_name_plural=verbose_name
        db_table = 'camp_shirt_types'

class CampDates(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        managed = False
        db_table = 'camp_dates'
        verbose_name = "camp dates"
        verbose_name_plural=verbose_name
    def __str__(self):
        return str(self.description)

class CampRegistrarInfo(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    mailing_address = models.TextField(blank=True, null=True)
    active = models.BooleanField("Include on regform?",max_length=1, default=1, blank=False, null=False )
    active = models.BooleanField("Include on regform?",max_length=1, default=1, blank=False, null=False )
    registration_source = models.IntegerField(blank=False, null=False, default=0, choices=REGISTRATION_SOURCE) ## 0=camp, 1=membership

    class Meta:
        managed = False
        db_table = 'camp_registrar_info'
        verbose_name = "Camp Registrar Address"
        verbose_name_plural=verbose_name
    def __str__(self):
        return str(self.description) + " " + str(self.name)


class CampPrices(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False)
    price=models.DecimalField(max_digits=7, decimal_places=2, blank=False,null=False)
    slug = models.CharField(max_length=255, blank=False, null=False)
    display_order = models.IntegerField(blank=False, null=False)
    cart_description = models.CharField(max_length=255, blank=False, null=False)
    def __str__(self):
        return str(self.description)
    class Meta:
        managed = False
        ordering = ['-display_order']
        verbose_name="prices"
        db_table = 'camp_prices'
        verbose_name_plural=verbose_name

class Person(models.Model):
    #### PERSON "MASTER" MODEL
    #### This defines the defaults for everything person related as long as abstract=True then the model definitions can be redefined later on
    ####
    #### CampCamper_child and CampCamper_adult are derived from this model and only change the default registration type and the adult_or_child field.
    ####
    #### This model can't be queried, it's basically just a template.

    #### IF YOU CHANGE DEFAULTS HERE, make sure that adding and deleting a second camper still works

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    registration = models.ForeignKey(CampRegistration,on_delete=models.DO_NOTHING,)
    registration_type= models.ForeignKey(CampRegistrationTypes, on_delete=models.DO_NOTHING, related_name="registration_type_from_camper", default=1)
    adult_or_child = models.CharField(max_length=255, blank=False, null=False,default="adult",choices=ADULT_OR_CHILD)
    first_name = models.CharField(max_length=255, blank=False, null=True)
    last_name = models.CharField(max_length=255, blank=False, null=True)
    membership_valid_from = models.DateField(blank=True, null=True)
    membership_valid_to = models.DateField(blank=True, null=True)
    #phone = models.CharField("Phone number",validators=[MinLengthValidator(limit_value=10,message="Phone number should have at least 10 numbers.  Missing area code?")],max_length=255, blank=False, null=False)
    phone = PhoneNumberField(blank=False, null=False)
    email = models.EmailField("Email address",max_length=255, blank=False, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    mobility = models.BooleanField('I use a mobility device such as wheelchair, walker, crutches, or cane.', blank=True, null=False, default=False,  )
    mobility_details = models.CharField("Mobility device details",max_length=255, blank=True, null=True)
    certification = models.BooleanField("I am certified in CPR, first aid, or AED, and am willing to be called on for first response in an emergency at camp.", blank=True, null=False, default=False, )
    certification_details = models.CharField("Certification details", max_length=255,blank=True, null=True)
    family_program = models.BooleanField('Participating in family program?',  blank=True, null=False, default=False )
    medical = models.BooleanField("I or my child(ren) have allergies, medical conditions, or medications the camp safety team should be aware of.",blank=True, null=False, default=False, )
    medical_details = models.CharField("Medical notes",max_length=255, blank=True, null=True)
    band = models.BooleanField("I will play in the camp band.",                         blank=True, null=False, default=False)
    instruments = models.CharField(max_length=255, blank=True, null=True)
    diet = models.BooleanField("Dietary restrictions",      blank=True, null=False, default=False)
    diet_details = models.TextField("Dietary restrictions",blank=True, null=True)
    publish = models.BooleanField("I consent to having my name, email address, and phone number published in TIFD\'s membership and Texas Camp rosters (we do not publish physical addresses for security reasons).",        blank=True, null=False, default=False)
    staff = models.BooleanField("I am a member of TIFD's administrative staff (camp committee volunteer).",        blank=True, null=False, default=False)
    need_linen = models.BooleanField("Check here to rent linens (sheets/towels) provided by GFC",  blank=True, null=False, default=False)
    staff_position = models.CharField("Staff position(s)",max_length=255, blank=True, null=True)
    free_t_shirt = models.BooleanField("Free t-shirt for staff members",        blank=True, null=False, default=False)
    dvd = models.BooleanField("I wish to order a dance review video, in which this year's teachers demonstrate the dances they taught. Digital access - TIFD will send a link after camp", blank=True, null=False, default=False)
    share_housing = models.CharField("I prefer to share housing with",max_length=255, blank=True, null=True)
    housing_assigned = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField("Age at camp", blank=True, null=True)
    housing_type= models.ForeignKey(CampHousingTypes, on_delete=models.DO_NOTHING, blank=True, null=True)
    t_shirt_type= models.ForeignKey(CampShirtTypes, on_delete=models.DO_NOTHING, verbose_name="I wish to order a commemorative camp t-shirt.", null=True, blank=True, default=1)
    membership_years = models.IntegerField(blank=False, null=False, default=1,)
    join_tifd = models.BooleanField("I would like to become a TIFD member or renew my membership ($15 for one year)", blank=False, null=False, default=True, )
    custom_registration_price=models.DecimalField("Donation amount", max_digits=7, decimal_places=2, blank=True,null=True,default=None )
    custom_registration_discount=models.DecimalField("Discount amount", max_digits=7, decimal_places=2, blank=True,null=True,default=None )
    history = HistoricalRecords()

    def __str__(self):
        if self.first_name is None:
            self.first_name = ""
        if self.last_name is None:
            self.last_name = ""
        return str( self.first_name + " " + self.last_name + " " + str(self.created_at.year))

    class Meta:
        db_table = 'camp_camper'
        managed = False
        abstract = True

class CampCamper(Person):
    #this is a query-able class that contains all the fields from the Person model.
    #membership_person= models.ForeignKey(MembershipPerson, on_delete=models.DO_NOTHING, related_name="membership_person_from_camper")
    history = HistoricalRecords()

    def __str__(self):
        if self.first_name is None:
            self.first_name = ""
        if self.last_name is None:
            self.last_name = ""
        return str( self.first_name + " " + self.last_name )
    #return str( self.first_name + " " + self.last_name + " " + str(self.created_at.year))

    class Meta:
        managed = False
        db_table = 'camp_camper'
        ordering = ['-id'] #this ordering will affect how the form is rendered on the reg form
        verbose_name = "Adult camper"

class CampCamper_adult(Person):
    registration = models.ForeignKey(CampRegistration,on_delete=models.DO_NOTHING, related_name="registration_from_adult")
    registration_type= models.ForeignKey(CampRegistrationTypes, on_delete=models.DO_NOTHING, related_name="registration_type_from_adult", default=1)  ### if you change the default, fix the camp/templates/camp/delete.html too

    if virtual_camp:
        housing_type= models.ForeignKey(CampHousingTypes, on_delete=models.DO_NOTHING, related_name="housing_type_from_adult",null=True,blank=True)
    else:
        housing_type= models.ForeignKey(CampHousingTypes, on_delete=models.DO_NOTHING, related_name="housing_type_from_adult",null=False,blank=False)

    adult_or_child = models.CharField(max_length=255, blank=False, null=False,default="adult",choices=ADULT_OR_CHILD)
    history = HistoricalRecords()

    def __str__(self):
        if self.first_name is None:
            self.first_name = ""
        if self.last_name is None:
            self.last_name = ""
        return str( self.first_name + " " + self.last_name )
        #return str( self.first_name + " " + self.last_name + " " + str(self.created_at.year))

    class Meta:
        managed = False
        db_table = 'camp_camper'
        ordering = ['id']  #this ordering will affect how the form is rendered on the reg form
        verbose_name = "Adult camper"


class CampCamper_child(Person):
    adult_or_child = models.CharField(max_length=255, blank=False, null=False,default="child",choices=ADULT_OR_CHILD)
    registration=models.ForeignKey(CampRegistration, on_delete=models.DO_NOTHING, related_name="registration_from_child")
    registration_type= models.ForeignKey(CampRegistrationTypes, on_delete=models.DO_NOTHING, related_name="registration_type_from_child", default=11)
    history = HistoricalRecords()

    def __str__(self):
        if self.first_name is None:
            self.first_name = ""
        if self.last_name is None:
            self.last_name = ""
        #return str( self.first_name + " " + self.last_name )
        return str( self.first_name + " " + self.last_name + " " + str(self.created_at.year))

    class Meta:
        managed = False
        db_table = 'camp_camper'
        ordering = ['id'] #this ordering will affect how the form is rendered on the reg form
        verbose_name = " Child camper"
class MembershipPayments(models.Model):
    #registration_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gross_amt = models.DecimalField("Gross",max_digits=10, decimal_places=2, blank=False, null=True)
    net_amt = models.DecimalField("Net",max_digits=10, decimal_places=2, blank=False, null=True)
    refund_amt = models.DecimalField("Refund",max_digits=10, decimal_places=2, blank=True, null=True)
    date_recd = models.DateField("Date received",blank=False,null=False,default=datetime.datetime.now().strftime('%Y-%m-%d'))
    who_has_possession = models.CharField("Who has possession",max_length=255, blank=False, null=False)
    payment_type = models.IntegerField("Type",choices=PAYMENT_TYPES, default=1)
    waiting_for_deposit = models.BooleanField("Waiting for deposit", null=False, blank=False, default=1)  # Field name made lowercase.
    cash = models.BooleanField(blank=True, null=True)  # Field name made lowercase.
    check_num = models.CharField("Check #",blank=True, null=True, max_length=25)
    deposit_date = models.DateField(blank=True, null=True)
    pp_ipn_name = models.CharField(max_length=255, blank=True, null=True)
    pp_ipn_email = models.CharField(max_length=255, blank=True, null=True)
    pp_ipn_phone = models.CharField(max_length=255, blank=True, null=True)
    pp_ipn_txn_id = models.CharField(max_length=255, blank=True, null=True)
    pp_ipn_id = models.IntegerField(blank=True, null=True)
    membership_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    years_paid = models.IntegerField(blank=True, null=True)
    paypal_fee = models.DecimalField("PayPal fee",max_digits=10, decimal_places=2, blank=True, null=True)
    camp_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    t_shirt_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dvd_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gfc_linens = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    registration= models.ForeignKey(CampRegistration, on_delete=models.DO_NOTHING, blank=True, null=True)
    membership_person= models.ForeignKey(MembershipPerson, on_delete=models.DO_NOTHING, blank=True, null=True)
    housing_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    other_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bobbi_fund = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    floor_fund = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    music_fund = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    general_fund = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    camp_fund = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    chuck_fund = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    texakolo_fund = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField("Payment Note",blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        managed = False
        db_table = 'membership_payments'
        verbose_name = u'Payments'
        verbose_name_plural = u'Payments'
        ordering = ['-id']

    def __str__(self):
        if self.pp_ipn_name:
            person=self.pp_ipn_name
        elif self.check_num:
            person="Check #"+str(self.check_num)+" via "+self.who_has_possession
        else:
            person="cash payment?"
        ptype="[?]"
        if self.registration_id==1: 
            ptype="[D]"
        elif self.registration:
            if self.registration.registration_source==0:
                ptype="[C]"
            if self.registration.registration_source==1:
                ptype="[M]"

        return str(ptype + "" + person) 

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in MembershipPayments._meta.fields]

class MembershipReport(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=255, blank=False, null=False, unique=True)
    display_order = models.IntegerField()
    category = models.CharField(max_length=255, blank=False, null=False, unique=False,choices=REPORT_TYPES, default="camp")

    class Meta:
        managed = False
        db_table = 'membership_report'
        verbose_name_plural = u'Website reports list'
        ordering = ['display_order']
    def __str__(self):
        return str(self.display_order) + ": " + str(self.title)


class CampTemplates(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    template_text = RichTextField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.CharField(max_length=255, blank=False, null=False, unique=True)
    display_order = models.IntegerField(null=True,blank=True)
    subject = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'camp_templates'

    def __str__(self):
        return str( self.slug)

class CampConstants(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    year = models.IntegerField(blank=False, null=True, default=datetime.datetime.now().year)
    form_open = models.DateField()
    form_close = models.DateField()
    form_late = models.DateField()
    camp_start = models.DateField()
    history = HistoricalRecords()

    class Meta:
        managed = False
        db_table = 'camp_constants'

    def __str__(self):
        return str(self.year) + " open:" + str(self.form_open)


