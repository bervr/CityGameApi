from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Game(models.Model):
    game_number = models.IntegerField(
        primary_key=True,
    )
    game_name = models.CharField(max_length=64, verbose_name='название игры')
    game_go = models.BooleanField(default=False)
    game_start = models.DateTimeField(blank=True, null=True)
    game_finish = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.game_name


class GameLevel(models.Model):
    level_of_game = models.ForeignKey(
        Game,
        related_name='game_id',
        on_delete=models.CASCADE,
        verbose_name='игра',
    )
    number = models.IntegerField(primary_key=True, )
    geo_lat = models.FloatField(max_length=16, verbose_name='широта')
    geo_lng = models.FloatField(max_length=16, verbose_name='долгота')
    name = models.CharField(max_length=64, unique=True, verbose_name='название уровня')
    task = models.TextField(verbose_name='текст задания', )
    answer = models.CharField(max_length=256)
    level_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.number}/{self.name}'


class Promt(models.Model):
    level = models.ForeignKey(
        GameLevel,
        related_name='promts',
        on_delete=models.CASCADE,
        verbose_name='уровень',
    )
    promt1 = models.CharField(max_length=300, db_index=True)
    promt2 = models.CharField(max_length=300, db_index=True)
    promt3 = models.CharField(max_length=300, db_index=True)

    def __str__(self):
        return f'Promts {self.level} level'


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
    getted_promt_counter = models.PositiveIntegerField(default=0)

    data = models.JSONField(null=True)

    team = models.ForeignKey(
        'auth.User',
        related_name='playing_team',
        on_delete=models.CASCADE,
        verbose_name='команда',
    )

    def registry_promt(instance, team, promt_number):
        level, __ = GamePlay.objects.get_or_create(level=instance, game=instance.level_of_game, team=team)
        if not level.data:
            level.data = {  # тут будет хранить сведенья о выданных подскзках
                1: False,
                2: False,
                3: False,
            }
            level.save()
        if level.level_status != 'DN':
            if not level.data[f'{promt_number}']:
                level.data[promt_number] = True
                level.getted_promt_counter += 1
                level.save()

    @receiver(pre_save, sender=TeamAnswers)
    def write_user_answer(sender, instance, **kwargs):
        level, __ = GamePlay.objects.get_or_create(level=instance.level, game=instance.game, team=instance.team)
        if level.level_status != 'DN':
            if TeamAnswers.check_answer(instance):
                level.level_status = 'DN'
                level.level_finished = datetime.now()
            else:
                level.level_status = 'TTA'
            level.save()

    def __str__(self):
        return f'команда {self.team}/ уровень-{self.level}' \
               f'/ статус - {self.level_status} /использовано подсказок {self.getted_promt_counter}'
