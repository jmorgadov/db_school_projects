from django.shortcuts import render
from .models import *
import copy

# Create your views here.
def add_data_main_view(request):
    return render(request, "add_data/add_data.html")

default_context = {
        'name' : '',
        'damage' : '',
        'average_pts' : ''
    }
    
def add_spell_view(request):
    context = copy.deepcopy(default_context)
    # Aki hay que hacer parecido a como haces en views.player_search_view, para editar un spell
    # if ...
    return render(request, "add_data/spell.html", context)
