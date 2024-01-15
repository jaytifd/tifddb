from django.forms import ModelForm, Form
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms import modelformset_factory, Textarea, TextInput, DateInput, RadioSelect, CheckboxInput, NumberInput
from .models import CampPrices
from django import forms
from .custom.mylogger import p

from .models import *


from localflavor.us.forms import USStateSelect, USZipCodeField


#convoluted, but also robust in case someone adds more than one t-shirt price
#shirtprice=CampPrices.objects.filter(slug__exact="shirt").values()
#shirtprice_decimal=shirtprice[0]['price']

try:
    from .constants import dvd_price,dvd_price_decimal,shipping_price,shipping_price_decimal
except: pass

#convoluted, but also robust in case someone adds more than one dvd price
#dvdprice=CampPrices.objects.filter(slug__exact="dvd").values()
#dvdprice_decimal=dvdprice[0]['price']


class RegistrationForm(ModelForm):
    #state = USStateSelect()
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class']='form-control'

    class Meta:
        model = CampRegistration
        fields = '__all__'

regform_fields=['address1','address2','city','state','zip','country','donation_chuck','donation_bobbi_gillotti','donation_camp_fund','donation_floor_fund','donation_live_music','donation_tifd','camper_note','agreecheckbox','rebate','postmark']
RegistrationFormset_edit=modelformset_factory(CampRegistration,
                fields=regform_fields,
                form=RegistrationForm,
                #exclude=['transaction_id','session','paymenttype','registration_status','registrar_approval_note','adjustment'],
                extra=0,
                widgets = {
                    #'state': USStateSelect(),
                    'postmark': DateInput(attrs={'type':'date'}),
                #    'notes': Textarea(attrs={'cols': 40, 'rows': 5,}),
                },
                )
RegistrationFormset_new=modelformset_factory(CampRegistration,
                fields=regform_fields,
                form=RegistrationForm,
                #exclude=['transaction_id','session','paymenttype','registration_status','registrar_approval_note','adjustment'],
                extra=1,
                widgets = {
                   #'address1': TextInput(attrs={'cols': 80, 'rows': 2}),
                    #'state': USStateSelect(),
                    'postmark': DateInput(attrs={'type':'date'}),
                }
                )


class RegistrationForm_adult(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm_adult, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class']='form-control'

        self.fields['publish'].widget.attrs['class']='checkboxinput form-check-input'
        self.fields['band'].widget.attrs['class']='checkboxinput form-check-input'
        self.fields['mobility'].widget.attrs['class']='checkboxinput form-check-input'
        self.fields['certification'].widget.attrs['class']='checkboxinput form-check-input'
        self.fields['medical'].widget.attrs['class']='checkboxinput form-check-input'
        self.fields['staff'].widget.attrs['class']='checkboxinput form-check-input'
        self.fields['need_linen'].widget.attrs['class']='checkboxinput form-check-input'
        self.fields['free_t_shirt'].widget.attrs['class']='checkboxinput form-check-input'
        self.fields['dvd'].widget.attrs['class']='checkboxinput form-check-input'
        self.fields['dvd'].label = self.fields['dvd'].label + " ($" + str(dvd_price_decimal)+")"
        self.fields['join_tifd'].widget.attrs['class']='checkboxinput form-check-input'

    class Meta:
        model = CampCamper_adult
        fields = '__all__'
        prefix="registration_form_adult"

class RegistrationForm_child(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm_child, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class']='form-control'

        self.fields['band'].widget.attrs['class']='checkboxinput form-check-input'
        self.fields['family_program'].widget.attrs['class']='checkboxinput form-check-input'
        self.fields['need_linen'].widget.attrs['class']='checkboxinput form-check-input'

    class Meta:
        model = CampCamper_child
        fields = '__all__'
        #html_name='asdaasdsdd'
        prefix="registration_form_child"


class DonationForm(ModelForm):
    class Meta:
        model = CampRegistration
        fields = [
                'donation_bobbi_gillotti',
                'donation_floor_fund',
                'donation_camp_fund',
                'donation_live_music',
                'donation_tifd',
                'donation_chuck',
                ]
        widgets = {
                'donation_tifd': NumberInput(attrs={'style': 'width: 4em;','step':'any','placeholder':'0.00','min':0}),
                'donation_floor_fund': NumberInput(attrs={'style': 'width: 4em;','step':'any','placeholder':'0.00','min':0}),
                'donation_camp_fund': NumberInput(attrs={'style': 'width: 4em;','step':'any','placeholder':'0.00','min':0}),
                'donation_live_music': NumberInput(attrs={'style': 'width: 4em;','step':'any','placeholder':'0.00','min':0}),
                'donation_bobbi_gillotti': NumberInput(attrs={'style': 'width: 4em;','step':'any','placeholder':'0.00','min':0}),
                'donation_chuck': NumberInput(attrs={'style': 'width: 4em;','step':'any','placeholder':'0.00','min':0}),
        }
        prefix="donation"

class RebateForm(ModelForm):
    class Meta:
        model = CampRegistration
        fields = ['rebate',]
        widgets = {
            #'donation_bobbi_gillotti': NumberInput(attrs={'style': 'width: 4em;'}),
        }
        prefix="rebate"
        rebate=CampRebates.objects.all().exclude(slug='legacy')
    def __init__(self, *args, **kwargs):
        super(RebateForm, self).__init__(*args, **kwargs)
        self.fields['rebate'].queryset = CampRebates.objects.all().exclude(slug='legacy')


class CamperNotesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CamperNotesForm, self).__init__(*args, **kwargs)
        self.fields['camper_note'].label = "Notes, questions, or comments for the registrar:"
    class Meta:
        model = CampRegistration
        fields = ['camper_note',]
        widgets = {
                'camper_note': Textarea(attrs={'rows': '4','class':'form-control'}),
        }
        prefix="camper_note"


#class AgreeField(forms.NullBooleanField):
#    #def to_python(self, value):
#    #    """Normalize data to a list of strings."""
#    #    # Return an empty list if no input was given.
#    #    if not value:
#    #        return []
#    #    return value.split(',')
#
#    def validate(self, value):
#        """Check if value consists only of valid emails."""
#        # Use the parent's handling of required fields, etc.
#        super().validate(value)
#        p("agreefield: ",value)
#        if value is not True:
#            raise forms.ValidationError("Sorry, you must agree to the safety policy before attending camp.")

class SafetypolicyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SafetypolicyForm, self).__init__(*args, **kwargs)
        self.fields['agreecheckbox'].label = "I have read and understood the above statement."
        #self.fields['agreecheckbox'].help_text = "I have read and understood the above statement."
        self.fields['agreecheckbox'].required = True
    class Meta:
        model = CampRegistration
        fields = ['agreecheckbox',]
        widgets = {
            #'donation_bobbi_gillotti': NumberInput(attrs={'style': 'width: 4em;'}),
        }
        prefix="agree"


