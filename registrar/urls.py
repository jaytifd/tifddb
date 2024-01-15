from django.urls import path
from django.contrib import admin
from django.conf.urls import include

from . import views

admin.site.site_header = 'Database Admin Panel'
admin.site.site_title = 'Database Admin Panel'


app_name='registrar'
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('reports', views.reports_home, name='reports_home'),
    path('docs', views.docs, name='docs'),
    path('payments', views.payments, name='payments'),
    path('payments/add', views.payments_add, name='payments_add'),
    path('payments/report', views.payments_report, name='payments_report'),
    path('payment/view/<int:payment_id>', views.payment_view, name='payment_view'),
    path('payment/ipn_view/<int:ipn_id>', views.ipn_view, name='ipn_view'),
    path('payments/delete/', views.payments_delete, name='payments_delete'),
    path('payments/delete/<int:payment_id>', views.payments_delete, name='payments_delete'),
    path('payments/edit/<int:payment_id>', views.payments_add, name='payments_add_edit'),
    path('payments/quick/<int:registration_id>', views.payments_quick, name='payments_quick'),
    path('registrar', views.registrar, name='registrar'),
    path('campconstants', views.campconstants, name='campconstants'),
    path('membership_report', views.membership_report, name='membership_report'),
    path('membership_report/<slug>', views.membership_report, name='membership_report'),
    path('registrar/update/<int:registration_id>', views.registrar_update, name='registrar_update'),
    path('adjustment/add', views.adjustment_add, name='adjustment_add'),
    path('approve/<int:registration_id>', views.approve, name='approve'),
    path('refund_report/', views.refund_report, name='refund_report'),
    path('refund/<int:registration_id>', views.refund, name='refund'),
    path('reports/<report_by_slug>', views.report_by_slug, name='reports_by_slug'),
    path('deposit', views.deposit, name='deposit'),
    path('donationletter/<int:registration_id>', views.donationletter_endpoint, name='donationletter'),
    path('view/<int:registration_id>', views.view, name='view'),
    path('renew', views.view, name='renew'),

]

