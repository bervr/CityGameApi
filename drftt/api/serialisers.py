from rest_framework import serializers
from .models import Game, GameLevel,  WrongAnswers, Team, GamePlay

class GameLevelSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameLevel
        fields = ('number', 'name', 'task', 'geo_lat', 'geo_lng',
                  'status',  'started', 'finished')

class GamePlaySerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GamePlay
        fields = ('game', 'level', 'team', )