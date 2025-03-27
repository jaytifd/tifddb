from django.http import HttpResponse, HttpResponseServerError, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.template import loader
from django.contrib import messages
from django.forms import modelformset_factory, Textarea, TextInput, DateInput, ValidationError, BooleanField
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.core import mail
from django.template.loader import render_to_string
from django.conf import settings
from django.template import Context, Template

from paypal.standard.forms import PayPalPaymentsForm

from .forms import *
from .models import *

import random
import string
import re
import datetime
import html2text
import logging

from .custom.mylogger import p

try:
    from .constants import linen_price,linen_price_decimal,dvd_price,dvd_price_decimal,membership_price,membership_price_decimal,shipping_price,shipping_price_decimal
except: pass

def my500(request):
    t = loader.get_template('camp/500.html')
    response = HttpResponseServerError(t.render())
    response.status_code = 500
    return response

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_client_ip(request):
    ip=""
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        pass
    return ip

def auth_check(request,registration_id):

        #return true if registration_id in the session, or if the user is in the "registrar" group
        try: request.session['registration']
        except KeyError: request.session['registration'] = []

        ip=get_client_ip(request)
        p(registration_id,"AUTH CHECK - registration_id:",registration_id, "session:",request.session['registration'], " path:", request.get_full_path(),"ip:",ip)
        session_registration=request.session['registration']

        if request.user.groups.filter(name__in=['registrar']).exists():
            p ('Registrar authenticated! registration_id',registration_id)
            return True
        elif request.user.groups.filter(name__in=['register_anytime']).exists():
            p ('Register anytime! registration_id',registration_id)
            return True
        elif registration_id in request.session['registration']:
            p ("Guest authenticated.",request.session['registration'])
            return True

        else: 
            p("auth failed. session:", request.session['registration'], " path:", request.get_full_path())
            return False

def get_list_of_registrations_from_session(request):

        try: request.session['registration']
        except KeyError: request.session['registration'] = []

        session_registration=request.session['registration']

        campers=CampCamper.objects.filter(registration__in=session_registration).order_by('-registration_id','pk')
        my_registration_dict={}
        for r in campers:
            if r.registration_id not in my_registration_dict.keys():
                my_registration_dict[r.registration_id]=[]
            my_registration_dict[r.registration_id].append(r)

        p("get list of registrations from session returned:",my_registration_dict)
        return my_registration_dict

def get_membership_info(first_name,last_name):
    modern_member=CampCamper.objects.filter(first_name__exact=first_name).filter(last_name__exact=last_name).exclude(membership_valid_to__exact=None).order_by("-membership_valid_to")[:1]
    legacy_member=MembershipPerson.objects.filter(first_name__exact=first_name).filter(last_name__exact=last_name).exclude(membership_valid_to__exact=None).order_by("-membership_valid_to")[:1]
    data={}

    if legacy_member:
        #if the legacy membership info is in the future
        #AND if it's farther ahead than the moderm record, spit it out
        #hopefully this is rare.
        #if (legacy_member[0].membership_valid_to > now.date()) and modern_member and legacy_member[0].membership_valid_to > modern_member[0].membership_valid_to:

        #if we have a legacy member and there is no modern member, return the legacy member
        #if we have both, only recturn legacy if membership_valid_to is greater than the modern member (should be rare)
        if not modern_member: p("no modern record found for", first_name, last_name)
        if modern_member and legacy_member[0].membership_valid_to > modern_member[0].membership_valid_to:
            p("older legacy record found for", first_name, last_name, "modern_valid", modern_member[0].membership_valid_to, "legacy valid", legacy_member[0].membership_valid_to)

        if (not modern_member) or (modern_member and legacy_member[0].membership_valid_to > modern_member[0].membership_valid_to):
            data['first_name']=legacy_member[0].first_name
            data['last_name']=legacy_member[0].last_name
            data['membership_valid_to']=legacy_member[0].membership_valid_to
            data['registration_source']=legacy_member[0].membership_type.membertype
            p("found legacy membership",legacy_member[0],legacy_member[0].id,legacy_member[0].registration_id,legacy_member[0].registration)
            return data,legacy_member

    if modern_member:
        data['first_name']=modern_member[0].first_name
        data['last_name']=modern_member[0].last_name
        data['membership_valid_to']=modern_member[0].membership_valid_to
        if modern_member[0].registration.registration_source==0:
            data['registration_source']="Texas Camp"
        else:
            data['registration_source']="Membership Renewal Form"

        p(f"found modern membership name:{modern_member[0]} id:{modern_member[0].id} regid:{modern_member[0].registration_id} reg:{modern_member[0].registration}")
        return data,modern_member

    else:
        p("get_membership_info returned nothing valid for",first_name,last_name)
        return data,modern_member
    return data,modern_member


def check_membership(request):

    if request.method == "POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        p("check membership query for",first_name,last_name)
        data,member=get_membership_info(first_name,last_name)
        if not data:
            data['failed_search']=True
            data['first_name']=first_name
            data['last_name']=last_name
            #messages.error(request, "Member not found!")

        return render(request,'camp/check_membership.html',{ 
            'data':data,
            })
    else:
        return render(request,'camp/check_membership.html',{ 
            }) 

