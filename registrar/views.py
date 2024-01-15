from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.template import loader
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models import Q
from django.forms import modelformset_factory, Textarea, TextInput, DateInput
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.template.loader import get_template
from django.contrib.auth.decorators import user_passes_test

from camp.models import *
from camp.custom.mylogger import p
from camp.custom.tday import tday
try:
    from camp.constants import dvd_price_decimal,membership_price_decimal,linens_price_decimal
    from camp.views import get_discount,  emailconfirmation, generate_email_html, get_membership_info, generate_cart_from_registration
except: pass

from paypal.standard.ipn.models import PayPalIPN

from .forms import *
from .models import *

from decimal import Decimal
from io import BytesIO
from xhtml2pdf import pisa
from weasyprint import HTML

import re
import csv
import datetime

now = datetime.datetime.now()
years = list(reversed(range(2004, datetime.datetime.now().year+2)))
        #range() does not include the final number in the range)

def get_thisyear(request):
    now = datetime.datetime.now()
    if request.GET.get('year'):
        thisyear=int(request.GET.get('year'))
    elif request.session.get('year'):
        thisyear=request.session.get('year')
        p("thisyear: session found")
    else:
        thisyear=datetime.datetime.now().year
        p("thisyear: no session found")

    p("thisyear:",thisyear)
    request.session['year']=thisyear

    #thisyear should be returned as a string since that's what the HTTP reuqest object returns
    return int(thisyear)

def registrar_check(user):
        return user.groups.filter(name__in=['registrar',])
def readonly_check(user):
        return user.groups.filter(name__in=['registrar','readonly'])

def render_to_pdf(template_src, request, context_dict={},pdf_only=False):
    template = get_template(template_src)
    context_dict['pdf_view']=True
    html  = template.render(context_dict,request)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if pdf_only:
        return result.getvalue()
    else:
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None


@login_required
@user_passes_test(registrar_check)
def docs(request):
    thisyear=get_thisyear(request)
    registration_status_options=CampRegistrationStatus.objects.all()
    return render(request, 'registrar/docs.html', {
        'years':years,
        'thisyear':thisyear,
        'registration_status_options':registration_status_options,
        "reports": MembershipReport.objects.all,
        })

@login_required
@user_passes_test(readonly_check)
def homepage(request):
    thisyear=get_thisyear(request)
    p("homepage thisyear",thisyear)

    registration_status_options=CampRegistrationStatus.objects.all()
    payments_waiting_for_deposit=MembershipPayments.objects.filter(waiting_for_deposit__exact=1).filter(date_recd__year=thisyear).select_related('registration').select_related('membership_person')

    c=CampCamper.objects.filter(registration__year=thisyear).order_by('-pk').select_related('registration_type').select_related('registration'). \
            select_related('registration__registration_status'). \
            order_by('registration'). \
            exclude(registration__email_confirmation_sent=1)

    unconfirmed_campers,registration_stats=generate_mycampers_dict(c)

    c=CampCamper.objects.filter(registration__year=thisyear).order_by('-pk').select_related('registration_type').select_related('registration').select_related('registration__registration_status').order_by('registration')
    all_campers,registration_stats=generate_mycampers_dict(c)

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
#+----+----------------------------+-----------------------------------------------------------------------------------------+---------------+

    return render(request, 'registrar/index.html', {
        'payments_waiting_for_deposit':payments_waiting_for_deposit,
        'years':years,
        'return':"home",
        'PAYMENT_TYPES':PAYMENT_TYPES,
        'registration_status_options':registration_status_options,
        'thisyear':thisyear,
        'unconfirmed_campers':unconfirmed_campers,
        'all_campers':unconfirmed_campers,
        'registration_stats':registration_stats,
        "reports": MembershipReport.objects.all,
        })

@user_passes_test(readonly_check)
@login_required
def reports_home(request):
    return render(request=request,
              template_name='registrar/reports_home.html',
              context={
                  "report": MembershipReport.objects.all,
              })

@user_passes_test(readonly_check)
@login_required
def refund_report(request):
    thisyear=get_thisyear(request)
    payments=MembershipPayments.objects.filter(created_at__year=thisyear).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS).filter(registration__registration_source=0).filter(registration__payment_type="paypal").filter(registration__id__gt=10664)

    total_gross=0
    for pp in payments:
        total_gross+=pp.gross_amt

    return render(request=request,
              template_name='registrar/reports_refund.html',
              context={
                  "payments":payments,
                  "thisyear":thisyear,
                  "total_gross":total_gross,
                  "reports": MembershipReport.objects.all,
              })

@user_passes_test(readonly_check)
@login_required
def report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear,page_title='',template='registrar/reports_generic.html',hidden_fields=('registration',)):

        thisyear=get_thisyear(request)
        headers=[]
        searchfields=[]
        result_list=[]
        filename="report.csv"

        slugs = [c.slug for c in MembershipReport.objects.all()]
        if report_by_slug in slugs:
            matching_report = MembershipReport.objects.get(slug=report_by_slug)
            page_title=matching_report.title
            filename=str(matching_report.title)+".csv"

        #it would be better to pull this out of models.verbose_name but I could not figure out a clean way to do it.
        for f in fields:
            if next(iter(f)) not in hidden_fields:
                  headers+=f.values()
                  searchfields+=f

        for x in result_dict:
            if x not in hidden_fields:

        ###CAREFUL WITH DEBUG PRINT STATEMENTS IN HERE
        # it will fail with a log message similar to:  'ascii' codec can't encode character '\xa9' in position 175: ordinal not in range(128)
                result_list+=x.values(),

        context={
                    "result_list": result_list, 
                    "result_dict": result_dict,
                    'headers':headers,
                    'years':years,
                    'thisyear':thisyear,
                    'hidden_fields':hidden_fields,
                    "page_title": page_title,
                    "reports": MembershipReport.objects.all(),
                    }
                
        if request.GET.get('csv'):
            #filename="camp_roster.csv"
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
            writer = csv.writer(response)

            headers_without_hidden_fields=[]
            for f in fields:
                headers_without_hidden_fields+=f.values()

            writer.writerow(headers_without_hidden_fields)


            for r in result_list:
                writer.writerow(r)
            return response

        if request.GET.get('pdf'):
                #careful with print'ing stuff here, non-ascii chars break dreamhost
                pdf = render_to_pdf(template, request, context)
                return HttpResponse(pdf, content_type='application/pdf')

        return render(request=request,
                      template_name=template,
                      context=context
                            )


@user_passes_test(readonly_check)
@login_required
def report_by_slug(request, report_by_slug):
    now=datetime.datetime.now()

    if request.GET.get('q'):
        search=request.GET.get('q')
        messages.error(request, "Filter applied: "+'"'+str(search)+'"')
    else: search = ''

    searchfields=[]
    thisyear=get_thisyear(request)

#################CAMP ROSTER################
    if report_by_slug == "camproster":

        fields=[
                {'registration':'id'},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'phone':'phone'},
                {'email':'email'},
                {'publish':'pubmail'},
                {'registration__address1':'address1'},
                {'registration__address2':'address2'},
                {'registration__city':'city'},
                {'registration__state':'state'},
                {'registration__zip':'zip'},
                {'registration__country':'country'},
                {'registration__year':'year'},
                ]

        for f in fields: searchfields+=f

        result_dict = CampCamper.objects.filter(
                    Q(registration__city__icontains=search) | 
                    Q(registration__state__icontains=search) | 
                    Q(first_name__icontains=search) | 
                    Q(last_name__icontains=search)).filter(registration__year__icontains=thisyear).filter(adult_or_child__iexact="adult").values(*searchfields).order_by('last_name').filter(registration__registration_source=0).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS)

        for result in result_dict:
            #p(result)
            if result['publish'] is True or result['registration__year'] == 2020:
                pass
            else:
                result['email']='<>'
                result['phone']='<>'
                result['registration__address1']='<>'
                result['registration__address2']=''
                result['registration__city']=''
                result['registration__state']=''
                result['registration__zip']=''
                result['registration__country']=''

        hidden_fields=['first_name','last_name','year','registration__address1','registration__address2','registration__city','registration__state','registration__country','publish','registration']
    
        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear,hidden_fields=hidden_fields,template="registrar/reports_camproster.html")

