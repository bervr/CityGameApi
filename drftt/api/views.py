from .serialisers import GameLevelSerialiser
from .models import Game, GameLevel, CorrectAnswers, WrongAnswers, Team
from rest_framework import viewsets

class GameLevelViewSet(viewsets.ModelViewSet):
    queryset = GameLevel.objects.all().order_by('name')
    serializer_class = GameLevelSerialiser