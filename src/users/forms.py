from typing import Any, Dict
from django import forms
from django.contrib.auth import get_user_model
import re

from users.models import User

UserModel = get_user_model()
import re

class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=50,
        required=True
    )
    password = forms.CharField(
        required=True
    )

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not (email and password):
            raise forms.ValidationError('Enter all the fields')

        try:
            user: User = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise forms.ValidationError('Invalid email')

        if not user.check_password(password):
            raise forms.ValidationError('Wrong password')

        return cleaned_data

