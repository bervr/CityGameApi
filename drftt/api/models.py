import datetime

from django.contrib import auth
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from collections import OrderedDict
import zoneinfo


class Game(models.Model):
    game_number = models.AutoField(
        primary_key=True,
    )
    game_name = models.CharField(max_length=64, verbose_name='название игры')
    game_go = models.BooleanField(default=False)
    game_start = models.DateTimeField(blank=True, null=True)
    game_finish = models.DateTimeField(blank=True, null=True)
    now = timezone.now()

    def check_game_time(instance):  #допустим что город один и сервер в его часовом поясе
        if instance.game_finish >= timezone.now() >= instance.game_start and not instance.game_go:
            instance.game_go = True
            instance.save()
        if instance.game_finish <= timezone.now() and instance.game_go:
            instance.game_go = False
            instance.save()
        return instance.game_go

    def get_places(self):
        places = {}
        raw_places =[]
        teams = User.objects.all()
        for team in teams:
            team_set = {}
            team_total_penalty = 0
            level_finished = 0
            levels = {}
            for level in GamePlay.objects.filter(game=self).filter(team=team):
                lvl = {}
                lvl['level_name'] = level.level.name
                lvl['level_status'] = level.level_status
                if level.level_status == 'DN':
                    level_finished += 1
                    team_total_penalty += level.level_penalty + level.getted_promt_counter*900 + \
                                          level.wrong_counter_answer*1800
                if level.level_penalty:
                    lvl['level_penalty'] = self.get_human_time(level.level_penalty)
                levels[f'{level.level_id}'] = lvl

            team_set['team'] = team.username
            team_set['levels'] = levels
            team_set['summ_penalty'] = self.get_human_time(team_total_penalty)
            team_set['total_finished'] = level_finished
            raw_places.append(team_set)
        sorted_places = sorted(sorted(raw_places, key=lambda x: x['summ_penalty']), key=lambda x: x['total_finished'], reverse=True)
        for i, item in enumerate(sorted_places):
            sorted_places[i]['place'] = i+1
            places[i+1] = sorted_places[i]
        return places

    def get_human_time(self, time):
        seconds = int(time)
        millis = str(time-seconds).strip('0')
        human_time = str(datetime.timedelta(seconds=seconds))
        return human_time+millis

    def __str__(self):
        return self.game_name


class GameLevel(models.Model):
    level_of_game = models.ForeignKey(
        Game,
        related_name='game_id',
        on_delete=models.CASCADE,
        verbose_name='игра',
    )
    id = models.AutoField(primary_key=True)
    number = models.PositiveIntegerField(auto_created=True)
    geo_lat = models.FloatField(max_length=16, verbose_name='широта')
    geo_lng = models.FloatField(max_length=16, verbose_name='долгота')
    name = models.CharField(max_length=64, unique=True, verbose_name='название уровня')
    task = models.TextField(verbose_name='текст задания', )
    answer = models.CharField(max_length=256)
    level_active = models.BooleanField(default=True)
    promt1 = models.CharField(max_length=300, null=True, db_index=True)
    promt2 = models.CharField(max_length=300, null=True, db_index=True)
    promt3 = models.CharField(max_length=300, null=True, db_index=True)

    def __str__(self):
        return f'{self.level_of_game}/{self.number} level/{self.name}'


class TeamAnswers(models.Model):
    game = models.ForeignKey(
        Game,
        related_name='answ_for_game',
        on_delete=models.CASCADE,
        verbose_name='игра',
    )
    level = models.ForeignKey(
        GameLevel,
        related_name='answers',
        on_delete=models.CASCADE,
        verbose_name='уровень',
    )
    team = models.ForeignKey(
        'auth.User',
        related_name='answers_team',
        on_delete=models.CASCADE,
        verbose_name='команда',
    )
    answer = models.CharField(max_length=256, )
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def check_answer(self, ):
        valid_answer = self.level.answer
        if valid_answer == self.answer:
            return True

    def __str__(self):
        return f'({self.level} - {self.team} - {self.answer})'


class GamePlay(models.Model):
    DONE = 'DN'
    TRY_TO_ANSW = 'TTA'
    NOT_STARTED = 'NSD'
    LEVEL_STATUS_CHOICES = (
        (DONE, 'сдано'),
        (TRY_TO_ANSW, 'неверный ответ'),
        (NOT_STARTED, 'не начато'),
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name='игра',
    )
    level = models.ForeignKey(
        GameLevel,
        related_name='team_level',
        on_delete=models.CASCADE,
        verbose_name='уровень', )
    level_started = models.DateTimeField(blank=True, null=True)
    level_finished = models.DateTimeField(blank=True, null=True)
    level_status = models.CharField(verbose_name='статус',
                                    max_length=3,
                                    choices=LEVEL_STATUS_CHOICES,
                                    default=NOT_STARTED)
    getted_promt_counter = models.PositiveIntegerField(null=True, default=0)
    # data_dict = dict()
    # data_dict =
    data = models.JSONField(default={  # тут будет хранить сведенья о выданных подсказках
                1: False,
                2: False,
                3: False,
            })
    # data = data_dict

    team = models.ForeignKey(
        'auth.User',
        related_name='playing_team',
        on_delete=models.CASCADE,
        verbose_name='команда',
    )
    wrong_counter_answer = models.PositiveIntegerField(null=True, default=0)
    level_penalty = models.DecimalField(null=True, max_digits=17, decimal_places=11)

    def start_game_level(instance, team):
        level = GamePlay.objects.create(level=instance, game=instance.level_of_game, team=team)
        level.level_started = instance.level_of_game.game_start
        level.save()

    def registry_promt(instance, team, promt_number):
        level = GamePlay.objects.filter(team=team).filter(level=instance).get()
        if level.level_status != 'DN':
            if not level.data[str(promt_number)]:
                level.data[str(promt_number)] = True
                level.getted_promt_counter += 1
                level.save()

    @receiver(pre_save, sender=TeamAnswers)
    def write_user_answer(sender, instance, **kwargs):
        try:
            level = GamePlay.objects.filter(team=instance.team).filter(level=instance.level).get()
        except:
            GamePlay.start_game_level(instance.level, instance.team)
            level = GamePlay.objects.filter(team=instance.team).filter(level=instance.level).get()
            level.save()
        game = level.game
        if game.check_game_time():  # проверяем что игра активна
            if level.level_status != 'DN':
                if TeamAnswers.check_answer(instance):
                    level.level_status = 'DN'
                    level.level_finished = timezone.now()
                    level.level_penalty = (level.level_finished - level.level_started).total_seconds()
                else:
                    level.level_status = 'TTA'
                    level.wrong_counter_answer +=1
                level.save()

    def __str__(self):
        return f'команда {self.team}/ уровень-{self.level}' \
               f'/ статус - {self.level_status} /использовано подсказок {self.getted_promt_counter}'


class TeamPlace(models.Model):
    id = models.AutoField(primary_key=True)
    game_id = models.PositiveIntegerField()
    place = models.BigIntegerField(null=True)
    user = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    level = models.ForeignKey(GameLevel, on_delete=models.DO_NOTHING)
    level_status = models.CharField(max_length=15)
    level_penalty = models.DecimalField(max_digits=17, decimal_places=11)
    total_finished = models.PositiveIntegerField(null=True, blank=True)
    summ_penalty = models.DecimalField(null=True, max_digits=17, decimal_places=11)
    class Meta:
        managed = False
        db_table = 'team_place'