#################T-SHIRT ################
    elif report_by_slug == "t-shirt":

        fields=[
                {'registration':'id'},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'phone':'phone'},
                {'email':'email'},
                {'free_t_shirt':'free t_shirt'},
                {'t_shirt_type__description':'t-shirt'},
                {'registration__address1':'address1'},
                {'registration__address2':'address2'},
                {'registration__city':'city'},
                {'registration__state':'state'},
                {'registration__zip':'zip'},
                {'registration__country':'country'},
                {'registration__created_at':'created_at'},
                ]
    
        for f in fields: searchfields+=f
        result_dict=CampCamper.objects.filter(
                    Q(free_t_shirt=1) | 
                    Q(t_shirt_type_id__gt=1)
                ).filter(registration__year__icontains=thisyear).values(*searchfields).filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(registration__city__icontains=search)).filter(registration__registration_source=0).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS)
    
        hidden_fields=['first_name','last_name','year','registration__address1','registration__address2','registration__city','registration__state','registration__country','publish','registration']
        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear,hidden_fields=hidden_fields,template="registrar/reports_tshirt.html")

#################DVD ################
    elif report_by_slug == "dvd":

        fields=[
                {'registration':'id'},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'phone':'phone'},
                {'email':'email'},
                {'registration__address1':'address1'},
                {'registration__address2':'address2'},
                {'registration__city':'city'},
                {'registration__state':'state'},
                {'registration__zip':'zip'},
                {'registration__country':'country'},
                ]
    
        for f in fields: searchfields+=f
        result_dict=CampCamper.objects.filter(
                    Q(dvd__exact=1) 
                ).filter(registration__year__icontains=thisyear).values(*searchfields).filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(registration__city__icontains=search)).filter(registration__registration_source=0).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS)
        hidden_fields=['first_name','last_name','year','registration__address1','registration__address2','registration__city','registration__state','registration__country','publish','registration']
        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear,hidden_fields=hidden_fields,template="registrar/reports_dvd.html")

#################CAMP STAFF ################
    elif report_by_slug == "campstaff":

        fields=[
                {'registration':"id"},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'registration_type__description':'registration type'},
                {'staff':'staff'},
                {'staff_position':'staff_position'},
                {'free_t_shirt':'free_t_shirt'},
                {'t_shirt_type__description':'t_shirt_type__description'},
                ]

        for f in fields: searchfields+=f
        result_dict=CampCamper.objects.filter(
                    Q(staff__exact=1) | 
                    Q(registration_type__description__icontains="staff") | 
                    Q(staff_position__isnull=False)
                ).filter(registration__year__exact=thisyear).filter(Q(first_name__icontains=search)| Q(last_name__icontains=search) | Q(diet_details__icontains=search)).values(*searchfields).filter(registration__registration_source=0).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS)
        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear)

#################LINEN ################
    elif report_by_slug == "linen":

        fields=[
                {'registration':"id"},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'registration_type__description':'registration type'},
                {'need_linen':'linen'},
                ]

        for f in fields: searchfields+=f
        result_dict=CampCamper.objects.filter(
                    Q(need_linen__exact=1) 
                ).filter(registration__year__exact=thisyear).filter(Q(first_name__icontains=search)| Q(last_name__icontains=search)).values(*searchfields).filter(registration__registration_source=0).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS)
        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear)


#################DIETS ################
    elif report_by_slug == "diet":

        fields=[
                {'registration':"id"},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'registration_type__description':'registration type'},
                {'diet':'diet'},
                {'diet_details':'diet details'},
                ]

        for f in fields: searchfields+=f
        result_dict=CampCamper.objects.filter(
                    Q(diet__exact=1) | 
                    Q(diet_details__isnull=False)
                ).filter(registration__year__exact=thisyear).filter(Q(first_name__icontains=search)| Q(last_name__icontains=search) | Q(diet_details__icontains=search)).values(*searchfields).filter(registration__registration_source=0).filter(registration__registration_source=0).exclude(diet_details="").filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS)
                #include if diet is NOT checked, but they filled in the diet_details form anyways

        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear)

#################FAMILY PROGRAM ################
    elif report_by_slug == "familyprogram":

        fields=[
                {'registration':'id'},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'age':'age'},
                {'family_program':'In Fam Prog'},
                {'registration__city':'city'},
                ]

        for f in fields: searchfields+=f
        result_dict=CampCamper.objects.filter(
                    Q(family_program__exact=1) | 
                    Q(adult_or_child__iexact='child')
                ).filter(registration__year__icontains=thisyear).filter(Q(first_name__icontains=search) | Q(last_name__icontains=search)| Q(registration__city__icontains=search)).values(*searchfields).filter(registration__registration_source=0).filter(registration__registration_source=0).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS)

        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear)

#################ADDRESS LABELS ################
    elif report_by_slug == "addresslabels":
        fields=[
                {'registration':'id'},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'registration__address1':'address1'},
                {'registration__address2':'address2'},
                {'registration__city':'city'},
                {'registration__state':'state'},
                {'registration__zip':'zip'},
                {'registration__country':'country'},
                ]
    
        for f in fields: searchfields+=f
        result_dict=CampCamper.objects.values(*searchfields).filter(registration__year__exact=thisyear).order_by('last_name').filter(registration__registration_source=0).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS)


        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear,template='registrar/reports_addresslabels.html')

#################NAME BADGES ################
    elif report_by_slug == "namebadges":

        fields=[
                {'registration':'id'},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'registration__city':'city'},
                {'registration__state':'state'},
                {'adult_or_child':'age category'},
                {'staff_position':'Staff position'},
                {'registration__postmark':'postmark'},
                ]
        for f in fields: searchfields+=f
        result_dict=CampCamper.objects.filter(registration__year__icontains=thisyear).values(*searchfields).filter(Q(first_name=search) | Q(last_name=search) | Q(registration__city__icontains=search)).filter(registration__registration_source=0).filter(registration__registration_source=0).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS)
        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear)

#################HOUSING ################
    elif report_by_slug == "housingreport":

        fields=[
                {'registration':'id'},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'phone':'homephone'},
                {'registration__city':'city'},
                {'housing_assigned':'Assigned'},
                {'housing_type__short_description':'housing preference'},
                {'share_housing':'sharewith'},
                {'adult_or_child':'age category'},
                {'need_linen':'Linen'},
                {'registration__camper_note':'camper_note'},
                {'registration__postmark':'postmark'},
                {'registration__created_at':'created_at'},
                ]
    
        for f in fields: searchfields+=f
        result_dict=CampCamper.objects.filter(registration__year__icontains=thisyear).values(*searchfields).order_by('registration').filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(registration__city__icontains=search)| Q(housing_assigned__icontains=search)).filter(registration__registration_source=0).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS)

        hidden_fields=('registration__created_at','registration')
        for r in result_dict:
            if r['registration__postmark'] is None:
                r['registration__postmark']=r['registration__created_at']

        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear,hidden_fields=hidden_fields)


#################MUSICIANS ################
    elif report_by_slug == "musicians":

        fields=[
                {'registration':'id'},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'phone':'phone'},
                {'email':'email'},
                {'registration__city':'city'},
                {'band':'band'},
                {'instruments':'instruments'},
                ]
    
        for f in fields: searchfields+=f
        result_dict=CampCamper.objects.filter(
                    Q(band__exact=1) | 
                    Q(instruments__isnull=False)
                ).filter(registration__year__icontains=thisyear).values(*searchfields).filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(registration__city__icontains=search)).filter(registration__registration_source=0).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS)
        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear)