def deletecamper(request,registration_id):
    if auth_check(request,registration_id) is not True: 
        return HttpResponse('<h1>Permission denied</h1>',status=403)

    camper_id=None
    if request.GET.get('delete_camper'):
        camper_id=int(request.GET.get('delete_camper'))
        mycamper=get_object_or_404(CampCamper,registration__exact=registration_id, pk=camper_id)
    if request.GET.get('delete_adult'):
        camper_id=int(request.GET.get('delete_adult'))
        mycamper=get_object_or_404(CampCamper,registration__exact=registration_id, pk=camper_id)
    if request.GET.get('delete_child'):
        camper_id=int(request.GET.get('delete_child'))
        mycamper=get_object_or_404(CampCamper,registration__exact=registration_id, pk=camper_id)
    registration_source=0

    if 'mycamper' in vars():
        registration_source=mycamper.registration.registration_source
        p("CAMPER DELETED:",camper_id,"reg source:",registration_source,mycamper.__dict__)
        mycamper.delete()
    else:
        p("CAMPER NOT FOUND! camper_id:",camper_id, " REG ID: ", registration_id)
    if registration_source==1:
        return HttpResponseRedirect(reverse('membership:create_edit',args=[registration_id]))
    else:
        return HttpResponseRedirect(reverse('camp:create_edit',args=[registration_id]))


def delete_entire_registration(request,registration_id):

    if auth_check(request,registration_id) is not True: 
        return HttpResponse('<h1>Permission denied</h1>',status=403)

    now = datetime.datetime.now()
    thisyear=request.GET.get('year') or str(now.year)

    myregistration=get_object_or_404(CampRegistration,pk=registration_id)
    mycampers=CampCamper.objects.filter(registration=registration_id)

    p("DELETE ENTIRE REGISTRATION CALLED for campers",mycampers," regid: ",registration_id)
    for c in mycampers:
        p("Deleted camper:",c.__dict__)
        try:
            c.delete()
        except:
            p("Camper delete dailed for ",c)

    p("Deleted registration:",myregistration.__dict__)
    myregistration.delete()

    return_url="%s?ts=%syear=%s" % (reverse('registrar:registrar'),now.microsecond,str(thisyear))
    return HttpResponseRedirect(return_url)


def donaterebate(request,registration_id):
    if auth_check(request,registration_id) is not True: 
        return HttpResponse('<h1>Permission denied</h1>',status=405)

    if request.method == "POST":

        registration=CampRegistration.objects.get(pk=registration_id)
        donationform = DonationForm(request.POST, instance=registration)
        rebateform = RebateForm(request.POST, instance=registration)
        campernotesform = CamperNotesForm(request.POST, instance=registration)
        safetypolicyform = SafetypolicyForm(request.POST, instance=registration)


        ##########################membership registration#######################
        if registration.registration_source==1: #0=camp, 1=membership
            #handle the membership registration differently - no safety form, no rebate form, just the donation form.
            if donationform.is_valid():
                if donationform.has_changed():
                    for c in donationform.changed_data:
                        p("[%s] DEBUG: donate form (membership) field %s went from \"%s\" to \"%s\"" % (str(registration_id),c,donationform[c].initial, donationform[c].data))
                donationform.save()
                generate_cart_from_registration(registration_id,save=True)
            else:
                if not donationform.is_valid():
                    messages.error(request, "Donation form error!")
                    p("donation form error (membership)",donationform.errors)

                    for field,message in donationform.errors.items():
                        messages.error(request, message)
                return HttpResponsePermanentRedirect(reverse('camp:confirm',args=[registration_id]))
            return HttpResponseRedirect(reverse('camp:final',args=[registration_id]))
        #########################################################################

        #######################camp registration#################################
        if ( donationform.is_valid() and rebateform.is_valid() and safetypolicyform.is_valid() and campernotesform.is_valid() ):
            p("All donation forms valid")
            if donationform.has_changed():
                for c in donationform.changed_data:
                    p("DEBUG: [%s] donate form field %s went from \"%s\" to \"%s\"" % (str(registration_id),c,donationform[c].initial, donationform[c].data))
                donationform.save()
            if rebateform.has_changed():
                for c in rebateform.changed_data:
                    p("DEBUG: [%s] rebate form field %s went from \"%s\" to \"%s\"" % (str(registration_id),c,rebateform[c].initial, rebateform[c].data))
                rebateform.save()
            if campernotesform.has_changed():
                for c in campernotesform.changed_data:
                    p("DEBUG: [%s] campernotesform form field %s went from \"%s\" to \"%s\"" % (str(registration_id),c,campernotesform[c].initial, campernotesform[c].data))
                campernotesform.save()
            if safetypolicyform.has_changed():
                for c in safetypolicyform.changed_data:
                    p("DEBUG: [%s] safetypolicy form field %s went from \"%s\" to \"%s\"" % (str(registration_id),c,safetypolicyform[c].initial, safetypolicyform[c].data))
                safetypolicyform.save()

                #change registration status
                registration.registration_status_id=2
                registration.save()

            #regenerate the shopping cart.
            generate_cart_from_registration(registration_id,save=True)

            if request.POST.get('finalreview')=='yes':
                return HttpResponseRedirect(reverse('camp:final',args=[registration_id]))
            else:
                #use permanent here to mitigate user hitting the back button wich would start a new registration.
                return HttpResponsePermanentRedirect(reverse('camp:confirm',args=[registration_id]))

        else:
            if not donationform.is_valid():
                messages.error(request, "Donation form error!")
                p("donation form error",donationform.errors)

                for field,message in donationform.errors.items():
                    p("message",dir(message),type(message),message)
                    p("donationrebate form error",message)
                    messages.error(request, message)

            if not rebateform.is_valid():
                messages.error(request, "Rebate form error!")
                p("rebateform form error",rebateform.errors)

                for field,message in rebateform.errors.items():
                    messages.error(request, message)

            if not safetypolicyform.is_valid():
                messages.error(request, "Safety policy form error! Please agree to the Safety Policy.")
                p("rebateform form error",safetypolicyform.errors)

                for field, message in safetypolicyform.errors.items():
                    messages.error(request, message)
            return HttpResponseRedirect(reverse('camp:confirm',args=[registration_id]))

