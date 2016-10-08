from django.contrib import admin
from .models import *
from .forms import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id']
    form = UserProfileForm

class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id']
    form = OwnerForm

class RenterAdmin(admin.ModelAdmin):
    list_display = ['id']
    form = RenterForm

class CarAdmin(admin.ModelAdmin):
    list_display = ['id']
    form = CarForm


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id']
    form = TransactionForm

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Renter, RenterAdmin)
admin.site.register(Transaction, TransactionAdmin)
