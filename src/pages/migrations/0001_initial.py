# Generated by Django 3.1.7 on 2021-05-11 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('defender_pts_before', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='BattleParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner', models.BooleanField(default=False)),
                ('battle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.battle')),
            ],
        ),
        migrations.CreateModel(
            name='Ent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('raze', models.CharField(max_length=50)),
                ('damage', models.CharField(max_length=50)),
                ('weakness', models.CharField(max_length=50)),
                ('health', models.IntegerField(default=100)),
                ('attacks', models.ManyToManyField(through='pages.Attack', to='pages.Ent')),
                ('battles', models.ManyToManyField(through='pages.BattleParticipant', to='pages.Battle')),
            ],
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('damage', models.CharField(max_length=50)),
                ('average_pts', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pages.ent')),
                ('known_spells', models.ManyToManyField(related_name='knonw', to='pages.Spell')),
                ('spells_in_use', models.ManyToManyField(related_name='in_use', to='pages.Spell')),
            ],
        ),
        migrations.CreateModel(
            name='Beast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('damage_pts', models.IntegerField()),
                ('ent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pages.ent')),
            ],
        ),
        migrations.AddField(
            model_name='battleparticipant',
            name='ent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.ent'),
        ),
        migrations.CreateModel(
            name='BattleEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('attacker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attacker', to='pages.ent')),
                ('battle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.battle')),
                ('defender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defender', to='pages.ent')),
            ],
        ),
        migrations.AddField(
            model_name='attack',
            name='spell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.spell'),
        ),
    ]
