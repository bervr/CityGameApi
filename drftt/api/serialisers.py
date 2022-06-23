from rest_framework import serializers
from .models import Game, GameLevel, WrongAnswers, Team, GamePlay


class GameSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('game_number', 'game_name', 'game_go', 'game_start', 'game_finish')


class GameLevelSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameLevel
        fields = ( 'number', 'name', 'task', 'geo_lat', 'geo_lng',
                  'status', 'started', 'finished',)


class TeamSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ('team_number', 'team_name',)


class GamePlaySerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GamePlay
        fields = ('level', 'team',)
