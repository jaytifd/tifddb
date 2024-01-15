from django import forms
from django.forms.models import inlineformset_factory
from .models import *
from django.forms import modelformset_factory, Textarea, TextInput, DateInput, RadioSelect, CheckboxInput, NumberInput

from ckeditor.widgets import CKEditorWidget

class DateInput(forms.DateInput):
    input_type = 'date'

class PaymentAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentAddForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class']='form-control'

        self.fields['cash'].widget.attrs['class']='checkboxinput '
        self.fields['gross_amt'].widget.attrs['readonly']=True
        self.fields['gross_amt'].widget.attrs['autocomplete']="off"
        self.fields['net_amt'].widget.attrs['readonly']=True
        self.fields['net_amt'].widget.attrs['autocomplete']="off"
        self.fields['date_recd'].widget.attrs['type']="date"
        self.fields['waiting_for_deposit'].widget.attrs['class']='checkboxinput '

    class Meta:
        model = MembershipPayments
        fields='__all__'
        #fields=['notes','deposit_date','date_recd','gross_amt','net_amt','cash','waiting_for_deposit']
        exclude=['membership_person',]
        widgets = {
            'notes': Textarea(attrs={'cols': 40, 'rows': 2}),
            'deposit_date': DateInput(),
            'date_recd': DateInput(),
            'gross_amt': TextInput(),
            'net_amt': TextInput(),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model=MembershipPayments
        #anything new here needs a field in the db too, and in camp_historicalmembershippayments
        fields=['date_recd','who_has_possession','payment_type','housing_fee','late_fee','t_shirt_fee','other_fee','chuck_fund','bobbi_fund','floor_fund','general_fund','camp_fund','music_fund','notes','gfc_linens'
                ]
        widgets = {
                'date_recd': DateInput(attrs={'type':'date'}),
                'housing_fee': NumberInput(attrs={'style': 'width: 5em;','step':'any','placeholder':'0.00'}),
                'late_fee': NumberInput(attrs={'style': 'width: 5em;','step':'any','placeholder':'0.00'}),
                'other_fee': NumberInput(attrs={'style': 'width: 5em;','step':'any','placeholder':'0.00'}),
                'bobbi_fund': NumberInput(attrs={'style': 'width: 5em;','step':'any','placeholder':'0.00'}),
                'chuck_fund': NumberInput(attrs={'style': 'width: 5em;','step':'any','placeholder':'0.00'}),
                'floor_fund': NumberInput(attrs={'style': 'width: 5em;','step':'any','placeholder':'0.00'}),
                'general_fund': NumberInput(attrs={'style': 'width: 5em;','step':'any','placeholder':'0.00'}),
                'music_fund': NumberInput(attrs={'style': 'width: 5em;','step':'any','placeholder':'0.00'}),
                't_shirt_fee': NumberInput(attrs={'style': 'width: 5em;','step':'any','placeholder':'0.00'}),
                'camp_fund': NumberInput(attrs={'style': 'width: 5em;','step':'any','placeholder':'0.00'}),
                'gfc_linens': NumberInput(attrs={'style': 'width: 5em;','step':'any','placeholder':'0.00'}),
        }

class ApproveRegistrationForm(forms.ModelForm):
    class Meta:
        model=CampRegistration
        fields=[
                'registration_status',
                'registrar_approval_note',
                ]
        widgets = {
                'registrar_approval_note':CKEditorWidget(),
        }
class CampConstantsForm(forms.ModelForm):
    class Meta:
        model = CampConstants
        fields='__all__'
        widgets = {
                'form_open': DateInput(),
                'form_close': DateInput(),
                'form_late': DateInput(),
                'camp_start': DateInput(),
                }

class MembershipPersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MembershipPersonForm, self).__init__(*args, **kwargs)

    class Meta:
        model=MembershipPerson
        fields='__all__'

MembershipPersonFormset=modelformset_factory(MembershipPerson,
                fields=[
                    'first_name',
                    'last_name',
                    'email',
                    'phone',
                    'membership_valid_from',
                    'membership_valid_to',
                    'membership_years',
                    'registration_type',
                    'gender',
                    ],
                form=MembershipPersonForm,
                #exclude=['transaction_id','session','paymenttype','registration_status','registrar_approval_note','adjustment'],
                extra=0,
                widgets = {
                #    'notes': Textarea(attrs={'cols': 40, 'rows': 5,}),
                },
                )


MembershipPersonFormset_inline = inlineformset_factory(CampRegistration, MembershipPerson,
                                            form=MembershipPersonForm,
                                            extra=0,
                                            widgets = {
                                            },
                                            fields=[
                                                'first_name',
                                                'last_name',
                                                'email',
                                                'phone',
                                                'registration_type',
                                                'membership_valid_from',
                                                'membership_valid_to',
                                                'gender',
                                                'membership_years',
                                                ],
                                            exclude=[
                                                ],
                                            )


