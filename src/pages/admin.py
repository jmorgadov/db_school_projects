from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Battle)
admin.site.register(BattleParticipant)
admin.site.register(Attack)
admin.site.register(Ent)
admin.site.register(Spell)
admin.site.register(BattleEvent)
admin.site.register(Player)