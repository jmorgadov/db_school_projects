from django.db import models
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q

# Create your models here.
class Battle(models.Model):
    place = models.CharField(max_length=50, blank=False, null=False)
    date = models.DateField(blank=False, null=False)

class BattleParticipant(models.Model):
    ent = models.ForeignKey("Ent", models.CASCADE)
    battle = models.ForeignKey("Battle", models.CASCADE)
    winner = models.BooleanField(default=False)

class Attack(models.Model):
    defender_pts_before = models.IntegerField(blank=False, null=False)
    spell = models.ForeignKey("Spell", models.CASCADE)

class Ent(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    raze = models.CharField(max_length=50, blank=False, null=False)
    damage = models.CharField(max_length=50, blank=False, null=False)
    weakness = models.CharField(max_length=50, blank=False, null=False)
    health = models.IntegerField(default=100, blank=False, null=False)
    attacks = models.ManyToManyField("Ent", through=Attack)
    battles = models.ManyToManyField(Battle, through=BattleParticipant)

class Spell(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    damage = models.CharField(max_length=50, blank=False, null=False)
    average_pts = models.IntegerField()

class BattleEvent(models.Model):
    attacker = models.ForeignKey(Ent, models.CASCADE, related_name='attacker')
    defender = models.ForeignKey(Ent, models.CASCADE, related_name='defender')
    battle = models.ForeignKey(Battle, models.CASCADE)
    number = models.IntegerField(blank=False, null=False)

class Player(models.Model):
    ent = models.OneToOneField(Ent, models.CASCADE)
    spells_in_use = models.ManyToManyField(Spell, related_name='in_use')
    known_spells = models.ManyToManyField(Spell, related_name='knonw')

    def wins_battles():
        return Count(
            'ent__battles',
            filter=Q(ent__battles__battleparticipant__winner=True)
        )

class Beast(models.Model):
    ent = models.OneToOneField(Ent, models.CASCADE)
    damage_pts = models.IntegerField()

