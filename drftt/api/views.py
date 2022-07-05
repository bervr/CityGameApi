from rest_framework.response import Response

from .serialisers import GameLevelSerialiser, GamePlaySerialiser, GameSerialiser,\
    TeamSerialiser, AnswerSerialiser, PromtSerialiser
from .models import Game, GameLevel, TeamAnswers, GamePlay, Promt
from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from django.db.models import Q, QuerySet


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
        try:
            requested_level = GamePlay.objects.filter(level=level_number).get()
        except:
            requested_level = None
        game_level = get_object_or_404(GameLevel, number=level_number)
        if game_level and game_level.level_active and not requested_level \
                or requested_level.level_status != 'DN':  # проверяем что уровень открыт команде
            promt_number = self.kwargs['num']
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



    # def perform_create(self, serialiser):
    #     serialiser.save(team=self.request.user)
#
# class PromtList(generics.ListAPIView):
#     queryset = Promt.objects.all()
#     serializer_class = PromtSerialiser
#
# class PromtDetail(generics.RetrieveAPIView):
#     queryset = Promt.objects.all()
#     serializer_class = PromtSerialiser




class GamePlayList(generics.ListAPIView):
    queryset = GamePlay.objects.all()
    serializer_class = GamePlaySerialiser
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class GamePlayDetail(generics.RetrieveAPIView):
    queryset = GamePlay.objects.all()
    serializer_class = GamePlaySerialiser
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

