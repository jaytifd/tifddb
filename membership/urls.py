from django.urls import path
from django.contrib import admin
from django.conf.urls import include

from . import views

admin.site.site_header = 'Database Admin Panel'
admin.site.site_title = 'Database Admin Panel'

app_name='membership'

urlpatterns = [
    path("", views.create, name="create"),
    path('<int:registration_id>', views.create, name='create_edit'),
    path('help/', views.help, name='help'),
    path("create/", views.create, name="create"),
    path('create/<int:registration_id>', views.create, name='create_edit')
]

