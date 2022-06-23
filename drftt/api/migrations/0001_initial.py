# Generated by Django 4.0.5 on 2022-06-22 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_number', models.IntegerField(primary_key=True, serialize=False)),
                ('game_name', models.CharField(max_length=64, verbose_name='Название игры')),
                ('game_go', models.BooleanField(default=False)),
                ('game_start', models.DateTimeField(blank=True, null=True)),
                ('game_finish', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameLevel',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False)),
                ('geo_lat', models.FloatField(max_length=16, verbose_name='широта')),
                ('geo_lng', models.FloatField(max_length=16, verbose_name='долгота')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='название уровня')),
                ('task', models.TextField(verbose_name='текст задания')),
                ('image', models.ImageField(blank=True, upload_to='level_img')),
                ('promt1', models.CharField(blank=True, max_length=300, verbose_name='подсказка1')),
                ('promt2', models.CharField(blank=True, max_length=300, verbose_name='подсказка2')),
                ('promt3', models.CharField(blank=True, max_length=300, verbose_name='подсказка3')),
                ('got_promt_counter', models.IntegerField(default=0)),
                ('level_started', models.BooleanField(default=False)),
                ('level_active', models.BooleanField(default=True)),
                ('level_done', models.BooleanField(default=False)),
                ('fail_try', models.BooleanField(default=False)),
                ('started', models.DateTimeField(blank=True, null=True)),
                ('finished', models.DateTimeField(blank=True, null=True)),
                ('level_of_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.game', verbose_name='уровень')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_number', models.IntegerField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=64, verbose_name='Название команды')),
            ],
        ),
        migrations.CreateModel(
            name='WrongAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=256)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gamelevel', verbose_name='уровень')),
            ],
        ),
        migrations.CreateModel(
            name='CorrectAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=256)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gamelevel', verbose_name='уровень')),
            ],
        ),
    ]