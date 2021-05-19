from django import forms
from pages.models import Player

class PlayerSearchForm(forms.Form):
    name = forms.CharField(label='Name', required=False)
    raze = forms.CharField(label='Raze', required=False)
    damage = forms.CharField(label='Damage', required=False)
    weakness = forms.CharField(label='Weakness', required=False)

    def get_players(self):
        data = self.cleaned_data
        filt = { 
            'ent__name' : data.get('name', None),
            'ent__raze' : data.get('raze', None),
            'ent__damage' : data.get('damage', None),
            'ent__weakness' : data.get('weakness', None)
        }
        filt = {k:v for k, v in data.items() if v is not None}
        all_players = (
            Player.objects
                .filter(**filt)
                .annotate(win_battles=Player.wins_battles())
                # .annotate(total_damage_caused=)
            )
        return all_players