#################DONATIONS ################
    elif report_by_slug == "donations_report":

        fields=[
                {'id':'payment_id'},
                {'pp_ipn_name':"pp_ipn_name"},
                {'pp_ipn_email':"PP email"},
                {'registration_id':'registrationid'},
                ]
    
        for f in fields: searchfields+=f
        result_dict=MembershipPayments.objects.filter(
                Q(registration_id__exact=1) |
                Q(general_fund__gt=0) |
                Q(bobbi_fund__gt=0) |
                Q(chuck_fund__gt=0) |
                Q(floor_fund__gt=0) |
                Q(texakolo_fund__gt=0) |
                Q(camp_fund__gt=0) |
                Q(music_fund__gt=0) 
                ).filter(created_at__year=thisyear).filter(registration_id__gte=1).values(*searchfields)
        i=0
        for r in result_dict:
            if r['pp_ipn_name']:
                e=r.pop('pp_ipn_email')
                reg=r.pop('registration_id')
                r['first_name']=r['pp_ipn_name'].split(' ',1)[0]
                r['last_name']=r['pp_ipn_name'].split(' ',1)[1]
                r.pop('pp_ipn_name')
                r['pp_ipn_email']=e
                pmt=MembershipPayments.objects.get(pk=r['id']) 
                items=itemize_payment(None,pmt)
            else:
                campers=CampCamper.objects.filter(registration_id=r['registration_id'])
                p("found campers",campers, "regid:",r['registration_id'])
                reg=r.pop('registration_id')
                e=r.pop('pp_ipn_email')
                r['first_name']=campers[0].first_name
                r['last_name']=campers[0].last_name
                r.pop('pp_ipn_name')
                r['email']=campers[0].email
                pmt=MembershipPayments.objects.get(pk=r['id']) 
                items=itemize_payment(None,pmt)
                
            for key,val in items.items():
                if "fund" in key:
                    r[key]=val
                    if i == 0:
                        fields.append({val:key})
            i+=1
            r['donations_report']=True
        hidden_fields=('registrationid','donations_report')
        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear,hidden_fields=hidden_fields)

#################MEMBER SEARCH ################
    elif report_by_slug == "member_search":

        fields=[
                {'registration':'id'},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'email':"email"},
                {'phone':"phone"},
                {'registration__address1':'address1'},
                {'registration__city':'city'},
                {'registration__year':'year'},
                {'registration__registration_source':'source'},
                {'registration__registration_status':'status'},
                ]
    
        if search=='': search="ASDASDASDADS"
        for f in fields: searchfields+=f
        result_dict=CampCamper.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(registration__city__icontains=search)).filter(registration__registration_status_id__in=REGISTRATION_PAID_STATUS).values(*searchfields).order_by('-registration__year')
        result_dict=CampCamper.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(registration__city__icontains=search)).values(*searchfields).order_by('-registration__year')
        return report_by_slug_render(request, report_by_slug,fields,result_dict,thisyear)


###################TIFD MEMBERS#########

    elif (report_by_slug == "members_in_good_standing") or \
         (report_by_slug == "members_expiring"):

        if report_by_slug == "members_expiring":
            now=datetime.datetime.strptime(str(thisyear), '%Y')
        else:
            #now=datetime.datetime.now() #shouldnt the datepicker work?
            now=datetime.datetime.strptime(str(thisyear), '%Y') 

        fields=[
                {'membership_address':'id'},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'phone':'phone'},
                {'email':'email'},
                {'membership_type__membertype':'source'},
                {'membership_valid_to':'membership_valid_to'},
                ]
    
        ####LEGACY MEMBERS##############3
        for f in fields: searchfields+=f

        result_dict_lifetime_valid=MembershipPerson.objects.\
                filter(Q(membership_valid_to__gte=now)).\
                filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(membership_address__city__icontains=search)).\
                filter( Q(first_name__icontains=search) |
                            Q(last_name__icontains=search) | 
                            Q(membership_address__city__icontains=search)
                            ).\
                exclude(membership_type=4).\
                filter(legacy_agecategory="Adult").\
                values(*searchfields)

        result_dict_lifetime_expired=MembershipPerson.objects.\
                filter(Q(membership_valid_to__year__lte=now.year)).\
                filter(Q(membership_valid_to__year__gte=thisyear)).\
                filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(membership_address__city__icontains=search)).\
                filter(legacy_agecategory="Adult").\
                filter( Q(first_name__icontains=search) |
                            Q(last_name__icontains=search) |
                            Q(membership_address__city__icontains=search)
                            ).\
                exclude(membership_type=4).\
                exclude(last_name__exact=None).\
                exclude(first_name__exact=None).\
                values(*searchfields)

            #result_dict_lifetime_valid=result_dict_lifetime_valid.\
                    #result_dict_lifetime_expired=result_dict_lifetime_expired.\


        #result_dict_lifetime_expired={}
        #result_dict_lifetime_valid={}

        #grab all the campers / online membership renewals
        #NEW DATABASE MEMBERS
        fields=[
                {'registration':'id'},
                {'first_name':"firstname"},
                {'last_name':"lastname"},
                {'phone':'phone'},
                {'email':'email'},
                {'registration__registration_source':'source'},
                {'membership_valid_to':'membership_valid_to'},
                ]
        searchfields=[]
        for f in fields: searchfields+=f

        result_dict_camper_valid=CampCamper.objects.\
                filter(membership_valid_to__gt=now).\
                filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(registration__city__icontains=search)).\
                values(*searchfields)

        result_dict_camper_expired=CampCamper.objects.\
                filter(membership_valid_to__year__lte=now.year).\
                filter(membership_valid_to__year__gte=thisyear).\
                filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(registration__city__icontains=search)).exclude(adult_or_child__exact="child").\
                values(*searchfields)

        for r in result_dict_camper_valid:
            if r['registration__registration_source']: 
                r['registration__registration_source']="mem"
            else:
                r['registration__registration_source']="camp"

        for r in result_dict_camper_expired:
            if r['registration__registration_source']: 
                r['registration__registration_source']="mem"
            else:
                r['registration__registration_source']="camp"

        result_dict_valid=(list(result_dict_camper_valid)+(list(result_dict_lifetime_valid)))
        result_dict_valid=sorted(result_dict_valid, key = lambda x: x['last_name'])

        result_dict_expired=(list(result_dict_camper_expired)+(list(result_dict_lifetime_expired)))
        result_dict_expired=sorted(result_dict_expired, key = lambda x: x['last_name'])

        if report_by_slug == "members_in_good_standing":
            result_dict=result_dict_valid
        else:
            result_dict=result_dict_expired

        result_dict_no_dupes=list()
        dupe_check=set()

        #should I de-dupe AFTER getting membership info.. wally changed his email address... maybe not.. they will bubble out eventually
        #for example wally changing email address
        for r in result_dict:
            data,member=get_membership_info(r['first_name'],r['last_name'])
            index_string=r['first_name'].strip().lower()+"|||"+r['last_name'].strip().lower()+"|||"#+str(r['email']).strip().lower()
            if (index_string not in dupe_check):
                dupe_check.add(index_string)
                rs=None
                rid=0
                if member:
                    if member[0].registration:
                        if member[0].registration.registration_source==0:
                            rs="camp"
                        elif member[0].registration.registration_source==1:
                            rs="membership"
                    else: rs="old database"

                    if member[0].registration_id:
                        rid=member[0].registration_id

                    if (report_by_slug=="members_expiring") and (
                            member[0].membership_valid_to.year < datetime.datetime.strptime(str(thisyear),'%Y').year or
                            member[0].membership_valid_to.year > now.year 
                            ):
                        p("pass:",member[0],"valid_to:",member[0].membership_valid_to.year,"search",datetime.datetime.strptime(str(thisyear),'%Y').year)
                        pass
                    else:
                        result_dict_no_dupes.append({
                            'registration_id':rid,
                            'first_name':member[0].first_name,
                            'last_name':member[0].last_name,
                            'phone':member[0].phone,
                            'email':member[0].email,
                            'registration_source':rs,
                            'membership_valid_to':member[0].membership_valid_to,
                            })

        return report_by_slug_render(request, report_by_slug,fields,result_dict_no_dupes,thisyear)

    else:
        raise Http404("report does not exist")

