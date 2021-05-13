from django import forms

class PlayerSearchForm(forms.Form):
    ent__name = forms.CharField(label='Name', required=False)
    ent__raze = forms.CharField(label='Raze', required=False)
    ent__damage = forms.CharField(label='Damage', required=False)
    ent__weakness = forms.CharField(label='Weakness', required=False)