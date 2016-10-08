from django import forms
from .models import *


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'


class RenterForm(forms.ModelForm):
    class Meta:
        model = Renter
        fields = '__all__'


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