def get_registrar_info(registration_source=0):  #0 = camp, 1 = membership.  Default to camp.
        #return the most recently added registrar info that's active
        registrar_info=CampRegistrarInfo.objects.filter(active=True).filter(registration_source=registration_source).order_by('-id')[0]
        p("registrar info found:",registrar_info.id,registrar_info)
        return registrar_info

def checkpayment(request,registration_id):
    if auth_check(request,registration_id) is not True: 
        return HttpResponse('<h1>Permission denied</h1>',status=421)

    previous_payments=None
    campers=CampCamper.objects.filter(registration__exact=registration_id).order_by('adult_or_child','id')
    registration=CampRegistration.objects.get(pk=registration_id)
    discount_list,discount_total=get_discount(registration_id)
    cart,cart_total=generate_cart_from_registration(registration_id)

    if registration.registration_status_id==6:
        return render(request,'camp/check_payment_error.html')

    registration.payment_type='check'
    registration.registration_status_id=4
    registration.save()
    previous_payments=MembershipPayments.objects.filter(registration=registration)
    payments_total=0

    #iterate through each of the payments and subtract payment from cart_total to get remaining balance
    remaining_balance=cart_total
    for payment in previous_payments:
        remaining_balance-=payment.gross_amt
        payments_total+=payment.gross_amt

    if registration.registration_source==1:
        registrar_info=get_registrar_info
        if not emailconfirmation(registration,request,template_slug="membership_received"):
            HttpResponseRedirect(reverse('camp:check_payment',args=(registration_id,)))
    else:
        registrar_info=get_registrar_info
        if not emailconfirmation(registration,request,template_slug="registration_received"):
            HttpResponseRedirect(reverse('camp:check_payment',args=(registration_id,)))

    p(registration_id,"CHECK EXIT:",registration_id)

    return render(request,'camp/check_payment.html',{
        'cart':cart,
        'discount_list':discount_list,
        'cart_total':cart_total,
        'campers':campers, 
        'registration':registration, 
        'registrar_info':registrar_info, 
        'previous_payments':previous_payments, 
        'payments_total':payments_total, 
        'remaining_balance':remaining_balance, 
        })

def paypalreturn(request,registration_id):
    if auth_check(request,registration_id) is not True: 
        return HttpResponse('<h1>Permission denied</h1>',status=421)

    campers=CampCamper.objects.filter(registration__exact=registration_id).order_by('adult_or_child','id')
    registration=CampRegistration.objects.get(pk=registration_id)
    discount_list,discount_total=get_discount(registration_id)
    cart,cart_total=generate_cart_from_registration(registration_id,save=False)
    previous_payments=MembershipPayments.objects.filter(registration=registration)
    remaining_balance=cart_total
    payments_total=0
    for payment in previous_payments:
        remaining_balance-=payment.gross_amt
        payments_total+=payment.gross_amt

    p("PayPal return to merchant registration_id:",registration_id)

    return render(request,'camp/paypal_return.html',{
        'campers':campers, 
        'cart':cart, 
        'previous_payments':previous_payments,
        'cart_total':cart_total, 
        'remaining_balance':remaining_balance, 
        'registration':registration, 
        })


def help(request,slug=None):
    if slug=="bg":
        return render(request,'camp/help-bg.html',{})
    if slug=="tifd":
        return render(request,'camp/help-tifd.html',{})
    if slug=="ff":
        return render(request,'camp/help-ff.html',{})
    if slug=="lm":
        return render(request,'camp/help-lm.html',{})
    if slug=="chuck":
        return render(request,'camp/help-chuck.html',{})
    return render(request,'camp/help.html',{})

def paypalpayment(request,registration_id):
    if auth_check(request,registration_id) is not True: 
        return HttpResponse('<h1>Permission denied</h1>',status=422)

    paypal_form=generate_paypal_form(registration_id,request)
    registration=CampRegistration.objects.get(pk=registration_id)

    if registration.registration_status_id==6:
        return render(request,'camp/check_payment_error.html')

    registration.payment_type='paypal'
    registration.registration_status_id=3
    registration.save()
    p("PAYPAL EXIT:",registration_id)

    #######
    #The paypal IPN system has been fast and reliable.. so sending a pre-confirmation email results in two emails right after one another.  
    #instead only email peple when the IPN comes in.

    #if people leave a registration without paying, there should be a different nag emailer function

    #if registration.registration_source==1:
    #    emailconfirmation(registration,request,template_slug="membership_received")
    #else:
    #    emailconfirmation(registration,request,template_slug="registration_received")

    return render(request,'camp/paypal_payment.html',{
        'paypal_form':paypal_form,
        'registration':registration,
        })


