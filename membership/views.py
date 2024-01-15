from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.template import loader
from django.contrib import messages

from decimal import Decimal
import datetime

from registrar.views import renew_tifd_membership

from camp.views import generate_cart_from_registration
from camp.views import get_discount,  emailconfirmation, generate_email_html
from camp.views import create as campcreate
from camp.views import auth_check
from camp.models import *
from camp.custom.mylogger import p
from camp.custom.tday import tday

try:
    from camp.constants import dvd_price_decimal,membership_price_decimal
except: pass

from .forms import *
from .models import *

years = CampRegistration.objects.order_by('-year').values('year',).distinct()
now = datetime.datetime.now()


def create(request,registration_id=None):

    ###################  WARNING ##############################
    ##  membership:create and camp:create are MOSTLY the same.  
    #If you make a change here, it should probably be made in both places!
    ######################################################################
    save_success=False
    edit_view=False
    renewid=None
    registration_options=CampRegistrationTypes.objects.filter(active=True).filter(slug__exact="membership")

    if request.GET.get('renewid'):
        renewid=request.GET.get('renewid')
        renewid=int(renewid)
        p('RENEW:',(renewid),type(renewid))

    
    membership_valid_from,membership_valid_to=renew_tifd_membership(None,False)
    p("Example membership renewal facts begin/end",membership_valid_from,membership_valid_to)

    if registration_id:
        if auth_check(request,registration_id) is True:
             registration=CampRegistration.objects.get(pk=registration_id)
             edit_view=True
             registrationform = RegistrationFormset_edit(queryset=CampRegistration.objects.filter(pk=registration_id))
             p('Edit view access granted, regid:',registration_id)

        else:
            msg="Registration id "+str(registration_id) + " access denied "
            messages.add_message(request, 40, msg)
            #registration_id=None
            #registration=Registration()
            p ("Registration ID but not authenticated")
            return HttpResponseRedirect(reverse('camp:create'))
    else:
        registration_id=None
        registration=CampRegistration()
        registrationform = RegistrationFormset_new(queryset=CampRegistration.objects.filter(pk=registration_id))


    #regformform_person=PersonFormset(instance=registration,initial=[{'email': "blah"}])
    regformform_person=PersonFormset(instance=registration)

    #after we have built the forms, do the renewal stuff
    if (renewid) and (renewid > 0) and (auth_check(request,registration_id) is True):
        p("setting up the form from renew id ",renewid)
        old_registration=CampRegistration.objects.get(pk=renewid)
        registrationform = RegistrationFormset_new(queryset=CampRegistration.objects.filter(pk=registration_id))

        copy_fields=(
                'address1',
                'address2',
                'city',
                'state',
                'zip',
                'country',
                )
        for f in copy_fields:
            registrationform[0].fields[f].initial=getattr(old_registration, f)
        oldcampers=CampCamper.objects.filter(registration=renewid)

        copy_fields=(
                'first_name',
                'last_name',
                'phone',
                'email',
                )
        i=0
        for oldcamper in oldcampers:
            for f in copy_fields:
                a=getattr(oldcamper,f)
                p(f'setting form #{i} {f} -> {a}')
                regformform_person[0].fields[f].initial=getattr(oldcamper,f)
            i=i+1

        #for key,val in registrationform[0].fields.items():
        #    p(key,val)

    if request.method == 'POST':
        registrationform=RegistrationFormset_edit(request.POST,form_kwargs={'empty_permitted': True})
        regformform_person=PersonFormset(request.POST,instance=registration,form_kwargs={'empty_permitted': True})

        if regformform_person.has_changed():
            for form in regformform_person:
                if form.has_changed():
                    for c in form.changed_data:
                        p("[%s] adult form field %s went from \"%s\" to \"%s\"" % (str(registration.pk),c,form[c].initial, form[c].data))



        if ( registrationform.is_valid() and regformform_person.is_valid()):
            p ("DEBUG: all forms valid!\n")

            #check to see if either the base (address) form, of the first camper is empty.  If so, fail.
            #but DON'T fail if this is a user editing their existing form.
            if edit_view is False:
            #the following only detects *changes* so if you are editing and don't change anything it will fail
                if (registrationform[0].cleaned_data == {} or regformform_person[0].cleaned_data == {}):
                    p ("The first form of a formset should not be empty!")
                    if registrationform[0].cleaned_data == {}:
                        msg="ERROR: Address form was left blank"
                        messages.add_message(request, 40, msg)
                        p (msg)
                    if regformform_person[0].cleaned_data == {}:
                        msg="ERROR: Camper #1 form was left blank"
                        messages.add_message(request, 40, msg)
                        p (msg)
                    for m in regformform_person.errors:
                        p ("m",m)
                        messages.error(request, m)

                    
                    #reload the form and give the user a chance to fix whatever before anything is saved
                    #hopefully the messages are useful.
                    p("re-rendering the regform to correct for errors")
                    return render(request,'membership/registration_form.html',{ 
                        'membership_valid_from':membership_valid_from,
                        'membership_valid_to':membership_valid_to,
                        'registration_options':registration_options,
                        'registrationform': registrationform,
                        'registration': registration, ##used in template only
                        #'registrationoptions': registrationoptions,
                        #'rebates': rebates,
                        'regformform_person': regformform_person,
                        }) 

                p('DEBUG: Blank form check - PASS')


            ####BASE FORM SAVED HERE#####


            #All good!?  Save the registration now to obtain the PK
            #hopefully all the errors have been caught, otherwise there will be a lot of duplicates.
            newregistration=registrationform.save(commit=False)
            #p ("newregis",dir(registrationform))
            #p ("newregis2",(registrationform.has_changed()))
            if edit_view is True:
                registration_pk=registration_id

            #if there are no changes to the regform, this won't get triggered.
            for l in newregistration:
                    p ("Registration form saved",dir(l))
                    l.save()
                    registration_pk=l.pk

                    #this is messy - keyig the transaction id off date and PK is a good idea, but we have to save the form twice.  
                    #once to get the PK, and once to save the transaction_id.
                    l.transaction_id=str(now.year)+str(registration_pk)
                    l.save()


            registration=CampRegistration.objects.get(pk=registration_pk)
            #re-init the camper forms here otherwise the below fails because django thinks the base regform has not been saved yet
            regformform_person=PersonFormset(request.POST,instance=registration)

            #Could these checks possibly fail?  
            if regformform_person.is_valid() :
                saved=regformform_person.save(commit=False)
                for r in saved:
                        r.save()
                        p ("save adult form",r)
                messages.success(request, "Saved Successfully! Registration ID: "+str(registration_pk))

                #add the memnuid_id to the session so user can come back later
                session_registrations=[]
                if request.session.get('registration'):
                    session_registrations=request.session['registration']

                session_registrations.append(registration_pk)
                p("Form saved - registration_id", registration_pk, " setting session to",session_registrations)
                request.session['registration']=session_registrations
                save_success=True
            else:
                if not regformform_person.is_valid():
                    p ("regformform_person not valid", (regformform_person.errors))
                    for m in regformform_person.errors:
                        messages.error(request, m)
                    i=0
                p("regform adult or child not valid - second pass")

        else:
            if not registrationform.is_valid():
                p ("registration not valid", (registrationform.errors))
                for m in registrationform.errors:
                    messages.error(request, m)
                i=0
                for r in registrationform:
                        p (r.changed_data)
                        for c in r.changed_data:
                            p ("DEBUG: [%s] BASE form field %s went from \"%s\" to \"%s\"" % (str(registration.pk),c,r[c].initial, r[c].data))
                        i=i+1
            if not regformform_person.is_valid():
                p ("regformform_person not valid", (regformform_person.errors))
                for m in regformform_person.errors:
                    p ("message:",m)
                    messages.error(request, m)
                i=0
                for r in regformform_person:
                        for c in r.changed_data:
                            p ("DEBUG: [%s] Adult #%d form field %s went from \"%s\" to \"%s\"" % (str(registration.pk),i,c,r[c].initial, r[c].data))
                        i=i+1

            p ("FORM ERROR")

    if save_success is True:
        p("save_success - redirect to confirm page") 
        return HttpResponseRedirect(reverse('camp:confirm', args=(registration_pk,)))

    p("rendering the base form") 
    p("reg options",registration_options)
    return render(request,'membership/registration_form.html',{ 
        'registrationform': registrationform,
        'registration': registration, ##used in template only
        'membership_valid_from':membership_valid_from,
        'membership_valid_to':membership_valid_to,
        'registration_options': registration_options,
        #'rebates': rebates,
        'regformform_person': regformform_person,
        }) 

def help(request,slug=None):
    return render(request,'membership/help.html',{})


