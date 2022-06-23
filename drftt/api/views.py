
from .serialisers import GameLevelSerialiser, GamePlaySerialiser, GameSerialiser, TeamSerialiser
from .models import Game, GameLevel,  WrongAnswers, Team, GamePlay, Promt
from rest_framework import viewsets



class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all().order_by('game_number')
    serializer_class = GameSerialiser


class GameLevelViewSet(viewsets.ModelViewSet):
    queryset = GameLevel.objects.all().order_by('name')
    serializer_class = GameLevelSerialiser

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('team_number')
    serializer_class = TeamSerialiser


class GamePlayViewSet(viewsets.ModelViewSet):
    queryset = GamePlay.objects.all()
    serializer_class = GamePlaySerialiser