def final(request,registration_id):
    if auth_check(request,registration_id) is not True: 
        return HttpResponse('<h1>Permission denied</h1>',status=400)

    save=True
    if request.GET.get('ro'):
        p("final read only mode")
        save=False

    messages.success(request, "Please double check all your information.")
    campers=CampCamper.objects.filter(registration__exact=registration_id).order_by('adult_or_child','id')
    registration=CampRegistration.objects.get(pk=registration_id)
    discount_list,discount_total=get_discount(registration_id)
    cart,cart_total=generate_cart_from_registration(registration_id,save)

    #get the registration again because we generated the cart
    registration=CampRegistration.objects.get(pk=registration_id)

    paypal_form=generate_paypal_form(registration_id,request)

    return render(request,'camp/final.html',{
        'cart':cart,
        'discount_list':discount_list,
        'virtual_camp':virtual_camp,
        'cart_total':cart_total,
#        'donationform':donationform,
#        'rebateform':rebateform,
        'paypal_form':paypal_form,
        'campers':campers, 
        'registration':registration, 
        })

def get_discount(registration_id):

            campers=CampCamper.objects.filter(registration__exact=registration_id).order_by('adult_or_child','id')
            registration=CampRegistration.objects.get(pk=registration_id)
            discount_list=[]
            discount_total=0

            if registration.rebate_id and registration.rebate.price !=0:
                                          #exclude rebates that are 0
                rebate_dict={'cart_description':registration.rebate.cart_description,
                        'description':registration.rebate.description,
                        'price':registration.rebate.price,
                            }
                discount_list.append(rebate_dict)
            if registration.adjustment:
                adjustment_dict={'cart_description':'Registrar adjustment',
                        'description':'Registrar adjustment',
                        'price':registration.adjustment
                            }
                discount_list.append(adjustment_dict)

            for camper in campers:
                if camper.free_t_shirt:
                    p("adding free shirt for",camper)
                    free_shirt_dict={'cart_description':'Staff T-Shirt',
                            'description':'Staff T-Shirt',
                            'price':-camper.t_shirt_type.price
                                }
                    discount_list.append(free_shirt_dict)
                if camper.custom_registration_discount:
                    p("adding custom discount for",camper)
                    custom_discount_dict={'cart_description':'Staff Discount '+str(camper.first_name),
                            'description':'Staff Discount'+str(camper.first_name),
                            'price':-camper.custom_registration_discount
                                }
                    discount_list.append(custom_discount_dict)

            for discount in discount_list:
                discount_total+=discount['price']
                p(str(registration_id),"adding discount",discount['price'],"total",discount_total)

            p(str(registration_id),"discount_list",discount_list)
            return discount_list,discount_total


def generate_cart_from_registration(registration_id,save=True):
            """
            this takes a registration_id and genrates the shopping cart
            by iterating through all the campers and making a big dict with all their shirts, dvds
            donations, etc.

            shopping cart is a nested dict that looks like

            cart ['camper1_name'] = {'item_name':int(price) }
            cart ['camper2_name'] = {'item_name':int(price) }
            cart ['camper3_name'] = {
                                        'item1_name':int(price1), 
                                        'item2_name':int(price2), 
                                        }

            with this dict, we can (hopefully) do the following:

                1. draw a nice looking cart for the confirmation pages:
                    campername
                            item1 - price1
                            item2 - price2
                
                2. feed it to generate_paypal_form which will make a paypal form
                    item_1_name="John Smith - Private Cabin"
                    amount_1_value="60.00"

                3. used when generating a payment object from a registration
            """
            now=datetime.datetime.now()
            campers=CampCamper.objects.filter(registration__exact=registration_id).order_by('adult_or_child','id')
            p(registration_id,"inside generate_cart_from_registration - campers:",campers)
            registration=CampRegistration.objects.get(pk=registration_id)

            cart={}
            cart_total=0
            adjustment=0
            membership_fee_gross=0

            donations=CampRegistration.objects.filter(pk=registration_id).values('donation_tifd', 'donation_floor_fund', 'donation_floor_fund', 'donation_bobbi_gillotti', 'donation_live_music','donation_chuck')

            for donation in donations:
                for name,price in donation.items():
                    if (price  and price > 0):
                        verbose_name=CampRegistration._meta.get_field(name).verbose_name
                        if 'Donations' not in cart.keys():
                            cart['Donations']={}
                        cart['Donations'][verbose_name]=price

            for c in campers:
                name=c.first_name+" "+c.last_name
                cart[name]={}
                
                if c.housing_type_id:
                    housing_dict={c.housing_type.cart_description:c.housing_type.price}
                    cart[name].update(housing_dict)

                if c.registration_id:
                    #when this is a "membership" registration, the tifd membership fee is here because it's a "registration" type
                    if c.registration.registration_source == 1:  # 0=camp, 1=membership
                        if "ifetime" in c.registration_type.description:
                            desc=c.registration_type.cart_description
                            price=c.registration_type.price
                            c.membership_years=9999
                            p(registration_id,"setting member years to 9999")
                            membership_fee_gross+=price
                        else:
                            desc=c.registration_type.cart_description+" ("+str(c.membership_years)+" years)"
                            price=c.registration_type.price*c.membership_years
                            membership_fee_gross+=price

                    else:  #if tegistration source is not 1 (this is a camp registration)
                        #if c.custom_registration_price is not None and type (c.custom_registration_price) is Decimal:
                        if c.registration_type.id == 113:
                            p(registration_id,"custom registration price decimal",c.custom_registration_price)
                            desc=c.registration_type.cart_description
                            price=c.custom_registration_price
                        else:
                            desc=c.registration_type.cart_description
                            price=c.registration_type.price


                    registration_dict={desc:price}

                    ###don't show the free virtual camp option
                    #if c.registration_type.id == 110:
                    #    registration_dict={}

                    cart[name].update(registration_dict)

                if c.t_shirt_type_id:
                    if c.t_shirt_type_id != 1:   #1 is the "no shirt" option
                        shirtdict={c.t_shirt_type.cart_description:c.t_shirt_type.price}
                        cart[name].update(shirtdict)

                if c.dvd is True:
                    dvddict={dvd_price[0]['cart_description']:dvd_price_decimal}
                    cart[name].update(dvddict)

                ##IMPORTANT##
                ##
                #IF YOU ADD PRODUCT TO CART WORKFLOW
                #BE SURE AND ADD AN ENTRY FOR THIS IN REGISTRAR.VIEWS.itemize_payment!!
                #
                #############

                #add linen charge
                if c.need_linen is True:
                    linendict={linen_price[0]['cart_description']:linen_price_decimal}
                    cart[name].update(linendict)

                #automatically add the membership to the cart unless...
                if (c.adult_or_child=="adult" and c.join_tifd != 0 and c.registration.registration_source != 1):
                    membershipdict={membership_price[0]['cart_description']:membership_price_decimal}
                    cart[name].update(membershipdict)
                    membership_fee_gross+=membership_price_decimal

            late_date=CampDates.objects.get(slug='late_date').date
            late_fee=CampPrices.objects.get(slug='late_fee')

            if ((late_date < c.registration.created_at.date())):
                #only do a late fee if this is a camp registration and if they registered after the date
                if c.registration.registration_source == 0:
                    cart[late_fee.cart_description]={late_fee.cart_description:late_fee.price}
                    registration.late_fee=late_fee.price
            else:
                #reset it, in case the late fee is set for some reason like the date changes
                registration.late_fee=Decimal(0.00)

            #if the registration has a late_fee attached to the registration, show it.
            if c.registration.late_fee and c.registration.late_fee > 0:
                cart[late_fee.cart_description]={late_fee.cart_description:c.registration.late_fee}


            for person,cart_items in cart.items():
                for item,val in cart_items.items():
                    if val is None: val=0
                    cart_total+=val

            discount_list,discount_total=get_discount(registration_id)

            #discount_total should be a negative number
            p(registration.id,"cart total before discounts",cart_total,'discount_list',discount_list,'discount_total',discount_total, "cart:",cart, "save:",save)
            cart_total=cart_total+discount_total
            p(registration.id,"cart total after discounts",cart_total,'discount_list',discount_list,'discount_total',discount_total, "cart:",cart, "save:",save)

            registration.cart_total=cart_total
            registration.membership_fee_gross=membership_fee_gross

            ##don't save under... what conditions?  When looking at an old regustration probably
            if (registration.year==now.year) and save is True:
                p(registration.pk,"SAVING CART!")
                registration.save()

            return cart,cart_total
                
