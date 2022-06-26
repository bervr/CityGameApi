from rest_framework import serializers
from .models import Game, GameLevel, TeamAnswers, GamePlay, Promt
from django.contrib.auth.models import User



class GameSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['game_number', 'game_name', 'game_go', 'game_start', 'game_finish']


class GameLevelSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameLevel
        fields = ('number', 'name', 'task', 'geo_lat', 'geo_lng')


class TeamSerialiser(serializers.ModelSerializer):
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="answers_team",)

    class Meta:
        model = User
        fields = ('id', 'username', 'answers')



class AnswerSerialiser(serializers.ModelSerializer):
    team = serializers.ReadOnlyField(source='team.username')
    class Meta:
        model = TeamAnswers
        fields = ('level', 'team', 'answer', 'created')

class PromtSerialiser(serializers.ModelSerializer):
    # team = serializers.ReadOnlyField(source='team.username')
    class Meta:
        model = Promt
        fields = ('level', 'promt', 'counter')



class GamePlaySerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GamePlay
        fields = ('level', 'team',)
