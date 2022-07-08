import datetime

from .serialisers import GameLevelSerialiser, GamePlaySerialiser, GameSerialiser,\
    TeamSerialiser, AnswerSerialiser, PromtSerialiser, GameSummarySerialiser
from .models import Game, GameLevel, TeamAnswers, GamePlay, Promt, TeamPlace
from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404



class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerialiser

class GameDetail(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerialiser

class GameLevelList(generics.ListAPIView):
    queryset = GameLevel.objects.all()
    serializer_class = GameLevelSerialiser

class GetPromt(generics.RetrieveAPIView):
    queryset = Promt.objects.all()
    serializer_class = PromtSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self, list=[]):
        data = super().get_serializer_class()
        setattr(data.Meta, 'fields', list)  # грязно, но по-другому не придумал
        return data

    def get_serializer(self, *args, **kwargs):
        team = self.request.user
        level_number = self.kwargs['pk']
        promt_number = self.kwargs['num']
        game_level = get_object_or_404(GameLevel, number=level_number)
        try:
            requested_level = GamePlay.objects.filter(team=team).filter(level=level_number).get()
        except:
            GamePlay.start_game_level(game_level, team)
            requested_level = GamePlay.objects.filter(team=team).filter(level=level_number).get()

        if game_level and game_level.level_active or requested_level.level_status != 'DN':  # проверяем что уровень открыт команде или не закончен
            promt_list = [f'promt{promt_number}',]
            GamePlay.registry_promt(game_level, team, promt_number)  # регистрируем выдачу подсказки
        else:
            promt_list = []
        serializer_class = self.get_serializer_class(promt_list)
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)



class GameLevelDetail(generics.RetrieveAPIView):
    queryset = GameLevel.objects.all()
    serializer_class = GameLevelSerialiser


class TeamList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = TeamSerialiser

class TeamDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = TeamSerialiser

class AnswersList(generics.ListAPIView):
    queryset = TeamAnswers.objects.all()
    serializer_class = AnswerSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serialiser):
        serialiser.save(team=self.request.user)

class AnswerDetail(generics.CreateAPIView):
    queryset = TeamAnswers.objects.all()
    serializer_class = AnswerSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serialiser):
        serialiser.save(team=self.request.user)


class GamePlayList(generics.ListAPIView):
    queryset = GamePlay.objects.all()
    serializer_class = GamePlaySerialiser
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class GamePlayDetail(generics.RetrieveAPIView):
    queryset = GamePlay.objects.all()
    serializer_class = GamePlaySerialiser
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class GameSummary(generics.ListAPIView):
    queryset = TeamPlace.objects.all()
    serializer_class = GameSummarySerialiser


# class GameSummary(generics.ListAPIView):
#     Model = GamePlay.objects.all()
#     def get_queryset(self):
#         queryset = self.queryset
#         promt_penalty = 900  # время в секундах
#         answer_penalty = 1800 # время в секундах
#         fields = []
#         for team in User:
#             total_penalty = 0
#             team_stat ={}
#             team_stat['team'] = team
#             levels = {}
#             for level in GameLevel:
#                 level_score = {}
#                 lvl = GamePlay.objects.filter(team=team).filter(level=level).get()
#                 level_status = lvl.level_status
#                 level_wrongs = lvl.wrong_answer_counter
#                 level_promts = lvl.getted_promt_counter
#                 level_score['number'] = level.level
#                 level_score['name'] = level.name
#                 level_score['status'] =level_status
#                 level_score['wrongs'] =level_wrongs
#                 level_score['promts'] =datetime.timedelta(seconds=level_promts)
#                 if level_status == 'DN':
#                     level_time = lvl.level.level_penalty
#                     level_penalty = level_time + level_wrongs*answer_penalty + level_promts*promt_penalty
#                     total_penalty += level_penalty
#                     level_score['penalty'] = datetime.timedelta(seconds=level_penalty)
#                 levels[level.level] = level_score
#                 team_stat['levels'] = levels
#                 team_stat['total_penalty'] = datetime.timedelta(seconds=total_penalty)
#             fields.append(team_stat)
#
#         if isinstance(queryset, QuerySet):
#             queryset = queryset.all()
#         return queryset