def generate_paypal_form(registration_id,request):
            now=datetime.datetime.now()
            registration=CampRegistration.objects.get(pk=registration_id)
            return_url="%s?ts=%s" % (reverse('camp:paypal_return',args=[registration_id]),now.microsecond)

            discount_list,discount_total=get_discount(registration_id)
            adjustment=0
            cart,cart_total=generate_cart_from_registration(registration_id,save=False)
            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "upload":1,
                "cmd":"_cart",
                "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                "return": request.build_absolute_uri(return_url),
                "cancel_return": request.build_absolute_uri(return_url),
                #paypal discount is calculated as a negative decimal - but paypal wants a positive one
                'discount_amount_cart': abs(discount_total),
                "currency_code": 'USD',
                "invoice": registration.transaction_id,
                "custom": registration.transaction_id,  # Custom command to correlate to some function later (optional)
            }
            i=2
            paypal_dict['item_name_1']="TIFD registration ID " + str(registration.transaction_id)
            paypal_dict['amount_1']="0" 
            for person,cart_items in cart.items():
                for item,val in cart_items.items():
                    if not re.search('/ebate/',item) and not re.search('djustment',item):
                        paypal_dict["item_name_"+str(i)]=person + " - " + item
                        paypal_dict["amount_"+str(i)]=val
                        i=i+1

            p(registration.pk,"paypal_dict",paypal_dict)
            paypal_form = PayPalPaymentsForm(initial=paypal_dict)
            return paypal_form

def confirm(request,registration_id):
    now=datetime.datetime.now()
    if auth_check(request,registration_id) is not True:
        return HttpResponse('<h1>Permission denied</h1>',status=402)
    else:
            campers=CampCamper.objects.filter(registration__exact=registration_id).order_by('adult_or_child','id')
            registration=CampRegistration.objects.get(pk=registration_id)
            p(registration.pk,"cart total before:",registration.cart_total)
            cart,cart_total=generate_cart_from_registration(registration_id)
            p(registration.pk,"cart total after:",registration.cart_total)
            discount_list,discount_total=get_discount(registration_id)

    camp_start=CampDates.objects.get(slug='camp_start').date
    p(registration_id,"drawing registration confirm page. registration_id: ", registration_id)
    donationform=DonationForm(instance=registration)
    rebateform=RebateForm(instance=registration)
    safetypolicyform=SafetypolicyForm(instance=registration)
    campernotesform=CamperNotesForm(instance=registration)

    if virtual_camp:
        safety_agreement=CampTemplates.objects.get(slug__exact='safety_agreement_virtual_camp').template_text
    else:
        safety_agreement=CampTemplates.objects.get(slug__exact='safety_agreement').template_text

    nextyear=now.year+1
    return render(request,'camp/confirm_registration.html',{
        'cart':cart,
        'safety_agreement':safety_agreement,
        'discount_list':discount_list,
        'cart_total':cart_total,
        'donationform':donationform,
        'camp_start':camp_start,
        'camp_end':camp_start+datetime.timedelta(days=3),
        'safetypolicyform':safetypolicyform,
        'rebateform':rebateform,
        'nextyear':nextyear,
        'campernotesform':campernotesform,
        #'paypal_form':paypal_form,
        'campers':campers, 
        'registration':registration, 
        })


