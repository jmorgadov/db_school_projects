from typing import Any, Dict
from django import forms
from django.contrib.auth import get_user_model
import re

UserModel = get_user_model()
import re

class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not (email and password):
            raise forms.ValidationError('Enter all the fields')

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise forms.ValidationError('Invalid email')

        if not user.check_password(password):
            raise forms.ValidationError('Wrong password')

        return cleaned_data

class RegisterForm(forms.Form):
    name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    nick = forms.CharField(required=True)
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)
    password_conf = forms.CharField(required=True)

    def clean_email(self):
        data = self.cleaned_data.get('email')

        if not re.match('.+@.+\..+', data):
            raise forms.ValidationError('Write a valid email')
        elif UserModel.objects.filter(email=data):
            raise forms.ValidationError('Email already taken')

        return data

    def clean_password_conf(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password_conf')

        if p1 != p2:
            raise forms.ValidationError('Password confirmation does not match')

        return p2

