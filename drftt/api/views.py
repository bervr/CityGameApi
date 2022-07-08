from django.db.models import Count

from .serialisers import GameLevelSerialiser, GamePlaySerialiser, GameSerialiser,\
    TeamSerialiser, AnswerSerialiser, PromtSerialiser, GameSummarySerialiser
from .models import Game, GameLevel, TeamAnswers, GamePlay, Promt, TeamPlace
from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404


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
        game = game_level.level_of_game
        try:
            requested_level = GamePlay.objects.filter(team=team).filter(level=level_number).get()
        except:
            GamePlay.start_game_level(game_level, team)
            requested_level = GamePlay.objects.filter(team=team).filter(level=level_number).get()
        if game.check_game_time():  # проверяем что игра активна
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


class AnswerDetail(generics.CreateAPIView):
    queryset = TeamAnswers.objects.all()
    serializer_class = AnswerSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serialiser):
        serialiser.save(team=self.request.user)


class GameSummary(generics.ListAPIView):
    queryset = TeamPlace.objects.all()
    serializer_class = GameSummarySerialiser

    # def get_queryset(self):
    #
    #     q = TeamPlace.objects.all()
    #     new_q = []
    #
    #     for item  in q:
    #         string = {}
    #         place =item.place
    #         a = item
    #         print(a)
    #
    #     return q

# class GameList(generics.ListAPIView):
#     queryset = Game.objects.all()
#     serializer_class = GameSerialiser
#
#
# class GameDetail(generics.RetrieveAPIView):
#     queryset = Game.objects.all()
#     serializer_class = GameSerialiser


# class GamePlayList(generics.ListAPIView):
#     queryset = GamePlay.objects.all()
#     serializer_class = GamePlaySerialiser
#
#
# class GamePlayDetail(generics.RetrieveAPIView):
#     queryset = GamePlay.objects.all()
#     serializer_class = GamePlaySerialiser

#
# class AnswersList(generics.ListAPIView):
#     queryset = TeamAnswers.objects.all()
#     serializer_class = AnswerSerialiser
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serialiser):
#         serialiser.save(team=self.request.user)