def generate_email_html(registration,template_slug):
    #returns html_body

    now=datetime.datetime.now()
    campers=CampCamper.objects.filter(registration=registration).order_by('adult_or_child','id')
    registrar_info=get_registrar_info()
    cart,cart_total=generate_cart_from_registration(registration.id)
    discount_list,discount_total=get_discount(registration.id)
    email_header_template=CampTemplates.objects.get(slug__exact=template_slug).template_text
    email_subject_template=CampTemplates.objects.get(slug__exact=template_slug).subject
    p(registration.pk,"generate email html subject",email_subject_template,"template slug:",template_slug)
    p(registration.pk,"generate email html header",email_header_template,"template slug:",template_slug)

    header_tpl = Template(email_header_template)
    subject_tpl = Template(email_subject_template)

    if registration.registrar_approval_note and now.year > 2020:
        intro_message=registration.registrar_approval_note
    else:
        intro_message=header_tpl.render(Context(dict(now=now, registrar_info=registrar_info)))
        try:
            if registration.payment_type == "check":
                intro_message = intro_message + "\n<p>Check or money order for camp fees can be mailed to:</p>\n<pre>\n" + str(registrar_info.name) + "\n" + str(registrar_info.mailing_address) + "\n</pre>\n"
        except:
            pass

    #intro_message=header_tpl.render(Context(dict(now=now, registrar_info=registrar_info)))
    subject=subject_tpl.render(Context(dict(now=now, registrar_info=registrar_info)))

    html_body=render_to_string('camp/check_payment.html',{
        'email_view':True,
        'cart':cart,
        'discount_list':discount_list,
        'cart_total':cart_total,
        'campers':campers, 
        'registration':registration, 
        'registrar_info':registrar_info, 
        })
    
    everything=intro_message+html_body

    email_content={'everything':everything,
            'intro_message':intro_message,
            'html_body':html_body,
            'subject':subject,
            'registrar_info':registrar_info,
            }

    return (email_content)


def emailconfirmation(registration,request,template_slug):
    now=datetime.datetime.now()
    campers=CampCamper.objects.filter(registration=registration).order_by('adult_or_child','id')
    email_content=generate_email_html(registration,template_slug)
    #intro_message=email_content['intro_message']
    html_body=email_content['everything']
    subject=email_content['subject']

    to=[]
    for camper in campers:
        to.append(camper.email)

    connection = mail.get_connection()
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_body=text_maker.handle(html_body)

    if campers[0].registration.registration_source==0 and now.year > 2020:
        from_email="Texas Camp " + str(now.year) + " registration " + "<camp-registration@tifd.org>"
    else:
        from_email="TIFD registrar <registrar@tifd.org>"

    reply_to = ["registrar@tifd.org"]
    bcc=["registrar@tifd.org"]

    #for address in to:
    email = EmailMultiAlternatives(
            subject, 
            text_body,   ##careful this is a positional arg
            from_email, 
            to,
            bcc=bcc,
            reply_to=reply_to,
            connection=connection,

            )
    email.attach_alternative(html_body,'text/html')

    ######DONATION LETTER#######
    from registrar.views import donationletter

    #only send PDF if the registration is paid - i.e. if this is a confirmation email
    p(registration.pk,"donation letter - checking registration status:",registration.registration_status.id)
    if registration.registration_status.id in REGISTRATION_PAID_STATUS:
        p(registration.pk,"donation letter - checking registration status - pass")
        #the donation letter will return false if the amount is less than the trigger
        pdf=donationletter(request,registration,pdf_only=True)
        if pdf:
            #https://stackoverflow.com/questions/1633109/creating-a-mime-email-template-with-images-to-send-with-python-django
            #save the pdf to a tmp file and attach. 
            filename="TIFD donation receipt "+str(now.year)+" - "+str(registration.id) +".pdf"
            p(registration.pk,"PDF filename",filename)
            with open(filename,'wb') as output:
                output.write(pdf)
                output.flush()
            p(registration.pk,"attaching donation receipt PDF: ",output.name)
            email.attach_file(output.name)
        else:
            p(registration.pk,"donationletter returned false - donation less than $50")

    p(registration.id," sending email to",to)
    try:
        if not settings.DEBUG:
            email.send()
        else:
            if request:
                messages.warning(request, "Email not sent in debug mode")
            p(registration.pk,"email sending disabled in DEBUG MODE")

    except Exception as e:
        msg="ERROR sending confirmation email.  Try reloading the page.  If this continues please contact registrar@tifd.org"
        messages.error(request, msg)
        messages.error(request, e)
        p(registration.pk,"email send failure - exception:",e)
        return False
    return True

#@login_required
def homepage(request):

        try: request.session['registration']
        except KeyError: request.session['registration'] = []

        p("current session registration:",request.session['registration'])
        session_registration=request.session['registration']
        adults=CampCamper.objects.filter(registration__in=session_registration).order_by('-registration_id','pk')
        my_registration_dict={}
        for r in adults:
            if r.registration_id not in my_registration_dict.keys():
                my_registration_dict[r.registration_id]=[]
            my_registration_dict[r.registration_id].append(r)

        p(my_registration_dict)
        return render(request,'camp/view_registrations.html',{'registrations':my_registration_dict})

