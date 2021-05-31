from typing import List
from django.db import models
from django.db.models import Count, Sum, Q, F
from random import choice, randint, random, sample
from datetime import datetime, timedelta

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

class Battle(models.Model):
    location = models.ForeignKey(Location, models.CASCADE)
    date = models.DateField(blank=False, null=False)

    def duration_query():
        return Count(
            'battleevent',
            distinct=True
        )


class BattleParticipant(models.Model):
    ent = models.ForeignKey("Ent", models.CASCADE)
    battle = models.ForeignKey("Battle", models.CASCADE)
    winner = models.BooleanField(default=False)

class Attack(models.Model):
    spell = models.ForeignKey("Spell", models.CASCADE, null=True)
    attacker = models.ForeignKey("Ent", models.CASCADE, related_name='attacker')
    defender = models.ForeignKey("Ent", models.CASCADE, related_name='defender')

    defender_pts_before = models.IntegerField(default=0, blank=False, null=False)
    damage_caused = models.IntegerField(default=0, blank=False, null=False)

    def save(self, *agrs, **kwagrs) -> None:
        self.defender_pts_before = self.defender.health
        
        dmg_pts = 0
        ent_t, instance = self.attacker.ent_type
        multiplier = (random() / 10) - 0.05
        if ent_t == 'player':
            dmg_pts = self.spell.average_pts + self.spell.average_pts * multiplier
        elif ent_t == 'beast':
            dmg_pts = instance.damage_pts + instance.damage_pts * multiplier

        if self.defender.weakness == self.attacker.damage:
            dmg_pts += 100

        new_health = max(0, self.defender.health - dmg_pts)
        self.defender.health = new_health
        self.defender.save()

        self.damage_caused = self.defender_pts_before - new_health
        return super().save(*agrs, **kwagrs)

class Ent(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    raze = models.CharField(max_length=50, blank=False, null=False)
    damage = models.CharField(max_length=50, blank=False, null=False)
    weakness = models.CharField(max_length=50, blank=False, null=False)
    health = models.FloatField(default=100, blank=False, null=False)

    @property
    def ent_type(self):
        try:
            return 'player', self.player
        except:
            pass

        try:
            return 'beast', self.beast
        except:
            pass
        return None, None

    @property
    def is_player(self):
        ent_t, _ = self.ent_type
        return ent_t == 'player'
    
    @property
    def is_beast(self):
        ent_t, _ = self.ent_type
        return ent_t == 'beast'


class Spell(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    damage = models.CharField(max_length=50, blank=False, null=False)
    average_pts = models.IntegerField()

    def known_by_count():
        return Count(
            'known_by',
            distinct=True
        )

    def times_used():
        return Count(
            'attack'
        )

class BattleEvent(models.Model):
    attack = models.ForeignKey(Attack, models.CASCADE)
    battle = models.ForeignKey(Battle, models.CASCADE)
    number = models.IntegerField(blank=False, null=False)

class Player(models.Model):
    ent = models.OneToOneField(Ent, models.CASCADE)
    spells_in_use = models.ManyToManyField(Spell, related_name='in_use_by')
    known_spells = models.ManyToManyField(Spell, related_name='known_by')

    def wins_battles():
        return Count(
            'ent__battleparticipant',
            filter=Q(ent__battleparticipant__winner=True),
            distinct=True
        )

    def damage_caused():
        return Sum('ent__attacker__damage_caused', distinct=True)

class Beast(models.Model):
    ent = models.OneToOneField(Ent, models.CASCADE)
    damage_pts = models.IntegerField()

    def battles():
        return Count(
            'ent__battleparticipant__battle',
            distinct=True
        )



def get_random_sample(model_type, k=1):
    query_set = model_type.objects.all()
    ids = list(query_set.values_list('id', flat=True))
    random_ids = sample(ids, k=min(len(ids),k))
    return query_set.filter(pk__in=random_ids)

def get_random_entry(model_type):
    return get_random_sample(model_type)[0]

def simulate_battle_iter(participants=16):
    location = get_random_entry(Location)
    date = datetime.now() - timedelta(days=randint(0, 365), minutes=randint(0,59))
    battle = Battle.objects.create(location=location, date=date)
    players_count = randint(0, participants)
    beasts_count = participants - players_count

    # Get random samples
    players = get_random_sample(Player, players_count)
    beasts = get_random_sample(Beast, beasts_count)

    # Prepare players
    for player in players:
        known_spells = list(player.known_spells.all())
        player.spells_in_use.set(sample(known_spells, k=min(len(known_spells), 3)))

    # Get ent list
    ent_ids = list(players.values_list('ent')) + \
           list(beasts.values_list('ent'))
    ent_ids = [e[0] for e in ent_ids]
    ents = Ent.objects.filter(pk__in=ent_ids)

    alive_ents: List[Ent] = list(ents)

    for ent in alive_ents:
        ent.health = 100
        ent.save()
        BattleParticipant.objects.create(ent=ent, battle=battle)

    event = 0
    while len(alive_ents) != 1:
        event += 1
        print(f'    Event: {event} - Ents alive: {len(alive_ents)}')
        attacker, defender = sample(alive_ents, 2)
        spell_used = None
        if attacker.is_player:
            spell_used = choice(list(attacker.player.spells_in_use.all()))
        attack = Attack.objects.create(attacker=attacker, defender=defender, spell=spell_used)
        BattleEvent.objects.create(battle=battle, attack=attack, number=event)

        yield f'{attacker.name:^24} --> {defender.name:^24}  (Damage caused: {round(attack.damage_caused, 3)})'
        if defender.health == 0:
            alive_ents.remove(defender)

    bp = BattleParticipant.objects.get(ent__pk=attacker.pk, battle=battle)
    bp.winner = True
    bp.save()


def simulate_battle(participants=16):
    for log in simulate_battle_iter(participants):
        print(log)
