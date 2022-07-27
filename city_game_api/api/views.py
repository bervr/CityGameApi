from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serialisers import GameLevelSerialiser, AnswerSerialiser, GameSummarySerialiser, PromtSerialiser
from .models import GameLevel, TeamAnswers, GamePlay, Game
from rest_framework import generics, permissions
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404


class GameLevelList(generics.ListAPIView):
    queryset = GameLevel.objects.all()
    serializer_class = GameLevelSerialiser

    def get_queryset(self):
        data = super().get_queryset()
        game_num = self.kwargs['game']
        game = get_object_or_404(Game, game_number=game_num)
        data = data.filter(level_of_game=game)
        game.check_game_time()
        return data


class GameLevelDetail(generics.ListAPIView):
    queryset = GameLevel.objects.all()
    serializer_class = GameLevelSerialiser

    def get_queryset(self):
        data = super().get_queryset()
        game_num = self.kwargs['game']
        level_num = self.kwargs['pk']
        game = get_object_or_404(Game, game_number=game_num)
        game.check_game_time()
        data = data.filter(level_of_game=game).filter(number=level_num)
        return data


class GetPromt(generics.ListAPIView):
    queryset = GameLevel.objects.all()
    serializer_class = PromtSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        level_number = self.kwargs['pk']
        game_number = self.kwargs['game']
        queryset = queryset.filter(level_of_game=game_number).filter(number=level_number)
        return queryset

    def get_serializer_class(self, list=[]):
        data = super().get_serializer_class()
        setattr(data.Meta, 'fields', list)  # грязно, но по-другому не придумал
        return data

    def get_serializer(self, *args, **kwargs):
        team = self.request.user
        level_number = self.kwargs['pk']
        promt_number = self.kwargs['num']
        game_number = self.kwargs['game']
        game_level = get_object_or_404(GameLevel, number=level_number, level_of_game=game_number)
        game = game_level.level_of_game
        game.check_game_time()  # проверяем что игра активна
        try:
            requested_level = GamePlay.objects.filter(team=team).filter(level=game_level).get()
        except:
            GamePlay.start_game_level(game_level, team)
            requested_level = GamePlay.objects.filter(team=team).filter(level=level_number).get()
        if game.check_game_time():
            if game_level and game_level.level_active or requested_level.level_status != 'DN':  # проверяем что уровень открыт команде или не закончен
                promt_list = [f'promt{promt_number}']
                GamePlay.registry_promt(game_level, team, promt_number)  # регистрируем выдачу подсказки
        else:
            promt_list = []
        serializer_class = self.get_serializer_class(promt_list)
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class AnswerDetail(generics.CreateAPIView):
    queryset = TeamAnswers.objects.all()
    serializer_class = AnswerSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serialiser):
        serialiser.save(team=self.request.user)


@api_view(['GET'])
def game_summary(request, game):
    instance = Game.get_places(get_object_or_404(Game, game_number=game))
    serialiser = GameSummarySerialiser(instance)
    return Response(serialiser.data)


