from typing import Any, Dict
from django.contrib.auth import logout
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.db.models import Q, Count

from pages.forms import PlayerSearchForm
from pages.models import *
import copy

# Create your views here.
class BaseView(TemplateView):
    def get(self, request: HttpRequest, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('start')
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        post = request.POST
        if post:
            if 'logout' in post:
                logout(request)
                return redirect('login')

        if 'logout' in post:
            logout(request)
            return redirect('login')
        return super().get(request, *args, **kwargs)


class HomeView(BaseView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = [{
            'name': 'Players',
            'url': 'players',
            'image': 'player.jpg'
        }, {
            'name': 'Beasts',
            'url': 'beasts',
            'image': 'beasts.jpg'
        }, {
            'name': 'Spells',
            'url': 'spells',
            'image': 'spell.jpg'
        }]
        return context

class PlayerSearchView(BaseView):

    template_name = 'player/players.html'
    extra_context = { }

    def post(self, request: HttpRequest, *args, **kwargs):
        post = request.POST
        if request.POST.get('player_search'):
            form = PlayerSearchForm(post)
            if form.is_valid():
                data = form.cleaned_data
                filters = {k: v for k, v in data.items() if v != ''}
                all_players = (
                    Player.objects
                        .filter(**filters)
                        .annotate(win_battles=Player.wins_battles())
                    )
                self.extra_context['data'] = all_players
            self.extra_context['form'] = form

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = {'form': PlayerSearchForm()}
        return super().get_context_data(**context)


def beast_search_view(request):

    context = { }

    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('beast_search'):
            search = {
                'name': request.POST['name'],
                'raze': request.POST['raze']
            }
            context['search'] = search

    if 'search' in context.keys():
        filters = {k: v for k, v in search.items() if v != ''}
        all_beasts = Beast.objects.filter(**filters)
    else:
        all_beasts = Beast.objects.all()
    context['data'] = all_beasts

    return render(request, 'beast/beasts.html', context)