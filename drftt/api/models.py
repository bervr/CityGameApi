from django.db import models


class Team(models.Model):
    team_number = models.IntegerField(primary_key=True,)
    team_name = models.CharField(max_length=64, verbose_name='Название команды')

    def __str__(self):
        return self.team_name


class Game(models.Model):
    game_number = models.IntegerField(
        primary_key=True,
    )
    game_name = models.CharField(max_length=64, verbose_name='Название игры')
    game_go = models.BooleanField(default=False)
    game_start = models.DateTimeField(blank=True, null=True)
    game_finish = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.game_name


class GameLevel(models.Model):
    level_of_game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name='уровень',
    )
    number = models.IntegerField(
        primary_key=True,
    )
    geo_lat = models.FloatField(max_length=16, verbose_name='широта')
    geo_lng = models.FloatField(max_length=16, verbose_name='долгота')
    name = models.CharField(max_length=64, unique=True, verbose_name='название уровня')
    task = models.TextField(verbose_name='текст задания', )
    image = models.ImageField(
        upload_to='level_img',
        blank=True,
    )
    level_started = models.BooleanField(default=False)
    level_active = models.BooleanField(default=True)
    level_done = models.BooleanField(default=False)
    fail_try = models.BooleanField(default=False)
    started = models.DateTimeField(blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'({self.number} - {self.name})'


class CorrectAnswers(models.Model):
    level = models.ForeignKey(
        GameLevel,
        on_delete=models.CASCADE,
        verbose_name='уровень',

    )
    answer = models.CharField(max_length=256)

    def __str__(self):
        return f'({self.level} - {self.answer})'


class WrongAnswers(models.Model):
    level = models.ForeignKey(
        GameLevel,
        on_delete=models.CASCADE,
        verbose_name='уровень',
    )
    answer = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.answer


class Promt(models.Model):
    level = models.ForeignKey(
        GameLevel,
        on_delete=models.CASCADE,
        verbose_name='уровень',
    )
    promt = models.CharField(max_length=300, blank=True, verbose_name='подсказка')
    counter = models.IntegerField(
    )

    def __str__(self):
        return f'(Уровень {self.level} подсказка {self.counter})'