##############END REPORTS##############

@user_passes_test(registrar_check)
@login_required
def ipn_view(request,ipn_id):
    pp_ipn_info=generate_ipn_dict(ipn_id)
    return render(request,'registrar/ipnview.html',{
        "pp_ipn_info":pp_ipn_info,
        })

def generate_ipn_dict(ipn_id):
    remove=('_state',
            )
    try:
        ipn=PayPalIPN.objects.get(id=ipn_id) 
    except:
        ipn=None
    if ipn:
        p("generated ipn view for ",ipn)
        ipn=ipn.__dict__
        for r in remove:
            ipn.pop(r)
        return ipn
    else: 
        return None

@user_passes_test(registrar_check)
@login_required
def deposit(request):
    thisyear=get_thisyear(request)

    saved=False

    if request.method == 'POST':
        p("deposit POST",request.POST)
        if request.POST.get('payments'):
            deposit_date=request.POST.get('deposit_date')
            post_payments=request.POST.getlist('payments')
            payments=MembershipPayments.objects.filter(pk__in=post_payments)
            p("user",request.user,"payments",payments,"POST",request.POST)
            if request.POST.get('save'):
                for x in payments:
                    x.waiting_for_deposit=0
                    x.deposit_date=deposit_date
                    p(request.user,"payments post",x.deposit_date)
                    x.save()
                    saved=True
            payments=MembershipPayments.objects.filter(date_recd__icontains=thisyear).filter(pk__in=payments).select_related('registration').select_related('membership_person')
        else:
            #triggered when user submits a blank form - no payments
            messages.error(request, "Error - no payments selected.  Please select a payment by checking the box to the left of the payment.")
            return HttpResponseRedirect(reverse('registrar:payments'))

        if saved:
            return HttpResponseRedirect(reverse('registrar:payments'))

        return render(request, 'registrar/deposit.html', {
            'payments':payments,
            'years':years,
            'thisyear':thisyear,
            "reports": MembershipReport.objects.all,
            })

@user_passes_test(registrar_check)
@login_required
def payments(request):
    thisyear=get_thisyear(request)

    if request.method == 'POST':
        if request.POST.get('payments'):
            payments=request.POST.getlist('payments')
            p(request.user,"payments",payments,"POST",request.POST)
            for x in payments:
                p("payments post",x)

    payments=MembershipPayments.objects.filter(date_recd__icontains=thisyear).select_related('registration').select_related('membership_person')
    return render(request, 'registrar/payments.html', {
        'payments':payments,
        'years':years,
        'thisyear':thisyear,
        "reports": MembershipReport.objects.all,
        })

@user_passes_test(registrar_check)
@login_required
def payments_delete(request,payment_id,return_to=None):
    now = datetime.datetime.now()
    thisyear=get_thisyear(request)
    payment=get_object_or_404(MembershipPayments, id=payment_id)
    p(request.user,"deleting payment",payment_id,payment.__dict__)
    if request.GET.get('return_to') == "payments":
        return_to="registrar:payments"
    payment.delete()
    if return_to:
        rev=reverse(return_to)+"?year="+str(thisyear)+"&ts="+str(now.microsecond)
        return HttpResponseRedirect(rev)

    rev=reverse('registrar:registrar')+"?year="+str(thisyear)+"&ts="+str(now.microsecond)
    return HttpResponseRedirect(rev)

