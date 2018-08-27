from django import forms
from cProfile import label
from email import email
from django.forms.widgets import Widget
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class RegistrationForm(forms.Form):
    username = forms.CharField(label='tai khoan', max_length= 30)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='mat khau', Widget=forms.PasswordInput())
    password2 = forms.CharField(label='nhap lai mat khau', Widget=forms.PasswordInput())
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.clean_data['password1']
            password2 = self.clean_data['password2']
            if password1==password2 and password1:   
                return password2
            raise forms.ValidationError("Mat khau khong hop le")
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\W+$', username):
            raise forms.ValidationError("ten tai khoan co ky tu dac biet")
        try:
            User.objects.get(username==username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("tai khoan da ton tai")
    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'],
                                email=self.cleaned_data['email'],
                                password=self.cleaned_data['password1'])