from django.db import models
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
class Battle(models.Model):
    location = models.ForeignKey(Location, models.CASCADE)
    date = models.DateField(blank=False, null=False)

class BattleParticipant(models.Model):
    ent = models.ForeignKey("Ent", models.CASCADE)
    battle = models.ForeignKey("Battle", models.CASCADE)
    winner = models.BooleanField(default=False)

class Attack(models.Model):
    defender_pts_before = models.IntegerField(blank=False, null=False)
    spell = models.ForeignKey("Spell", models.CASCADE)
    attacker = models.ForeignKey("Ent", models.CASCADE, related_name='attacker')
    deffender = models.ForeignKey("Ent", models.CASCADE, related_name='deffender')

class Ent(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    raze = models.CharField(max_length=50, blank=False, null=False)
    damage = models.CharField(max_length=50, blank=False, null=False)
    weakness = models.CharField(max_length=50, blank=False, null=False)
    health = models.IntegerField(default=100, blank=False, null=False)
    attacks = models.ManyToManyField('self', through=Attack, symmetrical=False, related_name='attacked_from')
    battles = models.ManyToManyField(Battle, through=BattleParticipant, related_name='battles_part')

class Spell(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    damage = models.CharField(max_length=50, blank=False, null=False)
    average_pts = models.IntegerField()

class BattleEvent(models.Model):
    attack = models.ForeignKey(Attack, models.CASCADE)
    battle = models.ForeignKey(Battle, models.CASCADE)
    number = models.IntegerField(blank=False, null=False)

class Player(models.Model):
    ent = models.OneToOneField(Ent, models.CASCADE)
    spells_in_use = models.ManyToManyField(Spell, related_name='in_use_by')
    known_spells = models.ManyToManyField(Spell, related_name='knonw_by')

    def wins_battles():
        return Count(
            'ent__battles',
            filter=Q(ent__battles__battleparticipant__winner=True)
        )

class Beast(models.Model):
    ent = models.OneToOneField(Ent, models.CASCADE)
    damage_pts = models.IntegerField()

