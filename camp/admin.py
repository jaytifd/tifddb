from django.contrib import admin

from .models import *
from .forms import *

from simple_history.admin import SimpleHistoryAdmin

# Register your models here.


class Camper_childInline(admin.TabularInline):
    model=CampCamper_child
    extra=0
    search_fields = ['phone','first_name','last_name']
class Camper_adultInline(admin.TabularInline):
    model=CampCamper_adult
    extra=0
    search_fields = ['phone','first_name','last_name']

class MembershipPersonAdmin(admin.ModelAdmin):
    extra=0
    list_per_page = 100
    search_fields = ['first_name','last_name','member_year','email','email2','phone','notes']

class CampRegistrationAdmin(admin.ModelAdmin):
    #allows "save as new function"
    #save_as = True
    extra=0
    inlines = [Camper_adultInline,Camper_childInline]
    list_per_page = 100
    search_fields = ['registration_from_adult__first_name','registration_from_adult__last_name', 'year']

admin.site.register(CampRegistration,CampRegistrationAdmin)
admin.site.register(CampCamper_adult,SimpleHistoryAdmin)
admin.site.register(CampCamper_child,SimpleHistoryAdmin)
admin.site.register(CampPrices)
admin.site.register(CampHousingTypes)
admin.site.register(CampRegistrationTypes)
admin.site.register(CampRegistrationStatus)
admin.site.register(CampRebates)
admin.site.register(CampDates)
admin.site.register(CampShirtTypes)
admin.site.register(CampRegistrarInfo)
admin.site.register(CampTemplates)
admin.site.register(MembershipPerson,MembershipPersonAdmin)
admin.site.register(MembershipPayments,SimpleHistoryAdmin)



