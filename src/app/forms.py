from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Profile
        fields = ('phone', 'gender', 'birthday', 'newsletter', 'address_main', 'address_secondary')

