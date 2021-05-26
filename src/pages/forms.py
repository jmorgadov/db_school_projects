from typing import Dict, List
from django import forms
from django.db.models import query
from django.db.models.base import Model
from django.db.models.query import QuerySet
from pages.models import Player
from pages.models import Beast
from pages.models import Spell


class SearchForm(forms.Form):
    count = forms.CharField(label='Count', required=False)
    order_by = forms.CharField(label='Order by', required=False)
    reverse = forms.BooleanField(label='Reverse', required=False)

    order_by_map: Dict[str, str] = { 'Id' : 'pk' }
    ordering_by: str = 'Id'
    query_set: QuerySet = None

    def __init__(self, *args, **kwargs) -> None:
        self.order_by_map = self.get_order_by_map()
        super().__init__(*args, **kwargs)

    def orders(self):
        return list(self.order_by_map.keys())

    def get_order_by_map(self):
        return self.order_by_map

    def get_query(self):
        data = self.cleaned_data

        order_by_map = self.get_order_by_map()
        order = data.get('order_by')
        if order == '' or order is None:
            order = 'Id'
        self.ordering_by = order
        order = order_by_map.get(order, 'pk')

        self.query_set = self.query_set.order_by(order)

        if data.get('reverse', False):
            self.query_set = self.query_set.reverse()

        count = -1
        try:
            count = int(data.get('count'))
        except ValueError:
            pass

        if count >= 0:
            return self.query_set[:count]
        else:
            return self.query_set
    
class PlayerSearchForm(SearchForm):
    name = forms.CharField(label='Name', required=False)
    raze = forms.CharField(label='Raze', required=False)
    damage = forms.CharField(label='Damage', required=False)
    weakness = forms.CharField(label='Weakness', required=False)

    def get_order_by_map(self):
        self.order_by_map = {
            'Id': 'id',
            'Name': 'ent__name',
            'Raze': 'ent__raze',
            'Damage': 'ent__damage',
            'Weakness': 'ent__weakness',
            'Win battles': 'win_battles',
            'Total damage caused': 'total_damage_caused'
        }
        return super().get_order_by_map()

    def get_query(self):
        data = self.cleaned_data
        filt = { 
            'ent__name' : data.get('name', None),
            'ent__raze' : data.get('raze', None),
            'ent__damage' : data.get('damage', None),
            'ent__weakness' : data.get('weakness', None)
        }
        filt = {k:v for k, v in filt.items() if v != ''}
        self.query_set = (
            Player.objects
                .filter(**filt)
                .annotate(
                    win_battles=Player.wins_battles(),
                    total_damage_caused=Player.damage_caused()
                )
            )
        return super().get_query()

class BeastSearchForm(SearchForm):
    name = forms.CharField(label='Name', required=False)
    raze = forms.CharField(label='Raze', required=False)
    damage = forms.CharField(label='Damage', required=False)
    weakness = forms.CharField(label='Weakness', required=False)

    def get_order_by_map(self):
        self.order_by_map = {
            'Id': 'id',
            'Name': 'ent__name',
            'Raze': 'ent__raze',
            'Damage': 'ent__damage',
            'Weakness': 'ent__weakness',
            'Battles': 'battles',
        }
        return super().get_order_by_map()

    def get_query(self):
        data = self.cleaned_data
        filt = { 
            'ent__name' : data.get('name', None),
            'ent__raze' : data.get('raze', None),
            'ent__damage' : data.get('damage', None),
            'ent__weakness' : data.get('weakness', None)
        }
        filt = {k:v for k, v in filt.items() if v != ''}

        self.query_set = (
            Beast.objects
                .filter(**filt)
                .annotate(battles=Beast.battles())
            )

        return super().get_query()


class SpellSearchForm(SearchForm):
    name = forms.CharField(label='Name', required=False)
    damage = forms.CharField(label='Damage', required=False)
    average_pts = forms.IntegerField(label='Average Pts', required=False)

    def get_order_by_map(self):
        self.order_by_map = {
            'Id': 'id',
            'Name': 'name',
            'Damage': 'damage',
            'Average pts': 'average_pts',
            'Known by': 'known_by',
            'Times used': 'times_used'
        }
        return super().get_order_by_map()

    def get_query(self):
        data = self.cleaned_data
        filt = { 
            'name' : data.get('name', None),
            'damage' : data.get('damage', None),
            'average_pts' : data.get('average_pts', None)
        }
        filt = {k:v for k, v in filt.items() if v != '' and v is not None}
        self.query_set = (
            Spell.objects
                .filter(**filt)
                .annotate(known_by_count=Spell.known_by_count())
                .annotate(times_used=Spell.times_used())
            )
        return super().get_query()


