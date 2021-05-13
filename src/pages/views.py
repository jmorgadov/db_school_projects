from django.contrib.auth import logout
from django.shortcuts import redirect, render

from pages.forms import PlayerSearchForm
from .models import *
import copy

general_context = {
    'categories' : [
        {
            'name' : 'Players',
            'url' : 'players',
            'image' : 'player.jpg'
        },
        {
            'name' : 'Beasts',
            'url' : 'beasts',
            'image' : 'beasts.jpg'
        },
        {
            'name' : 'Spells',
            'url' : 'spells',
            'image' : 'spell.jpg'
        }
    ],
    'text' : 'Welcome'
}

# Create your views here.
def home_view(request):
    # user = request.user
    # if not user.is_authenticated:
    #     return redirect('start')
    if request.POST:
        if 'logout' in request.POST:
            logout(request)
            return redirect('login')
    context = copy.deepcopy(general_context)
    return render(request, 'home.html', context)

def player_search_view(request):

    context = {
        'form' : PlayerSearchForm()
    }

    if request.method == 'POST':
        post = request.POST
        if request.POST.get('player_search'):
            form = PlayerSearchForm(post)
            if form.is_valid():
                data = form.cleaned_data        
                filters = {k:v for k, v in data.items() if v != ''}
                all_players = Player.objects.filter(**filters)
                context['data'] = all_players
            context['form'] = form
    
    return render(request, 'player/players.html', context)

    
def beast_search_view(request):

    context = copy.deepcopy(general_context)

    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('beast_search'):
            search = {
                'name' : request.POST['name'],
                'raze' : request.POST['raze']
            }
            context['search'] = search

    if 'search' in context.keys():
        filters = {k:v for k, v in search.items() if v != ''}
        all_beasts = Beast.objects.filter(**filters)
    else:
        all_beasts = Beast.objects.all()
    context['data'] = all_beasts    

    return render(request, 'beast/beasts.html', context)