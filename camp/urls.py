from django.conf import settings
from django.urls import path
from django.contrib import admin
from django.conf.urls import include

from . import views


if settings.DEBUG:
    import debug_toolbar

app_name='camp'
urlpatterns = [
    path('', views.create, name='create'),
    #camp registration
        #/new/
        #/new/confirm/
        #/new/edit/  <--- an alias to confirm
        #/new/save/
    path('create/', views.create, name='create'),
    path('create/<int:registration_id>', views.create, name='create_edit'),
    path('delete/camper/<int:registration_id>', views.deletecamper, name='deletecamper'),
    path('delete/registration/<int:registration_id>', views.delete_entire_registration, name='delete_entire_registration'),
    path('donaterebate/<int:registration_id>', views.donaterebate, name='donaterebate'),
    path('confirm/<int:registration_id>', views.confirm, name='confirm'),
    path('final/<int:registration_id>', views.final, name='final'),
    path('final/', views.final, name='final'),
    path('status/<int:registration_id>', views.status, name='status'),
    path('checkpayment/<int:registration_id>', views.checkpayment, name='check_payment'),
    path('paypalpayment/<int:registration_id>', views.paypalpayment, name='paypal_payment'),
    path('paypalreturn/<int:registration_id>', views.paypalreturn, name='paypal_return'),
    path('test/500', views.my500, name='test_500'),
    path('help/', views.help, name='help'),
    path('check_membership/', views.check_membership, name='check_membership'),
    path('help/<slug>', views.help, name='help_slug'),
    path("view", views.homepage, name="homepage"),
    path("test", views.test, name="test"),
    path("test/", views.test, name="test"),
]

