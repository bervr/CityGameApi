from .serialisers import GameLevelSerialiser, GamePlaySerialiser
from .models import Game, GameLevel,  WrongAnswers, Team, GamePlay, Promt
from rest_framework import viewsets
from django.contrib.auth.decorators import user_passes_test

# @user_passes_test(lambda u: u.is_active)
class GameLevelViewSet(viewsets.ModelViewSet):
    queryset = GameLevel.objects.all().order_by('name')
    serializer_class = GameLevelSerialiser

# @user_passes_test(lambda u: u.is_active)
class GamePlayViewSet(viewsets.ModelViewSet):
    queryset = GamePlay.objects.all().order_by('game').order_by('team')
    serializer_class = GamePlaySerialiser