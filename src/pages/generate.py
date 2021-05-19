from pages.models import *
from datetime import datetime
from functools import reduce
from random import shuffle, choice, randint, sample
import json

model_types = [
    Battle,
    BattleParticipant,
    Attack,
    Ent,
    Spell,
    BattleEvent,
    Player,
    Beast
]


def clean_model(model_type):
    for item in model_type.objects.all():
        item.delete()

def clean_db():
    for t in model_types:
        clean_model(t)

def create_random_data():
    clean_db()

    data = None
    with open('pages/fake_data/random_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    races = data.get('races', [])
    damages = data.get('damages', [])

    for location in data.get('locations', []):
        fields = { 'name': location }
        Location.objects.create(**fields)

    spells = []

    for spell in data.get('spells', []):
        fields = {
            'name': spell,
            'damage': choice(damages),
            'average_pts': randint(5, 25)
        }
        spells.append(Spell.objects.create(**fields))

    for player in data.get('player_names', []):
        damage, weakness = sample(damages, k=2)
        fields = {
            'name': player,
            'raze': choice(races),
            'damage': damage,
            'weakness': weakness
        }
        ent = Ent.objects.create(**fields)
        player_fields = {
            'ent': ent
        }
        p = Player.objects.create(**player_fields)
        p.known_spells.set(sample(spells, k=randint(1,8)))

    for beast in data.get('beasts', []):
        damage, weakness = sample(damages, k=2)
        fields = {
            'name': beast,
            'raze': choice(races),
            'damage': damage,
            'weakness': weakness
        }
        ent = Ent.objects.create(**fields)
        beast_fields = {
            'ent': ent,
            'damage_pts': randint(5,25)
        }
        Beast.objects.create(**beast_fields)


def parse_model(model_type, fields, **extra):
    model_fields = {}
    m2m_fields = {}
    for field, value in fields.items():
        extra_name = f'{field}_set'
        if extra_name in extra:
            if isinstance(value, int):
                model_fields[field] = extra[extra_name][value]
            elif isinstance(value, list):
                m2m_fields[field] = [extra[extra_name][i] for i in value]
        else:
            model_fields[field] = value
    
    obj = model_type.objects.create(**model_fields)
    for field, value in m2m_fields.items():
        obj.__getattribute__(field).set(value)
    return obj

def generate_data_from_models():
    clean_db()

    data = None
    with open('pages/fake_data/models.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    battles = [parse_model(Battle, m) for m in data.get('battles', [])]
    spells = [parse_model(Spell, m) for m in data.get('spells', [])]
    ents = [parse_model(Ent, m) for m in data.get('ents', [])]
    attacks = [
        parse_model(
            Attack,
            m,
            attacker_set=ents,
            deffender_set=ents,
        ) for m in data.get('attacks', [])
    ]
    battle_events = [
        parse_model(
            BattleEvent,
            m,
            attack_set=attacks,
            battle_set=battles
        ) for m in data.get('battle_events', [])
    ]
    battle_partic = [
        parse_model(
            BattleParticipant,
            m,
            ent_set=ents,
            battle_set=battles
        ) for m in data.get('battle_partic', [])
    ]
    players = [
        parse_model(
            Player,
            m,
            ent_set=ents,
            spells_in_use_set=spells,
            known_spells_set=spells,
        ) for m in data.get('players', [])
    ]
    beasts = [
        parse_model(
            Beast,
            m,
            ent_set=ents,
            spells_in_use_set=spells,
            known_spells_set=spells,
        ) for m in data.get('beasts', [])
    ]


    battle_partic = [parse_model(BattleParticipant, m) for m in data.get('battle_partic', [])]

    entries = battles + attacks + spells + ents + battle_events + \
              battle_partic + players + beasts
    for entry in entries:
        entry.save()