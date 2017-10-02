from django import forms
from .models import MapEntity
from django.contrib.auth.models import User;
from django.contrib.auth.forms import *
from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget
from django.contrib.auth.hashers import make_password

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", min_length=5)
    password = forms.CharField(label="Password", min_length=5, widget=forms.PasswordInput, )

class EventForm(ModelForm):
    class Meta:
        model = MapEntity
        # fields = ['entityName' ,'entityType', 'entityDescription', 'startDate', 'endDate']
        fields = ['entityName' ,'entityType', 'entityDescription']
        widgets = {
            #Use localization and bootstrap 3
            # 'startDate': DateTimeWidget(attrs={'id':"dateTimeId"}, bootstrap_version=3),
            # 'endDate': DateTimeWidget(attrs={'id':"dateTimeId"}, bootstrap_version=3)
        }

    locLat = forms.FloatField(widget=forms.HiddenInput())
    locLong = forms.FloatField(widget=forms.HiddenInput())

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username' ,'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        # Then call the clean() method of the super  class
        cleaned_data = super(RegisterForm, self).clean()
        password = self.cleaned_data.get('password')
        if len(password) < 6 :
            raise forms.ValidationError("Passwords have to be over 6 characters")            

        return cleaned_data
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        if commit:
            user.save()
        return user