@user_passes_test(registrar_check)
@login_required
def adjustment_add(request):
    if request.POST.get('adjustment') and request.POST.get('registration_id'):
        registration=get_object_or_404(CampRegistration, id=request.POST.get('registration_id'))
        if registration:
            adjustment=Decimal(request.POST.get('adjustment'))
            p(request.user,"adjustment found",type(adjustment),adjustment)
            registration.adjustment=adjustment
            registration.save()
            #make sure to regenerate the care here - we added a discount.
            generate_cart_from_registration(registration.id,save=True)
            
        else:
            p('ERROR - adjustment without registration')
            raise NameError('registration')
    if request.META.get('HTTP_REFERER', '/'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(reverse('registrar:registrar'))

def itemize_payment(registration,payment=None):

    #this takes a camp registration (or payment) and returns a conveinent dict of things a registrant has paid for
    #used in the donation letter function and in the payment's report report

    #initialize the default itemized payment field values
    payment_fields={
            'camp_fee':0,
            'membership_fee':0,
            't_shirt_fee':0,
            'dvd_fee':0,
            #'shipping_fee':0,
            'housing_fee':0,
            'other_fee':0,
            #'paypal_fee':0,  ignore paypal fee it's calculated separately
            #'refund_amt':0,  refund_amt onlt exists in the payment model so exclude it
            'late_fee':0,
            'general_fund':0,
            'gfc_linens':0,
            'camp_fund':0,
            'bobbi_fund':0,
            'chuck_fund':0,
            'texakolo_fund':0,
            'floor_fund':0,
            'music_fund':0,
            'camp_fund':0,
            }

    if registration is None and payment is None: 
        p("itemization returning empty dict")
        return payment_fields

    elif registration is None and payment: 
        p("itemization returning payment dict")
        for key in payment_fields:
            attr=getattr(payment,key)
            if attr is None: attr=Decimal(0.0)
            payment_fields[key]=attr

        p("itemization payment dict",payment_fields)
        return payment_fields
    else:

        p("itemization returning registration dict")
        campers=CampCamper.objects.filter(registration_id=registration.id).select_related('registration_type')
        for c in campers:
            if c.need_linen:
                payment_fields['gfc_linens']+=linens_price_decimal
            if c.t_shirt_type_id:
                payment_fields['t_shirt_fee']+=c.t_shirt_type.price
            if c.dvd:
                payment_fields['dvd_fee']+=dvd_price_decimal
            if c.housing_type_id:
                payment_fields['housing_fee']+=c.housing_type.price
            if c.registration_type_id and c.registration_type.slug!="membership" :
                #membership "registration" types should not be calculated as camp fees
                if c.custom_registration_price and c.custom_registration_price >0:
                    payment_fields['camp_fee']+=c.custom_registration_price
                else:
                    payment_fields['camp_fee']+=c.registration_type.price

            #for camp, if member is adult and join_tifd=1, add a membership
            if c.registration.registration_source==0:
                if c.adult_or_child=="adult" and c.join_tifd==1:
                    payment_fields['membership_fee']+=membership_price_decimal

                ##membership renewal registrations
            if c.registration_type.slug=="membership":
                if "ifetime" in c.registration_type.description:
                    payment_fields['membership_fee']+=c.registration_type.price
                else:
                    payment_fields['membership_fee']+=c.registration_type.price*c.membership_years


        if registration.shipping_fee:
            payment_fields['shipping_fee']+=registration.shipping_fee
        if registration.donation_camp_fund:
            payment_fields['camp_fund']+=registration.donation_camp_fund
        if registration.donation_chuck:
            payment_fields['chuck_fund']+=registration.donation_chuck
        if registration.donation_bobbi_gillotti:
            payment_fields['bobbi_fund']+=registration.donation_bobbi_gillotti
        if registration.donation_floor_fund:
            payment_fields['floor_fund']+=registration.donation_floor_fund
        if registration.donation_tifd:
            payment_fields['general_fund']+=registration.donation_tifd
        if registration.donation_live_music:
            payment_fields['music_fund']+=registration.donation_live_music
        if registration.late_fee:
            payment_fields['late_fee']+=registration.late_fee
        if registration.rebate:
            payment_fields['membership_fee']=payment_fields['membership_fee']+registration.rebate.price
            p("applied rebate",registration.rebate.price, "membership fee:",payment_fields['membership_fee'])
        p("new itemization for reg", registration.pk, "payment fields",payment_fields)
        return(payment_fields)


@user_passes_test(registrar_check)
@login_required
def payment_view(request,payment_id):
    payment=get_object_or_404(MembershipPayments, id=payment_id)
    return render(request, 'registrar/payment_view.html', {
        'payment':payment.__dict__, 
        })


@user_passes_test(registrar_check)
@login_required
def payments_add(request,payment_id=False):
    #NOTE: the payments function needs to handle paymes with and without registration_ids.
    #SEE ALSO: signals.py for the paypal IPN code.
    now=datetime.datetime.now()

    thisyear=get_thisyear(request)
    registration=None
    previous_payments=None
    cart={}
    cart_total=0
    discount_list=[]
    discount_total=0
    remaining_balance=0
    payments_total=0
    pp_ipn_info={}

    if request.GET.get('registration_id'):
        try:
            #if registration id is not found, try and fail gracefully
            registration=CampRegistration.objects.get(pk=request.GET.get('registration_id'))
            cart,cart_total=generate_cart_from_registration(registration.id,save=False)
            discount_list,discount_total=get_discount(registration.id)
            remaining_balance=cart_total
        except Exception as e:
            p("CRITICAL ERROR: registration not found: \"",request.GET.get('registration_id'),"\"",request,e)
            messages.error(request, 'Registration ' + request.GET.get('registration_id') + " not found! !" )
            return redirect("registrar:homepage")

    ##totally new payment
    ##pre-generate all the itemized fields from the shopping cart

    if payment_id is False:
        new_payment_form=PaymentAddForm()

        #initial fields for every payment form
        new_payment_form.fields['date_recd'].initial = now.strftime('%Y-%m-%d')
        new_payment_form.fields['who_has_possession'].initial = str(  str(request.user.first_name+ " " + str(request.user.last_name)))
        #if request.GET.get('registration_id'):
        if (registration):

            #initial fields for payment form when a registration is associated
            new_payment_form.fields['registration'].initial = registration.id
            new_payment_form.fields['gross_amt'].initial = registration.cart_total
            new_payment_form.fields['net_amt'].initial = registration.cart_total
            if registration.paypal_fee:
                new_payment_form.fields['net_amt'].initial-=registration.paypal_fee
                new_payment_form.fields['who_has_possession'].initial = "paypal"

            previous_payments=MembershipPayments.objects.filter(registration=registration)  ##but not the current payment?

            if previous_payments:
                for payment in previous_payments:
                    remaining_balance-=payment.gross_amt
                    payments_total+=payment.gross_amt

            #try and fill in all the payment defaults by analyzing the registration
            payment_fields=itemize_payment(registration);
            p("calculated payment fields",payment_fields)

            if not previous_payments:
                #if there is a previous payment, don't try and guess what the itimizations should be
                for name,val in payment_fields.items():
                    new_payment_form.fields[name].initial = val

    ##editing an existing payment
    else:
        payment=MembershipPayments.objects.get(pk=payment_id)
        if payment.pp_ipn_id:
            pp_ipn_info=generate_ipn_dict(payment.pp_ipn_id)

        new_payment_form=PaymentAddForm(instance=payment)

        #the edit page doesn't have the registration_id param, so pull it from the payment object
        previous_payments={}

        if payment.registration_id:
            if CampRegistration.objects.filter(pk=payment.registration_id).exists():
                registration=payment.registration
                cart,cart_total=generate_cart_from_registration(registration.id,save=False)
                discount_list,discount_total=get_discount(registration.id)
                previous_payments=MembershipPayments.objects.filter(registration=registration)
                #iterate through each of the payments and subtract payment from cart_total to get remaining balance
                remaining_balance=cart_total
                for payment in previous_payments:
                    remaining_balance-=payment.gross_amt
                    payments_total+=payment.gross_amt

    if request.method == 'POST':
        if payment_id is False:
            #insert new payment
            new_payment_form = PaymentAddForm(request.POST)
        else:
            #update existing payment
            payment=MembershipPayments.objects.get(pk=payment_id)
            new_payment_form = PaymentAddForm(request.POST,instance=payment)
        
        if new_payment_form.has_changed():
            for c in new_payment_form.changed_data:
                 p(request.user,"DEBUG: new_payment_form form field %s went from \"%s\" to \"%s\"" % (c,new_payment_form[c].initial, new_payment_form[c].data))
            if not new_payment_form.is_valid():
                for m in new_payment_form.errors:
                    p("new_payment_form error",m)
                    messages.error(request, m)
            if new_payment_form.is_valid():
                f=new_payment_form.save()
                messages.success(request, "Payment ID " + str(f.id) + " saved successfully!")
                p(request.user,"payment id",str(f.id),"saved")

                #this only works for NEW payments
                if request.POST.get('remaining_balance') == "0.00":
                    if registration:
                        registration.registration_status_id=8
                        registration.save()
                        campers=CampCamper.objects.filter(registration_id=registration.id)
                        for c in campers:
                            valid_from,valid_to=renew_tifd_membership(c,save=True)
                            p("remaining balance is zero - renewing membership for",c,"until:",valid_to)

                        #If this is a camp registration, and the balance is zero, redirect to the approval page
                        return HttpResponseRedirect(reverse('registrar:approve',args=(registration.id,)))

                if request.META.get('HTTP_REFERER', '/'):
                    p("REFERRER:",request.META.get('HTTP_REFERER', '/'))
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    return HttpResponseRedirect(reverse('registrar:registrar'))

            else:
                for m in new_payment_form.errors:
                    p("new_payment_form error",m)
                    messages.error(request, m)

    p("Remaining balance",remaining_balance)
    return render(request, 'registrar/new_payment.html', {
        'new_payment_form':new_payment_form,
        "reports": MembershipReport.objects.all,
        'previous_payments':previous_payments,
        'registration':registration,
        'remaining_balance':remaining_balance,
        'pp_ipn_info':pp_ipn_info,
        'discount_list':discount_list,
        'payments_total':payments_total,
        'cart':cart,
        #'registration_status_options':registration_status_options,
        'now':now,
        'years':years,
        'thisyear':thisyear,
        'cart_total':cart_total,
        })

@user_passes_test(readonly_check)
@login_required
def payments_report(request):
    
    search=""
    thisyear=get_thisyear(request)
    start_date=str(thisyear)+"-01-01"
    end_date=str(thisyear)+"-12-31"
    if request.GET.get('start_date'):
        start_date=request.GET.get('start_date')

    if request.GET.get('end_date'):
        end_date=request.GET.get('end_date')

    if request.GET.get('q'):
        search=request.GET.get('q')
        messages.error(request, "Filter applied: "+'"'+str(search)+'"')

    start_date_obj=datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj=datetime.datetime.strptime(end_date, '%Y-%m-%d')


    p("start",start_date_obj,"end",end_date_obj)
    payments=MembershipPayments.objects.filter(date_recd__gte=start_date_obj).filter(date_recd__lte=end_date_obj).filter(id__gte=1).filter(who_has_possession__icontains=search).select_related('membership_person').select_related('registration')

    if request.GET.get('csv'):
        filename="payments.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
        writer = csv.writer(response)

        headers_without_hidden_fields=[]
        for f in MembershipPayments._meta.get_fields():
            p("field",f.name)
            headers_without_hidden_fields.append(f.name)

        writer.writerow(headers_without_hidden_fields)
        p("header",headers_without_hidden_fields)

        for pmt in payments:
            pmt.__dict__.pop('_state')
            writer.writerow(pmt.__dict__.values())
        return response

    registrations={}
    payments_total=0
    payments_net=0
    payments_wfd=0
    payments_notwfd=0
    payments_paypalfee=0
    registrations_cart_total=0
    itemizations_dict=itemize_payment(None)
    donation_itemizations_dict=itemize_payment(None)
    itemizations_total=0
    donation_itemizations_total=0
    refunds_total=0


    for pmt in payments:
        if pmt.id > 0:
            p("payment id:",pmt.id,pmt.gross_amt,pmt)
            payments_total+=pmt.gross_amt
            if pmt.refund_amt:
                refunds_total+=abs(pmt.refund_amt)

            if pmt.paypal_fee: payments_paypalfee+=pmt.paypal_fee

            if pmt.waiting_for_deposit: 
                payments_wfd+=pmt.gross_amt
            else:
                payments_notwfd+=pmt.gross_amt



            if pmt.registration_id==1 or pmt.registration_id is None:
            #  ^^^^ a donation        or ^^^^ a manually entered payment John Bloom
                donation_itemizations=itemize_payment(None,pmt)
                #p("d::",pmt,donation_itemizations)
                for key,val in donation_itemizations.items():
                    donation_itemizations_dict[key]+=val 
                    donation_itemizations_total+=val

            elif pmt.registration: #a payment attached to a camp/membership registration
                if pmt.registration.registration_status_id in REGISTRATION_PAID_STATUS:
                    #only report on PAID registrations

                    if pmt.registration.cart_total: registrations_cart_total+=pmt.registration.cart_total
                    itemizations=itemize_payment(pmt.registration)
                    #p("check3",pmt.id,itemizations['camp_fee'])
                    for key,val in itemizations.items():
                        itemizations_dict[key]+=val
                        itemizations_total+=val
                else:
                    if pmt.registration.registration_status_id==11 and pmt.registration.year==2021:
                        refunds_total-=abs(pmt.refund_amt)

            else:
                #this code is hit when a registration is deleted, but not the payment
                itemizations=itemize_payment(None,pmt)
                for key,val in itemizations.items():
                    itemizations_dict[key]+=val
                    itemizations_total+=val
                #legacy payments
                p("PAYMENT WITHOUT REGISTRATON ID!",pmt.registration_id,pmt.id,pmt.__dict__)


        if pmt.id==10220: 
            exit
    p("final dict",itemizations_dict)
    p("refunds_total",refunds_total)
    p("final donations dict",donation_itemizations_dict)
    payments_net=payments_total-payments_paypalfee #-refunds_total  refunds are already subtracted from gross

    return render(request, 'registrar/payments_report.html', {
        'payments':payments,
        'payments_total':payments_total,
        'payments_wfd':payments_wfd,
        'start_date':start_date,
        'end_date':end_date,
        'payments_paypalfee':payments_paypalfee,
        'payments_notwfd':payments_notwfd,
        'registrations_cart_total':registrations_cart_total,
        'registrations':registrations,
        'donation_itemizations':donation_itemizations_dict,
        'donation_itemizations_total':donation_itemizations_total,
        'itemizations':itemizations_dict,
        'itemizations_total':itemizations_total,
        'refunds_total':refunds_total,
        'payments_net':payments_net,
        "reports": MembershipReport.objects.all,
        "thisyear": thisyear,
        'years':years,
        })

@user_passes_test(registrar_check)
@login_required
def approve(request,registration_id):

    if request:
        p(registration_id,"here in approve",request.user)

    registration_status_options=CampRegistrationStatus.objects.all()
    registration=get_object_or_404(CampRegistration, id=registration_id)
    campers=CampCamper.objects.filter(registration=registration)

    cart,cart_total=generate_cart_from_registration(registration.id,save=False)
    previous_payments=MembershipPayments.objects.filter(registration=registration)

    membership_dict={}
    if request.method == 'POST':
        f=ApproveRegistrationForm(request.POST,instance=registration)
        if f.is_valid():
            f.save()
            approve_registration(request,registration)
            return HttpResponseRedirect(reverse("registrar:homepage"))
    approve_registration_form=ApproveRegistrationForm(instance=registration)

    for c in campers:
        c.temp_membership_valid_from,c.temp_membership_valid_to=renew_tifd_membership(c,save=False)

    if registration.registration_source == 0:
        email_content=generate_email_html(registration,template_slug="registration_approved")
    elif registration.registration_source == 1:
        email_content=generate_email_html(registration,template_slug="membership_confirmed")

    else:
        p("REGISTRATION SOURCE WAS NOT ZERO OR ONE -- THIS SHOULD NOT HAPPEN")
        email_content=generate_email_html(registration,template_slug="membership_approved")

    approve_registration_form.initial['registrar_approval_note'] = email_content['intro_message']

    return render(request, 'registrar/approve.html', {
        'registration':registration,
        'cart':cart,
        'previous_payments':previous_payments,
        'cart_total':cart_total,
        'registration_status_options':registration_status_options,
        "years": years,
        "reports": MembershipReport.objects.all,
        "campers": campers,
        'html_body':email_content['html_body'],
        'subject':email_content['subject'],
        'approve_registration_form':approve_registration_form,
        })

def approve_registration(request,registration):
    campers=CampCamper.objects.filter(registration=registration)
    if registration.registration_status_id in REGISTRATION_PAID_STATUS: 
        for c in campers:
            renew_tifd_membership(c,save=True)

    if registration.registration_source==0:
        template="registration_approved"
    else:
        template="membership_confirmed"
    if not emailconfirmation(registration,request,template):
        #if email confirmation function fails, reload the page and hopefully provide a sane error message
        p("email confirmation failed regid:",registration.id)
        return HttpResponseRedirect(reverse('registrar:approve',args=(registration.id,)))
    else:
        registration.email_confirmation_sent=1
        registration.save()
        msg="Success! Registration approved."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('registrar:registrar'))
    return True