RegistrationFormset_adult = inlineformset_factory(CampRegistration, CampCamper_adult,
                                            form=RegistrationForm_adult, 
                                            extra=4,
                                            widgets = {
                                                'diet_details': Textarea(attrs={'cols': 40, 'rows': 1,}),
                                                'first_name': TextInput(attrs={'cols': 80, 'rows': 2,'omplete':"off"}),
                                            },
                                            fields='__all__',
                                            exclude=[
                                                'family_program',
                                                'adult_or_child', #<---- set automatically in the model definition
                                                ],
                                            )


#housing_id should be blank for child, but can't be blank for adult.
RegistrationFormset_child = inlineformset_factory(CampRegistration, CampCamper_child,
                                            form=RegistrationForm_child, 
                                            extra=5,
                                            widgets = {
                                                'diet_details': TextInput(attrs={'cols': 80, 'rows': 2,'autocomplete':"off"}),
                                                'age': NumberInput(attrs={'cols': 4,'style':'-moz-appearance: textfield; -webkit-appearance: none; margin:0;' }),
                                            },
                                            fields=[
                                                'first_name',
                                                'last_name',
                                                'age',
                                                'gender',
                                                'band',
                                                'instruments',
                                                'diet',
                                                'registration_type',
                                                'diet_details',
                                                't_shirt_type',
                                                'need_linen',
                                                'family_program',
                                                ]

                                            )



class ManagementForm(Form):
    """
    Keep track of how many form instances are displayed on the page. If adding
    new forms via JavaScript, you should increment the count field of this form
    as well.
    """
    def __init__(self, *args, **kwargs):
        self.base_fields[TOTAL_FORM_COUNT] = IntegerField(widget=HiddenInput)
        self.base_fields[INITIAL_FORM_COUNT] = IntegerField(widget=HiddenInput)
        # MIN_NUM_FORM_COUNT and MAX_NUM_FORM_COUNT are output with the rest of
        # the management form, but only for the convenience of client-side
        # code. The POST value of them returned from the client is not checked.
        self.base_fields[MIN_NUM_FORM_COUNT] = IntegerField(required=False, widget=HiddenInput)
        self.base_fields[MAX_NUM_FORM_COUNT] = IntegerField(required=False, widget=HiddenInput)
        super().__init__(*args, **kwargs)


from paypal.standard.forms import PayPalPaymentsForm
from django.utils.html import format_html
class TIFDPayPalPaymentsForm(PayPalPaymentsForm):

    def __init__(self, *args, **kwargs):
        super(PayPalPaymentsForm, self).__init__(*args, **kwargs)

    def render(self):
        return format_html(u"""<form action="{0}" method="post">
    {1}
    <input type="image" src="{2}" name="submit" alt="Buy it Now" />
</form>""", self.get_login_url(), self.as_p(), self.get_image())

