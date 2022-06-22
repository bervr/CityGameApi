from rest_framework import serializers
from .models import Game, GameLevel, CorrectAnswers, WrongAnswers, Team

class GameLevelSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameLevel
        fields = ('number', 'name', 'task', 'geo_lat', 'geo_lng')