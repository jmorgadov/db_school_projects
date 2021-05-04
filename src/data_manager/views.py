from django.shortcuts import render

from pages.models import Spell
import copy

# Create your views here.
def add_data_main_view(request):
    return render(request, "add_data/add_data.html")


def validate_spell(name, damage, average_pts):
    message = ''
    if len(name) > 50:
        message = 'Name too long (50 chars maximum)'
    if len(damage) > 50:
        message = 'Damage too long (50 chars maximum)'
    try:
        pts = int(average_pts)
    except ValueError:
        message = 'Average points must be an integer'
    return len(message), message


def add_spell_view(request):
    context = {
        'name' : '',
        'damage' : '',
        'average_pts' : '',
        'message' : '',
        'message_color' : 'green'
    }    

    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('add_spell'):
            # Get fields values
            name = request.POST['name']
            context['name'] = name
            damage = request.POST['damage']
            context['damage'] = damage
            average_pts = request.POST['average_pts']
            context['average_pts'] = average_pts

            # Validate values
            error, message = validate_spell(name, damage, average_pts)

            if not error:
                filt = Spell.objects.filter(name=name)
                if filt:
                    spell = filt[0]
                    spell.damage = damage
                    spell.average_pts = average_pts
                    context['message'] = 'Spell edited'
                else:
                    spell = Spell.objects.create(name=name, damage=damage,
                                                 average_pts=average_pts)
                    context['message'] = 'Spell created'
                spell.save()
            else:
                context['message'] = message
                context['message_color'] = 'red'   
    
    return render(request, "add_data/spell.html", context)