def membership_report(request):
    now=datetime.datetime.now()
    thisyear=get_thisyear(request)
    if request.GET.get('q'):
        search=request.GET.get('q')
        messages.error(request, "Filter applied: "+'"'+str(search)+'"')
    else: search = ''

    p("search'",search)
    membership_person = MembershipPerson.objects.filter(
                Q(last_name__icontains=search) |
                Q(first_name__icontains=search)
                ).filter(membership_valid_to__gte=datetime.date(now.year, now.month, now.day)).select_related('membership_address').select_related('membership_type')
    #.values(*searchfields).order_by('last_name')

    membership_camper = CampCamper.objects.filter(
                Q(last_name__icontains=search) |
                Q(first_name__icontains=search)
                ).filter(membership_valid_to__gte=datetime.date(now.year, now.month, now.day)).select_related('registration')

    return render(request, 'registrar/membership_report.html', {
        "reports": MembershipReport.objects.all,
        "years": years,
        'membership_person':membership_person,
        'membership_camper':membership_camper,
        })

@user_passes_test(readonly_check)
@login_required
def registrar(request):
    now=datetime.datetime.now()

    thisyear=get_thisyear(request)
    search=request.GET.get('q')
    email_sent=request.GET.get('email_sent')
    camponly=request.GET.get('camponly')
    memonly=request.GET.get('memonly')
    paid=request.GET.get('paid')
    registration_status_options=CampRegistrationStatus.objects.all()
    payment_form=PaymentForm()
    registrations_set=set({})
    registration_header_info={'total_owed':0, 
            'total_gross':0,
            'total_pp_fees':0,
            'outstanding':0,
            }

    campers=CampCamper.objects.filter(registration__year=thisyear).order_by('-pk').select_related('registration_type').select_related('registration').select_related('registration__registration_status').order_by('registration')

    if str(thisyear) != str(now.year):
        messages.error(request, "Filter applied: "+'"'+str(thisyear)+'"')
    if search:
        messages.error(request, "Filter applied: "+'"'+str(search)+'"')
        p("registrar search:",search)

        #get a queryset of objects that match the search term
        myfilter=(Q(first_name__icontains=search) |
               Q(last_name__icontains=search)|
               Q(registration__address1__icontains=search) |
               Q(registration__city__icontains=search) |
               Q(registration__id__icontains=search) |
               Q(registration__registration_status__status__icontains=search))

        campers=campers.filter(myfilter)

    #generate the total payments vs total outstanding for the table header
    myregistrations=CampRegistration.objects.filter(year=thisyear)

    sendmsg=False
    msg=set()
    if email_sent=="on":
        campers=campers.filter(registration__email_confirmation_sent=1)
        myregistrations=myregistrations.filter(email_confirmation_sent=1)
        sendmsg=True
        msg.add("email sent")
    if paid=="on":
        campers=campers.filter(registration__registration_status__in=REGISTRATION_PAID_STATUS)
        myregistrations=myregistrations.filter(registration_status__in=REGISTRATION_PAID_STATUS)
        sendmsg=True
        msg.add("paid")
    if camponly=="on":
        myregistrations=myregistrations.filter(registration_source=0)
        campers=campers.filter(registration__registration_source=0)
        sendmsg=True
        msg.add("camp only")
    if memonly=="on":
        myregistrations=myregistrations.filter(registration_source=1)
        campers=campers.filter(registration__registration_source=1)
        sendmsg=True
        msg.add("membership only")

    if sendmsg:
        messages.error(request, "Filter applied: "+", ".join(msg))


    for registration in myregistrations:
        registrations_set.add(registration.pk)
        if registration.cart_total:
            registration_header_info['total_owed']+=registration.cart_total

    all_payments=MembershipPayments.objects.filter(registration_id__in=registrations_set).select_related('membership_person')
    for payment in all_payments:
        if payment.gross_amt:
            registration_header_info['total_gross']+=payment.gross_amt
        if payment.paypal_fee:
            registration_header_info['total_pp_fees']+=payment.paypal_fee

    registration_header_info['outstanding']=registration_header_info['total_owed']-(registration_header_info['total_gross'])
    mycampers,registration_stats=generate_mycampers_dict(campers)

    return render(request,'registrar/registrar.html',{
            'mycampers':mycampers,
            'registration_status_options':registration_status_options,
            "reports": MembershipReport.objects.all,
            "years": years,
            "registration_header_info": registration_header_info,
            'PAYMENT_TYPES':PAYMENT_TYPES,
            "thisyear": thisyear,
            "paid":paid,
            "camponly":camponly,
            "memonly":memonly,
            "email_sent":email_sent,

            })

