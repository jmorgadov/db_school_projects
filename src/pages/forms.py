from django import forms
from django.db.models.base import Model
from django.db.models.query import QuerySet
from pages.models import Player
from pages.models import Beast
from pages.models import Spell

class PlayerSearchForm(forms.Form):
    name = forms.CharField(label='Name', required=False)
    raze = forms.CharField(label='Raze', required=False)
    damage = forms.CharField(label='Damage', required=False)
    weakness = forms.CharField(label='Weakness', required=False)
    count = forms.CharField(label='Count', required=False)
    order_by = forms.CharField(label='Order by', required=False)
    reverse = forms.BooleanField(label='Reverse', required=False)

    order_by_map = {
        "name": "ent__name",
        "raze": "ent__raze",
        "damage": "ent__damage",
        "weakness": "ent__weakness",
        "win_battles": "win_battles",
        "total_damage_caused": "total_damage_caused"
    }

    def get_players(self):
        data = self.cleaned_data
        filt = { 
            'ent__name' : data.get('name', None),
            'ent__raze' : data.get('raze', None),
            'ent__damage' : data.get('damage', None),
            'ent__weakness' : data.get('weakness', None)
        }
        filt = {k:v for k, v in filt.items() if v != ''}
        print(filt)

        count = -1
        try:
            count = int(data.get('count'))
        except ValueError:
            pass

        order = data.get('order_by')
        if order == '' or order is None:
            order = 'pk'
        else:
            order = self.order_by_map.get(order.lower().replace(' ','_'), 'pk')

        all_players = (
            Player.objects
                .filter(**filt)
                .annotate(
                    win_battles=Player.wins_battles(),
                    total_damage_caused=Player.damage_caused()
                )
                .order_by(order)
            )
        
        print('reverse', data.get('reverse', False))
        if data.get('reverse', False):
            all_players = all_players.reverse()

        if count >= 0:
            return all_players[:count]
        else:
            return all_players


class BeastSearchForm(forms.Form):
    name = forms.CharField(label='Name', required=False)
    raze = forms.CharField(label='Raze', required=False)
    damage = forms.CharField(label='Damage', required=False)
    weakness = forms.CharField(label='Weakness', required=False)
    count = forms.CharField(label='Count', required=False)
    order_by = forms.CharField(label='Order by', required=False)
    reverse = forms.BooleanField(label='Reverse', required=False)

    order_by_map = {
        "name": "ent__name",
        "raze": "ent__raze",
        "damage": "ent__damage",
        "weakness": "ent__weakness",
        "total_damage_caused": "total_damage_caused"
    }

    def get_beasts(self):
        data = self.cleaned_data
        filt = { 
            'ent__name' : data.get('name', None),
            'ent__raze' : data.get('raze', None),
            'ent__damage' : data.get('damage', None),
            'ent__weakness' : data.get('weakness', None)
        }
        filt = {k:v for k, v in filt.items() if v != ''}
        print(filt)

        count = -1
        try:
            count = int(data.get('count'))
        except ValueError:
            pass

        order = data.get('order_by')
        if order == '' or order is None:
            order = 'pk'
        else:
            order = self.order_by_map.get(order.lower().replace(' ','_'), 'pk')

        all_beasts = (
            Beast.objects
                .filter(**filt)
                .annotate(
                    win_battles=Beast.wins_battles(),
                    total_damage_caused=Beast.damage_caused()
                )
                .order_by(order)
            )
        
        print('reverse', data.get('reverse', False))
        if data.get('reverse', False):
            all_beasts = all_beasts.reverse()

        if count >= 0:
            return all_beasts[:count]
        else:
            return all_beasts

    def get_beasts(self):
        data = self.cleaned_data
        filt = { 
            'ent__name' : data.get('name', None),
            'ent__raze' : data.get('raze', None),
            'ent__damage' : data.get('damage', None),
            'ent__weakness' : data.get('weakness', None)
        }
        filt = {k:v for k, v in filt.items() if v != ''}
        print(filt)

        count = -1
        try:
            count = int(data.get('count'))
        except ValueError:
            pass

        order = data.get('order_by')
        if order == '' or order is None:
            order = 'pk'
        else:
            order = self.order_by_map.get(order.lower().replace(' ','_'), 'pk')

        all_beasts = (
            Beast.objects
                .filter(**filt)
                .order_by(order)
            )
        
        print('reverse', data.get('reverse', False))
        if data.get('reverse', False):
            all_beasts = all_beasts.reverse()

        if count >= 0:
            return all_beasts[:count]
        else:
            return all_beasts


class SpellSearchForm(forms.Form):
    name = forms.CharField(label='Name', required=False)
    damage = forms.CharField(label='Damage', required=False)
    average_pts = forms.IntegerField(label='Average Pts', required=False)
    reverse = forms.BooleanField(label='Reverse', required=False)

    order_by_map = {
        "name": "spell__name",
        "damage": "spell__damage",
        "average_pts": "spell__average_pts"
    }

    def get_spells(self):
        data = self.cleaned_data
        filt = { 
            'spell__name' : data.get('name', None),
            'spell__damage' : data.get('damage', None),
            'spell__average_pts' : data.get('average_pts', None)
        }
        filt = {k:v for k, v in filt.items() if v != ''}
        print(filt)

        count = -1
        try:
            count = int(data.get('count'))
        except ValueError:
            pass

        order = data.get('order_by')
        if order == '' or order is None:
            order = 'pk'
        else:
            order = self.order_by_map.get(order.lower().replace(' ','_'), 'pk')

        all_spells = (
            Spells.objects
                .filter(**filt)
                .order_by(order)
            )
        
        print('reverse', data.get('reverse', False))
        if data.get('reverse', False):
            all_spells = all_spells.reverse()

        if count >= 0:
            return all_spells[:count]
        else:
            return all_spells


