from paypal.standard.models import ST_PP_COMPLETED, ST_PP_REFUNDED, ST_PP_REVERSED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.shortcuts import get_object_or_404
from .models import *
from membership.models import *
from .custom.mylogger import p
from registrar.views import itemize_payment
from registrar.views import renew_tifd_membership
from camp.views import emailconfirmation
from registrar.views import donationletter

now = datetime.datetime.now()

def invalid_ipn(sender, **kwargs):
    p("invalid ipn!")
    return

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    p('IPN Initial hello',(ipn_obj),ipn_obj.payment_status,ipn_obj.first_name,ipn_obj.last_name,ipn_obj.payer_email,ipn_obj.mc_gross,ipn_obj.mc_fee,ipn_obj.reason_code,ipn_obj.txn_id)
    if ipn_obj.payment_status == ST_PP_REVERSED:
        p("Here inside REVERSED IPN",ipn_obj,"invoice",ipn_obj.invoice,type(ipn_obj.invoice),ipn_obj.mc_gross)
        #no code here to handle this yet
        return false

    elif ipn_obj.payment_status == ST_PP_REFUNDED:
        p("Here inside REFUND IPN1",ipn_obj,"invoice",ipn_obj.invoice,type(ipn_obj.invoice),ipn_obj.mc_gross)
        if ( ipn_obj.receiver_email != "jay-facilitator@spaz.org" and ipn_obj.receiver_email != 'payments@tifd.org'):
            p('PayPal callback had wrong receiver email:',ipn_obj.receiver_email)
            return False
        r2=CampRegistration.objects.get(transaction_id=ipn_obj.invoice)
        p("Here inside REFUND IPN2.2",ipn_obj,"r2",r2,"invoice",ipn_obj.invoice)
        registration = get_object_or_404(CampRegistration, transaction_id=ipn_obj.invoice)
        p("Here inside REFUND IPN2",ipn_obj,"registration",registration,"invoice",ipn_obj.invoice)
        if registration:
            p("Here inside REFUND IPN3",ipn_obj,"registration",registration)
            mypayment=MembershipPayments.objects.get(registration_id=registration.pk)

            ##BE CAREFUL python will refuse to += None type with strings or decimals
            if mypayment:
                if mypayment.refund_amt:
                    mypayment.refund_amt=mypayment.refund_amt+abs(ipn_obj.mc_gross)
                else:
                    mypayment.refund_amt=abs(ipn_obj.mc_gross)
                    #refunds are stored as positive decimals

                mypayment.paypal_fee+=ipn_obj.mc_fee  #mc_fee is negative
                mypayment.gross_amt+=ipn_obj.mc_gross #mc_gross is negative
                mypayment.net_amt=mypayment.gross_amt-mypayment.paypal_fee
                newnote="\nPayment refunded via PayPal at %s total:%0.2f id:%d txn:%s\n" % (now.strftime('%Y-%m-%d %H:%M:%S'),ipn_obj.mc_gross,ipn_obj.id,ipn_obj.txn_id)
                if mypayment.notes:
                    mypayment.notes=mypayment.notes+newnote
                else:
                    mypayment.notes=newnote

                registration.registration_status_id=11 # 11 = refunded
                registration.save()
                mypayment.save()
                p("Here inside REFUND PAYMENT SAVED..",ipn_obj,"registration",registration,"payment",mypayment,"paymentid",mypayment.pk,"refund:",ipn_obj.mc_gross)
                return True

        else:
            return False


    elif ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ( ipn_obj.receiver_email != "jay-facilitator@spaz.org" and ipn_obj.receiver_email != 'payments@tifd.org'):
            p('PayPal callback had wrong receiver email:',ipn_obj.receiver_email)
            # Not a valid payment
            return False
        if ipn_obj.payment_status == 'Completed':
            #https://developer.paypal.com/docs/ipn/integration-guide/IPNandPDTVariables/
            #mc_fee Transaction fee associated with the payment. mc_gross minus mc_fee equals the amount deposited into the receiver_email

            # payment was successful
            p("Incoming PayPal callback - looking for invoice number:",ipn_obj.invoice)

            #registration = get_object_or_404(CampRegistration, transaction_id=ipn_obj.invoice)

            #We also want to accept "anonymous" donations via paypal - i.e. those that are not tied to a registration
            #since everything is keyed off registrations, just assign these payments to registration #1 which is a reg specifically created for this purpose.

            try:
                registration = CampRegistration.objects.get(transaction_id=ipn_obj.invoice)
            except:
                #if this is not a camp/membership registration accept the payment anyways, woohoo!
                registration = CampRegistration.objects.get(pk=1)

            p("Incoming PayPal callback - invoice number:",ipn_obj.invoice, "registration:",registration)

            #create the payment object
            payment=MembershipPayments(
                    gross_amt=ipn_obj.mc_gross,
                    net_amt=(ipn_obj.mc_gross-ipn_obj.mc_fee),
                    paypal_fee=ipn_obj.mc_fee,
                    payment_type=3,
                    waiting_for_deposit=1,
                    who_has_possession='PP',
                    date_recd=now.strftime('%Y-%m-%d'),
                    pp_ipn_name=(str(ipn_obj.first_name) + " " + str(ipn_obj.last_name)),
                    pp_ipn_email=str(ipn_obj.payer_email),
                    pp_ipn_phone=str(ipn_obj.contact_phone),
                    pp_ipn_txn_id=str(ipn_obj.txn_id),
                    pp_ipn_id=int(ipn_obj.id),
                    registration_id=registration.id,
                    )
            payment.save()
            p('PayPal callback received! Payment recorded: status=IPN valid, invoice=', ipn_obj.invoice, " gross=",ipn_obj.mc_gross, "cart total",registration.cart_total, "registration_id",registration.pk, "payment_id",payment.pk)

            #update the registration

            ###### DONTAION ONLY -- NO CAMP/MEMBERSHIP REGISTRATON ###########
            if registration.pk==1:
                p("PayPal IPN registration 1 - anonymous donation payment_id:",payment.id,"ipn_id:",ipn_obj.id,"item name:",ipn_obj.item_name)
                #this is the anonymous donation registration
                if ipn_obj.item_name=="Virtual Camp 2020":
                    p("PayPal IPN registration 1 - anonymous donation - ", payment.gross_amt, "sent to camp_fee")
                    payment.camp_fee=payment.gross_amt

                elif ipn_obj.item_name=="Texas Camp Fund":
                    p("PayPal IPN registration 1 - anonymous donation - ", payment.gross_amt, "sent to camp_fund")
                    payment.camp_fund=payment.gross_amt

                elif ipn_obj.item_name=="General Fund":
                    p("PayPal IPN registration 1 - anonymous donation - ", payment.gross_amt, "sent to general_fund")
                    payment.general_fund=payment.gross_amt

                elif ipn_obj.item_name=="Bobbi Gillotti Scholarship Fund":
                    p("PayPal IPN registration 1 - anonymous donation - ", payment.gross_amt, "sent to bobbi_fund")
                    payment.bobbi_fund=payment.gross_amt

                elif ipn_obj.item_name=="Donation in remembrance of Chuck Roth":
                    p("PayPal IPN registration 1 - anonymous donation - ", payment.gross_amt, "sent to chuck_fund")
                    payment.chuck_fund=payment.gross_amt

                elif ipn_obj.item_name=="Texa-Kolo":
                    p("PayPal IPN registration 1 - anonymous donation - ", payment.gross_amt, "sent to texakolo1")
                    payment.texakolo_fund=payment.gross_amt

                elif "KOLO" in ipn_obj.item_name:
                    p("PayPal IPN registration 1 - anonymous donation - ", payment.gross_amt, "sent to texakolo2")
                    payment.texakolo_fund=payment.gross_amt

                elif ipn_obj.item_name=="Live Music Fund":
                    p("PayPal IPN registration 1 - anonymous donation - ", payment.gross_amt, "sent to music_fund")
                    payment.music_fund=payment.gross_amt

                elif ipn_obj.item_name=="Floor Fund":
                    p("PayPal IPN registration 1 - anonymous donation - ", payment.gross_amt, "sent to floor_fund")
                    payment.floor_fund=payment.gross_amt

                else:
                    p("PayPal IPN - no fund found for item_name:",ipn_obj.item_name,"sending ", payment.gross_amt, "to general fund. payment_id:",payment.id,"ipn_id:",ipn_obj.id)
                    payment.general_fund=payment.gross_amt

                payment.save()
                p("final donation:",payment.__dict__)

                #set the trigger low, always send out a donation receipt here

                #this should probably get moved to cron.. because if any of this fails paypal will keep re-sending the IPN and create a bunch of new payments
                pdf=donationletter("",registration,pdf_only=True,trigger=1)
                if pdf:
                    template="donation_confirmed"
                    p("mailing out donation letter for regid",registration.id)
                    request=''
                    if not emailconfirmation(registration,request,template):
                        p("EMAIL SEND FAILED donation letter signals.py regid:",registration.id)
                return True



            #### CAMP / MEMBERSHIP REGISTRATION FULLY PAID #######
            elif registration.cart_total == ipn_obj.mc_gross:


                #Step 0, save the registration 
                registration.registration_status_id = 6
                registration.paypal_fee = ipn_obj.mc_fee
                registration.paypal_gross = ipn_obj.mc_gross
                registration.save()
                #registration.payment = ipn_obj.mc_gross - ipn_obj.mc_fee
                #registration.save()
                #add ipn_obj.invoice, ipn_obj.first_name, ipn_obj.last_name, ipn_obj.payer_email ipn_obj.contact_phone  ipn_obj.payer_status
                p("PayPal callback received! Finished updating registration status. registration_id:",registration.pk, "status:",registration.registration_status, "payment_id:",payment.pk)


                #Step 1, itemize the payment
                payment_fields=itemize_payment(registration);
                for key,val in payment_fields.items():
                    setattr(payment, key, val)
                payment.save()
                p("PayPal callback received! Finished itemizing payment.  registration_id:",registration.pk, "status:",registration.registration_status, "payment_id:",payment.pk, "payment_fields",payment_fields)

                #Step 3 - process membership renewals and send confirmation emails
                campers=CampCamper.objects.filter(registration=registration).filter(adult_or_child__iexact="adult")
                for c in campers:
                    #set the memvership info in the database
                    r=renew_tifd_membership(c)

                    #if a membership is renewed, automatically send out the membership details... but only for TIFD memberships?
                    if r:
                        if registration.registration_source==0:
                            template="registration_approved"
                        else:
                            template="membership_confirmed"
                        request=""
                        if not emailconfirmation(c.registration,request,template):
                            p("email confirmation failed regid:",c.registration.id)
                            return false
                        else:
                            registration.email_confirmation_sent=1
                            registration.save()

                #everything succeeded, it was a miracle!
                return True

            #######CAMP / MEMBERSHIP REGISTRATION __NOT__ FULLY PAID
            elif registration.cart_total != ipn_obj.mc_gross:
                p('PayPal callback received! Cart total was not equal to payment. invoice=', ipn_obj.invoice, " gross=",ipn_obj.mc_gross, "cart total",registration.cart_total, "registration_id",registration.pk, "payment_id",payment.pk)
                # mark the order as non paid
                registration.registration_status_id = 7
                registration.paypal_fee = ipn_obj.mc_fee
                registration.paypal_gross = ipn_obj.mc_gross
                registration.save()
                return False
            else:
                p("PayPal IPN else fallthrough. returning false")
                return False
    else: 
        p("IPN failed to auth. Status:", ipn_obj.payment_status)
        return False

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.

        # Undertake some action depending upon `ipn_obj`.
        #if ipn_obj.custom == "premium_plan":
        #    price = ...
        #else:
        #    price = ...
#
#        if ipn_obj.mc_gross == price and ipn_obj.mc_currency == 'USD':
#            ...
#    else:
#        pass
#        #...

valid_ipn_received.connect(show_me_the_money)
invalid_ipn_received.connect(show_me_the_money)