def generate_mycampers_dict(campers):
    #generate a list of dicts (indexed on registration_id) that's easier for Django to render in one pass without doing a ton of DB queries in the template.
    #also add a list of payments to the campers_object in the mypyments field

    mycampers={}
    registrations_set=set({})
    registration_stats={
            'tifd_memberships':0,
            'adult_campers':0,
            'child_campers':0,
            'confirmed_registration':0,
            'paid':0,
            }

    payments_thisyear=MembershipPayments.objects.all().order_by('id')
    payments_by_regid={}
    for payment in payments_thisyear:
        if payment.registration_id not in payments_by_regid.keys():
            payments_by_regid[payment.registration_id]=[]
        payments_by_regid[payment.registration_id].append(payment)

    for camper in campers:
        camper.mypayments_total=0
        if camper.registration.registration_source==0: 
            if camper.registration.email_confirmation_sent==1:
                registration_stats['confirmed_registration']+=1
            if camper.registration.registration_status_id in REGISTRATION_PAID_STATUS:
                registration_stats['paid']+=1
            if "child" in camper.adult_or_child:
                registration_stats['child_campers']+=1
            else:
                registration_stats['adult_campers']+=1
        else:
            registration_stats['tifd_memberships']+=1


        if camper.registration_id in payments_by_regid.keys():
            camper.mypayments=payments_by_regid[camper.registration_id] 
            for pmt in camper.mypayments:
                camper.mypayments_total+=pmt.gross_amt
        camper.due=camper.registration.cart_total-camper.mypayments_total

        registrations_set.add(camper.registration_id)

        #create a dict indexed by registration_id so the template can iterate through registration id, then campers
        if camper.registration_id not in mycampers.keys():
            mycampers[camper.registration_id]=[]
        mycampers[camper.registration_id].append(camper)

    p("generate_campers_dict returned:",mycampers)
    return mycampers,registration_stats


@require_http_methods(["POST"])
@user_passes_test(registrar_check)
@login_required
def registrar_update(request,registration_id):
    if request.POST:
        status=request.POST.get('status')
        payment=request.POST.get('payment')
        registration=CampRegistration.objects.get(pk=registration_id)
        p(registration_id,"registrar",request.user,"updated status from",registration.registration_status_id,"->",status)
        registration.registration_status_id=status
        registration.save()

    loop=0
    if request.GET.get('loop'):
        loop=request.GET.get('loop')

    if request.GET.get('return')=="home":
        return_to=reverse('registrar:homepage')
    else:
        return_to=reverse('registrar:registrar')+"#"+str(loop)

    return HttpResponseRedirect(return_to)

def donationletter_endpoint(request,registration_id):
    registration=CampRegistration.objects.get(pk=registration_id)
    return donationletter(request,registration,pdf_only=False,trigger=0)

def donationletter(request,registration,pdf_only=False,trigger=1):
    now=datetime.datetime.now()

    #trigger is a number above which the letter is generated

    campers=CampCamper.objects.filter(registration=registration).filter(adult_or_child__icontains="adult")
    itemizations=itemize_payment(registration)

    #payment_fields={
    #        't_shirt_fee':0,
    #        'dvd_fee':0,
    #        'camp_fee':0,
    #        'housing_fee':0,
    #        'other_fee':0,
    #        'refund_amt':0,
    #        'late_fee':0,
    #        'membership_fee':0,
    #        'bobbi_fund':0,
    #        'floor_fund':0,
    #        'music_fund':0,
    #        'general_fund':0,
    #        'camp_fund':0,
    #        }
    donation_fields={
            'membership_fee':0,
            'bobbi_fund':0,
            'chuck_fund':0,
            'camp_fund':0,
            'floor_fund':0,
            'music_fund':0,
            'general_fund':0,
            'camp_fund':0,
            }
    donations={}

    if now.year==2020:
        donation_fields['camp_fee']=0

    donations_total=0
    for key,val in itemizations.items():
        if key in donation_fields:
            #if val>0:
                donations[key]=val
                donations_total+=val

    #TODO pull these descriptions dynamically
    donations['Membership Dues']=donations.pop('membership_fee')
    donations['Bobbi Gillotti Scholarship Fund']=donations.pop('bobbi_fund')
    donations['In remembrence of Chuck Roth']=donations.pop('chuck_fund')
    donations['Texas Camp Fund']=donations.pop('camp_fund')
    donations['Floor Fund']=donations.pop('floor_fund')
    donations['Live Music Fund']=donations.pop('music_fund')
    donations['TIFD General Fund']=donations.pop('general_fund')
    if now.year==2020:
        donations['Virtual Camp 2020 Donation']=donations.pop('camp_fee')

    treasurer="Shirley Johnson, TIFD Treasurer"

    context={
            'donations': donations,
            'donations_total': donations_total,
            'registration': registration,
            'campers': campers,
            'treasurer': treasurer,
            }

    template="registrar/donationletter.html"

    if request and pdf_only is False:
            #return an HTTP response
            context['pdf_view']=True
            response = HttpResponse(content_type='application/pdf;')
            response['Content-Disposition'] = 'inline; filename=list_people.pdf'
            response['Content-Transfer-Encoding'] = 'binary'

            pdf=render_to_pdf(template, request, context,pdf_only=True)
            response.write(pdf)
            return response

    elif pdf_only is True:
        #return the PDF so we can attach it to email
        p("donations_total:",donations_total,"trigger:",trigger)
        if donations_total < trigger:
            return False
        else:
            context['pdf_view']=True
            pdf=render_to_pdf(template, request, context,pdf_only=True)
            return pdf
    else:
         return render(request,template, context)


