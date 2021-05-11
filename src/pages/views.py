from django.shortcuts import redirect, render
from .models import *
import copy

general_context = {
    'categories' : [
        {
            'name' : 'Players',
            'url' : 'players'
        },
        {
            'name' : 'Beasts',
            'url' : 'beasts'
        },
        {
            'name' : 'Spells',
            'url' : 'spells'
        }
    ],
    'text' : 'Welcome'
}

# Create your views here.
def home_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('start')
    context = copy.deepcopy(general_context)
    return render(request, 'home.html', context)

def player_search_view(request):

    context = copy.deepcopy(general_context)

    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('player_search'):
            search = {
                'name' : request.POST['name'],
                'raze' : request.POST['raze'],
                'damage' : request.POST['damage'],
                'weakness' : request.POST['weakness'],
            }
            context['search'] = search

    if 'search' in context.keys():
        filters = {k:v for k, v in search.items() if v != ''}
        all_players = Player.objects.filter(**filters)
    else:
        all_players = Player.objects.all()
    context['data'] = all_players
    

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