def get_active_housing_options():
    housing_options=CampHousingTypes.objects.filter(active=True)
    return housing_options

def get_active_registration_options(adultorchild):
    if adultorchild is None or adultorchild == "both".lower():
       return CampRegistrationTypes.objects.filter(active=True).filter(slug__exact="registration")
    return CampRegistrationTypes.objects.filter(adult_or_child__iexact=adultorchild).filter(active=True).filter(slug__exact="registration")

#this is hit fix ajax when the paypal link is clicked
def status(request,registration_id):
    if auth_check(request,registration_id) is not True: 
        return HttpResponse('<h1>Permission denied</h1>',status=400)

    p(registration_id,"PayPal AJAX status check/change action=",request.GET.get('action'),"status=",request.GET.get('status'))
    if request.GET.get('action')=="change":
        if ((request.GET.get('status')=="3") or (request.GET.get('status')==3)) :
                registration=CampRegistration.objects.get(pk=registration_id)

                registration.registration_status_id=3
                registration.payment_type='paypal'
                registration.save()
                p(registration_id,"registration status changed to Waiting for Paypal (3) via AJAX",registration.pk,registration)
                return HttpResponse(status = 200)
    else:
        p(registration_id,"Status change error")
        raise
        return HttpResponse(status = 500)


def create(request,registration_id=None):
    now=datetime.datetime.now()

    ################################  DANGER ############################################
    ##  membership:create and camp:create are MOSTLY the same.  If you make a change here
    ## it should probably be made in both places!
    #####################################################################################

    save_success=False
    late_after=CampDates.objects.get(slug='late_date').date
    camp_start=CampDates.objects.get(slug='camp_start').date
    form_open=CampDates.objects.get(slug='form_open').date
    form_close=CampDates.objects.get(slug='form_close').date

    edit_view=False
 
    if (auth_check(request,500) is False):
        if ((form_open > now.date()) or (form_close < now.date())):
            #allow registrar access to the closed form
            p ("form closed", form_open, form_close, now.date() )
            return  render(request,'camp/camp_closed.html',{
                'thisyear':now.year,
                })

    if registration_id is None:
        current_registrations=get_list_of_registrations_from_session(request)
        p('no registration_id - current registrations in session:',current_registrations)
    else: current_registrations = None

    housing_options=get_active_housing_options()
    registration_options_adult=get_active_registration_options("adult")
    registration_options_child=get_active_registration_options("child")

    if registration_id:
        if auth_check(request,registration_id) is True:
             registration=CampRegistration.objects.get(pk=registration_id)
             edit_view=True
             registrationform = RegistrationFormset_edit(queryset=CampRegistration.objects.filter(pk=registration_id))
             p(registration_id,'Edit view access granted, regid:',registration_id)

        else:
            msg="Registration id "+str(registration_id) + " access denied "
            messages.add_message(request, 40, msg)
            p(registration_id,"Registration ID but not authenticated")
            return HttpResponseRedirect(reverse('camp:create'))
    else:
        p("new view - no registration ID")
        registration_id=None
        registration=CampRegistration()
        registrationform = RegistrationFormset_new(queryset=CampRegistration.objects.filter(pk=registration_id))
 


    p("Create view, initializing the registration forms") 
    regformform_adult=RegistrationFormset_adult(instance=registration,queryset=CampCamper.objects.filter(adult_or_child__iexact="adult"))
    regformform_child=RegistrationFormset_child(instance=registration,queryset=CampCamper.objects.filter(adult_or_child__iexact="child"))

    if request.method == 'POST':
        registrationform=RegistrationFormset_edit(request.POST,form_kwargs={'empty_permitted': True})
        regformform_adult=RegistrationFormset_adult(request.POST,instance=registration,form_kwargs={'empty_permitted': True})
        regformform_child=RegistrationFormset_child(request.POST,instance=registration,form_kwargs={'empty_permitted': True})

        p ("registrationform has changed",registrationform.has_changed())
        p ("camper_adult has changed",regformform_adult.has_changed())
        p ("camper_child has changed",regformform_child.has_changed())

        if regformform_child.has_changed():
            for form in regformform_child:
                if form.has_changed():
                    i=1
                    for c in form.changed_data:
                        p ("[%s] child #%d form field %s went from \"%s\" to \"%s\"" % (str(registration_id),i,c,form[c].initial, form[c].data))
                    i=i+1

        if regformform_adult.has_changed():
            for form in regformform_adult:
                
                if form.has_changed():
                    i=0
                    for c in form.changed_data:
                        p("[%s] adult #%d form field %s went from \"%s\" to \"%s\"" % (str(registration_id),i,c,form[c].initial, form[c].data))
                    i=i+1



        if ( registrationform.is_valid() and regformform_adult.is_valid()) and regformform_child.is_valid() :
            p ("DEBUG: all forms valid!\n")

            #check to see if either the base (address) form, of the first camper is empty.  If so, fail.
            #but DON'T fail if this is a user editing their existing form.
            if edit_view is False:
            #the following only detects *changes* so if you are editing and don't change anything it will fail
                if (registrationform[0].cleaned_data == {} or regformform_adult[0].cleaned_data == {}):
                    p ("The first form of a formset should not be empty!")
                    if registrationform[0].cleaned_data == {}:
                        msg="ERROR: Address form was left blank"
                        messages.add_message(request, 40, msg)
                        p (msg)
                    if regformform_adult[0].cleaned_data == {}:
                        msg="ERROR: Camper #1 form was left blank"
                        messages.add_message(request, 40, msg)
                        p(msg)
                    for m in regformform_adult.errors:
                        p ("mmessage",m)
                        messages.error(request, m)
                    
                    #reload the form and give the user a chance to fix whatever before anything is saved
                    #hopefully the messages are useful.
                    p("re-rendering the regform to correct for errors")

                    return render(request,'camp/registration_form.html',{ 
                        'virtual_camp':virtual_camp,
                        'housing_options':housing_options,
                        'late_after':late_after,
                        'camp_start':camp_start,
                        'registration_options_adult':registration_options_adult,
                        'registration_options_child':registration_options_child,
                        'registrationform': registrationform,
                        'dvd_price': dvd_price,
                        'linen_price': linen_price_decimal,
                        'registration': registration, ##used in template only
                        'regformform_child': regformform_child,
                        #'housing_options': housing_options,
                        #'registrationoptions': registrationoptions,
                        #'rebates': rebates,
                        'regformform_adult': regformform_adult,
                        }) 

                p('DEBUG: Blank form check - PASS')

            ####BASE FORM SAVED HERE#####
            #All good!?  Save the registration now to obtain the PK
            #hopefully all the errors have been caught, otherwise there will be a lot of duplicates.
            newregistration=registrationform.save(commit=False)
            if edit_view is True:
                registration_pk=registration_id

            #if there are no changes to the regform, this won't get triggered.
            for l in newregistration:
                    p ("Registration form saved",dir(l))
                    l.save()
                    registration_pk=l.pk

                    #this is messy - keying the transaction id off date and PK is a good idea, but we have to save the form twice.  
                    #once to get the PK, and once to save the transaction_id.
                    l.transaction_id=str(now.year)+str(registration_pk)
                    l.save()


            registration=CampRegistration.objects.get(pk=registration_pk)
            #re-init the camper forms here otherwise the below fails because django thinks the base regform has not been saved yet
            regformform_adult=RegistrationFormset_adult(request.POST,instance=registration)
            regformform_child=RegistrationFormset_child(request.POST,instance=registration)

            #Could these checks possibly fail?  
            if ( regformform_adult.is_valid() and regformform_child.is_valid() ):
                saved=regformform_adult.save(commit=False)
                for r in saved:
                        print("r",r)
                        r.save()
                        p ("save adult form",r)
                saved=regformform_child.save(commit=False)
                for r in saved:
                        #set the child housing option here.
                        #r.housing_id=1
                        r.save()
                        p ("save child form",r)
                messages.success(request, "Saved Successfully! Please continue and fill out the second page.")

                #add the registration to the session so user can come back later
                session_registrations=[]
                if request.session.get('registration'):
                    session_registrations=request.session['registration']

                session_registrations.append(registration_pk)
                p(registration.pk,"Form saved - registration_id", registration_pk, " setting session to",session_registrations)
                request.session['registration']=session_registrations
                save_success=True
            else:
                if not regformform_adult.is_valid():
                    p ("regformform_adult not valid", (regformform_adult.errors))
                    for m in regformform_adult.errors:
                        messages.error(request, m)
                    i=0
                if not regformform_child.is_valid():
                    p ("regformform_child not valid", (regformform_child.errors))
                    for m in regformform_child.errors:
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
            if not regformform_adult.is_valid():
                p ("regformform_adult not valid", (regformform_adult.errors))
                for m in regformform_adult.errors:
                    p ("mmessage:",m)
                    messages.error(request, m)
                i=0
                for r in regformform_adult:
                        p (r.changed_data)
                        for c in r.changed_data:
                            p ("DEBUG: [%s] Adult #%d form field %s went from \"%s\" to \"%s\"" % (str(registration.pk),i,c,r[c].initial, r[c].data))
                        i=i+1
            if not regformform_child.is_valid():
                p ("regformform_child not valid", (regformform_child.errors))
                for m in regformform_child.errors:
                    messages.error(request, m)
                i=0
                for r in regformform_child:
                        p (r.changed_data)
                        for c in r.changed_data:
                            p ("DEBUG: [%s] Child #%d form field %s went from \"%s\" to \"%s\"" % (str(registration.pk),i,c,r[c].initial, r[c].data))
                        i=i+1

            p ("FORM ERROR")

    if save_success is True:
        p(registration.pk,"save_success - redirect to confirm page",request.META) 
        #if virtual_camp:
        #   return HttpResponseRedirect(reverse('camp:final', args=(registration_pk,)))
        #else:
        return HttpResponseRedirect(reverse('camp:confirm', args=(registration_pk,)))

    p("rendering the base form") 
    return render(request,'camp/registration_form.html',{ 
        'virtual_camp':virtual_camp,
        'housing_options':housing_options,
        'late_after':late_after,
        'camp_start':camp_start,
        'camp_end':camp_start+datetime.timedelta(days=3),
        'registration_options_adult':registration_options_adult,
        'registration_options_child':registration_options_child,
        'registrationform': registrationform,
        'dvd_price': dvd_price,
        'linen_price': linen_price_decimal,
        'current_registrations': current_registrations,
        'housing_options': housing_options,
        'registration': registration, ##used in template only
        #'registrationoptions': registrationoptions,
        #'rebates': rebates,
        'regformform_child': regformform_child,
        'regformform_adult': regformform_adult,
        }) 


def test(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
             p("valid!", form.cleaned_data)
             l=form.save()
             p("after save", l)
             return True
    else:
        form = RegistrationForm()


    return render(request,'camp/test.html',{ 
           'form':form,

                                            })