def renew_tifd_membership(camper,save=True,thisyear=int(datetime.datetime.now().year)):

    """
        Take a CampCamper object and (optionally) renew their TIFD membership

        If the camper did not sign up for membership, that should be handled gracefully
            - a camp camper could already be a lifetime member
            - a membership "camper" could just be donating

        This also gets called by camp/signals.py when a paypal IPN is successfully processed

        returns two datetime objects describing how long the membership is good from and until.

        According to the TIFD board, membership is good from Thanksgiving day - Thanksgiving day
        If a membership is renewed is Jan-Oct, then "pro-rate" the membership so that it starts from the previous year.

    """
    now = datetime.datetime.now()
    form_open=CampDates.objects.get(slug='form_open').date
    p("form_open:",form_open,now.month)

    #if camp registration is open for the year, or camp has ended and it's still the same year (December) then registrations are for thisyear. Otherwise it's year-1
    if now.year!=form_open.year:
        startyear=thisyear-1
    elif (now.date() >= form_open):
        startyear=thisyear  # if month is 11 or 12 then start this year regardless of the form_open 
    elif (now.date()<form_open):  #if form_open is in the future, and it's early in the year, startyear is the previous year
        startyear=thisyear-1
    else:
        startyear=thisyear-1
    #(now,form_open,(now.date()>=form_open))
    camper_valid_to=None

    if not camper:
        #the membership sign up page needs to display the current renewal dates, so just spit them out
        valid_from=tday(startyear)
        valid_to=tday(startyear+1)
        return(valid_from,valid_to)


    p("inside renew_tifd_membership. save:",save, "startyear:",startyear," camper:",camper," years:",camper.membership_years," join tifd:",camper.join_tifd," regid", camper.registration_id, "join_tifd",camper.join_tifd,"regtype desc",camper.registration_type.description)
    if camper.join_tifd==1:
        if camper.membership_years is None:
            p("join TIFD is 1 but membership years is null or zero - this is probably a bug",camper.membership_years)
            raise Exception("join TIFD is 1 but membership years is null or zero")
            #c.membership_years=1

        valid_from=tday(startyear)
        valid_to=tday(startyear+camper.membership_years)
        p(f"valid_from:{valid_from} valid_to:{valid_to}")
        if "ifetime" in str(camper.registration_type.description):
            valid_to=tday(startyear+100)

        camper_valid_from=camper.membership_valid_from
        camper_valid_to=camper.membership_valid_to

        #make sure to only set a memership forward
        if camper_valid_to and ( camper_valid_to > valid_to.date() ):
                p("refusing to set a membership valid_to date backwards")
        elif camper_valid_to and (camper_valid_to == valid_to.date()):
                p("member",camper,"is already joined until",valid_to)

        else:
            p("renew membership for camper:",camper,"years:",camper.membership_years, "from:",valid_from, "until:",valid_to, "before from",camper.membership_valid_from, "before to:",camper.membership_valid_to)
            camper.membership_valid_from=valid_from
            camper.membership_valid_to=valid_to
            if save is True:
                if "No membership" not in camper.registration_type.description:
                    camper.save()
                else:
                    p("NOT SAVING - \"no membership\" not in camper.registration_type.description:",camper.registration_type.description,camper)

           #is this the correct thing to return here?  should camper.membership_valid_to be the source of truth?
    return camper.membership_valid_from,camper.membership_valid_to

@user_passes_test(registrar_check)
@login_required
def view(request,registration_id):
    campers=CampCamper.objects.filter(registration__exact=registration_id).order_by('adult_or_child','id')
    campers_list=campers.values()
    registration=CampRegistration.objects.get(pk=registration_id)
    payments_list=MembershipPayments.objects.filter(registration_id=registration_id).values()
    discount_list,discount_total=get_discount(registration_id)
    cart,cart_total=generate_cart_from_registration(registration_id,save=False)

    return render(request,'registrar/view.html',{
        'cart':cart,
        'discount_list':discount_list,
        'cart_total':cart_total,
        'campers':campers,
        'payments_list':payments_list,
        'registration':registration,
        'campers_list':campers_list,
        'registration_dict':registration.__dict__,
        })


@user_passes_test(registrar_check)
@login_required
def payments_quick(request,registration_id):
    registration=CampRegistration.objects.get(pk=registration_id)
    itemizations=itemize_payment(registration,payment=None)
    new_payment=MembershipPayments.objects.create()

    check_num=request.POST.get('qp_checknum')
    qp_total=request.POST.get('qp_total')

    new_payment.check_num=check_num
    new_payment.registration=registration

    gross_amt=0
    net_amt=0
    paypal_fee=0
    for key,val in itemizations.items():
         setattr(new_payment, key , val)
         if "paypal" not in key:
             net_amt+=val
         else:
             paypal_fee+=val
         gross_amt+=val

    #deal with registrar discounts
    if registration.adjustment:
        gross_amt+=registration.adjustment


    if Decimal(gross_amt) != Decimal(qp_total):
        p("ERROR - invalid quick payment! gross_amt:", gross_amt, "qp_total:",qp_total, "itemizations",itemizations)
        messages.error(request, f"ERROR - bad quick payment! gross_amt: {gross_amt} qp_total: {qp_total}")
        new_payment.delete()
        return HttpResponseRedirect(reverse('registrar:homepage'))
    new_payment.who_has_possession=str(request.user.first_name+ " " + str(request.user.last_name))
    new_payment.gross_amt=gross_amt
    new_payment.net_amt=net_amt
    new_payment.paypal_fee=paypal_fee
    new_payment.save()

    registration.registration_status_id=8
    registration.save()
    if registration.cart_total == new_payment.gross_amt:
        #approve automatically!  what could go wrong?
        p("automatically approving registration:", registration_id)
        approve_registration(request,registration)

    p(registration_id,request.user,"quick payment done id:",new_payment.id,"qp_total:",qp_total, "cart_total",registration.cart_total,"gross_amt:",gross_amt,"itemizations:",itemizations.items())
    if request.GET.get('return')=="home":
        return_to=reverse('registrar:homepage')
    else:
        return_to=reverse('registrar:registrar')
    return HttpResponseRedirect(return_to)

    
@user_passes_test(registrar_check)
@login_required
def campconstants(request):
    thisyear=get_thisyear(request)
    if request.method == "POST":
        form = CampConstantsForm(request.POST)
        if form.is_valid():
            p("form valid!")
            form.save()
            return redirect("registrar:campconstants")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request = request,
                          template_name = "registrar/campconstants.html",
                          context={"form":form})

    form=CampConstantsForm()
    #pull in the most recently added constants object ordered by id.  What could go wrong?

    last_constants=CampConstants.objects.order_by("-id")[0]
    p("last:",last_constants)

    form.fields['camp_start'].initial = last_constants.camp_start
    form.fields['form_open'].initial = last_constants.form_open
    form.fields['form_close'].initial = last_constants.form_close
    form.fields['form_late'].initial = last_constants.form_late

    p(last_constants.id, last_constants.form_open)

    thisyear=get_thisyear(request)
    
    from camp.views import get_active_housing_options,get_active_registration_options
    
    housing_options=get_active_housing_options()
    registration_options_adult=get_active_registration_options("adult")
    registration_options_child=get_active_registration_options("child")

    return render(request, 'registrar/campconstants.html', {
        "form":form,
        'thisyear':thisyear,
        "reports": MembershipReport.objects.all,
        "registration_options_adult":registration_options_adult,
        "registration_options_child":registration_options_child,
        "housing_options":housing_options,
            })

@user_passes_test(registrar_check)
@login_required
def refund(request,registration_id):
    now = datetime.datetime.now()
    thisyear=get_thisyear(request)
    payment=get_object_or_404(MembershipPayments, id=payment_id)
    p(request.user,"deleting payment",payment_id,payment.__dict__)
    if request.GET.get('return_to') == "payments":
        return_to="registrar:payments"
    payment.delete()
    if return_to:
        rev=reverse(return_to)+"?year="+str(thisyear)+"&ts="+str(now.microsecond)
        return HttpResponseRedirect(rev)

    rev=reverse('registrar:registrar')+"?year="+str(thisyear)+"&ts="+str(now.microsecond)
    return HttpResponseRedirect(rev)
