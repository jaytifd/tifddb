from django.forms import ModelForm, Form
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms import modelformset_factory, Textarea, TextInput, DateInput, RadioSelect, CheckboxInput, NumberInput
from django import forms
from camp.custom.mylogger import p
from .models import *

from localflavor.us.forms import USStateSelect, USZipCodeField

class RegistrationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['registration_source'].initial = 1   #0 = camp, 1=membership
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class']='form-control'

    class Meta:
        model = CampRegistration
        fields = '__all__'

regform_fields=['address1','address2','city','state','zip','country','donation_camp_fund','donation_chuck','donation_bobbi_gillotti','donation_floor_fund','donation_live_music','donation_tifd','camper_note','agreecheckbox','rebate','postmark','registration_source',]
RegistrationFormset_edit=modelformset_factory(CampRegistration,
                fields=regform_fields,
                form=RegistrationForm,
                #exclude=['transaction_id','session','paymenttype','registration_status','registrar_approval_note','adjustment'],
                extra=0,
                widgets = {
                    'state': USStateSelect(),
                    'postmark': DateInput(attrs={'type':'date'}),
                    'donation_tifd': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                    'donation_floor_fund': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                    'donation_camp_fund': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                    'donation_live_music': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                    'donation_bobbi_gillotti': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                             'donation_chuck': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                #    'notes': Textarea(attrs={'cols': 40, 'rows': 5,}),
                },
                )
RegistrationFormset_new=modelformset_factory(CampRegistration,
                fields=regform_fields,
                form=RegistrationForm,
                #exclude=['transaction_id','session','paymenttype','registration_status','registrar_approval_note','adjustment'],
                extra=1,
                widgets = {
                #    'address1': TextInput(attrs={'cols': 80, 'rows': 2}),
                    'state': USStateSelect(),
                    'donation_tifd': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                    'donation_floor_fund': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                    'donation_camp_fund': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                    'donation_live_music': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                    'donation_bobbi_gillotti': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                             'donation_chuck': NumberInput(attrs={'style': 'width: 7em;','step':'any','placeholder':'0.00','min':0}),
                    'postmark': DateInput(attrs={'type':'date'}),
                }
                )




class PersonForm(ModelForm):

    CHOICES = (
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            )
    membership_years=forms.ChoiceField(choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class']='form-control'

        self.fields['registration_type'].queryset = CampRegistrationTypes.objects.filter(active=True).filter(slug__exact="membership")
        self.fields['publish'].widget.attrs['class']='checkboxinput form-check-input'

        #THIS NEEDS TO BE THE DEFAULT CHOICE OR ALL THE HIDDEN FORMS WILL FAIL VALIDATION
        #
        self.fields['registration_type'].initial = 107
        self.fields['membership_years'].initial = "1"

    class Meta:
        model = CampCamper_adult
        fields = '__all__'
        prefix="registration_form_adult"

PersonFormset = inlineformset_factory(CampRegistration, CampCamper_adult,
                                            form=PersonForm,
                                            extra=7,
                                            widgets = {
                                            },
                                            fields=['first_name','last_name','email','phone','registration_type','membership_years','publish'],
                                            exclude=[
                                                ],
                                            )


