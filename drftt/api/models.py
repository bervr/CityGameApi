from django.db import models
# from django.contrib.auth.models import User

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

class Dicty(models.Model):
    name = 'promts'
    max_length = models.PositiveIntegerField(default=3)

class PromtKV(models.Model):
    container = models.ForeignKey(Dicty, db_index=True, on_delete=models.CASCADE,)
    key = models.CharField(max_length=50, default='подсказка', db_index=True)
    value = models.CharField(max_length=300, blank=True, db_index=True)
    # verbose_name = models.CharField(max_length=50, blank=True, db_index=True)

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

    promt_dict = PromtKV()

    promt1 = models.CharField(max_length=300, blank=True, verbose_name='подсказка1')
    promt2 = models.CharField(max_length=300, blank=True, verbose_name='подсказка2')
    promt3 = models.CharField(max_length=300, blank=True, verbose_name='подсказка3')
    promt_dict = {'promt1': promt1,
                  'promt2': promt2,
                  'promt3': promt3}


    def __str__(self):
        return f'{self.number}/{self.name}'

# class Promt(models.Model):
#     level = models.ForeignKey(
#         GameLevel,
#         on_delete=models.CASCADE,
#         verbose_name='уровень',
#     )
#
#
#     def __str__(self):
#         return f'Уровень {self.level} подсказка {self.promt_number}'

class GamePlay(models.Model):
    DONE = 'DN'
    TRY_TO_ASK = 'TTA'
    NOT_STARTED = 'NSD'
    LEVEL_STATUS_CHOICES = (
        (DONE, 'сдано'),
        (TRY_TO_ASK, 'неверный ответ'),
        (NOT_STARTED, 'не начато'),
    )
    opened_promt = 'OPP'
    closed_promt = 'CLP'


    promt_status_choises = (
        (opened_promt, 'открытая'),
        (closed_promt, 'закрытая')
    )

    promt1_status = models.CharField(verbose_name='подсказка1',
                                    max_length=3,
                                    choices=promt_status_choises,
                                    default=closed_promt)

    promt2_status = models.CharField(verbose_name='подсказка2',
                                    max_length=3,
                                    choices=promt_status_choises,
                                    default=closed_promt)

    promt3_status = models.CharField(verbose_name='подсказка3',
                                    max_length=3,
                                    choices=promt_status_choises,
                                    default=closed_promt)


    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name='игра',
    )
    level = models.ForeignKey(
        GameLevel,
        related_name='team_level',
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

    def one_promt_geted(self, level, number, user):
        pass
        # levels_promt = GamePlay.objects.get(level)
        # current_team = GamePlay.objects.get(user)
        # requested_promt = GamePlay.objects.get(f'promt{number}')
        # current_promt = GamePlay.objects.filter(level=level, team=user, )


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




