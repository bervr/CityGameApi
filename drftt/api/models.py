from django.db import models
# from django.contrib.auth.models import User



# class Team(models.Model, User):
#     # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team')
#     # team_number = models.IntegerField(primary_key=True,)
#     team_name = models.CharField(max_length=64, verbose_name='название команды')
#
#     def __str__(self):
#         return self.team_name

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
        on_delete=models.CASCADE,
        verbose_name='игра',
    )
    number = models.IntegerField(primary_key=True,)
    geo_lat = models.FloatField(max_length=16, verbose_name='широта')
    geo_lng = models.FloatField(max_length=16, verbose_name='долгота')
    name = models.CharField(max_length=64, unique=True, verbose_name='название уровня')
    task = models.TextField(verbose_name='текст задания', )
    answer = models.CharField(max_length=256)
    level_active = models.BooleanField(default=True)


    def __str__(self):
        return f'{self.number}/{self.name}'


class GamePlay(models.Model):
    DONE = 'DN'
    TRY_TO_ASK = 'TTA'
    NOT_STARTED = 'NSD'
    LEVEL_STATUS_CHOICES = (
        (DONE, 'сдано'),
        (TRY_TO_ASK, 'неверный ответ'),
        (NOT_STARTED, 'не начато'),
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name='игра',
    )
    level = models.ForeignKey(
        GameLevel,
        on_delete=models.CASCADE,
        verbose_name='уровень',)
    level_started = models.DateTimeField(blank=True, null=True)
    level_finished = models.DateTimeField(blank=True, null=True)
    level_status = models.CharField(verbose_name='статус',
                              max_length=3,
                              choices=LEVEL_STATUS_CHOICES,
                              default=NOT_STARTED)
    getted_promt_counter = models.PositiveIntegerField(default=0)

    team = models.ForeignKey(
        'auth.User',
        related_name='playing_team',
        on_delete=models.CASCADE,
        verbose_name='команда',
    )

    def __str__(self):
        return f'команда {self.team}/ уровень-{self.level}' \
               f'/ статус - {self.level_status} /использовано подсказок {self.getted_promt_counter}'


class TeamAnswers(models.Model):
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
    answer = models.CharField(max_length=256,)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def check_answer(self):
        pass

    def __str__(self):
        return f'({self.level} - {self.team} - {self.answer})'

class Promt(models.Model):
    level = models.ForeignKey(
        GameLevel,
        on_delete=models.CASCADE,
        verbose_name='уровень',
    )
    promt = models.CharField(max_length=256, blank=True, verbose_name='подсказка')
    counter = models.IntegerField(default=0)


    # def get_promt(self, number):
    #     promt = self.level.objects.get(number)
    #     self
    #     self.is_active = False
    #     self.save()

    def __str__(self):
        return f'Уровень {self.level} подсказка {self.counter}'



