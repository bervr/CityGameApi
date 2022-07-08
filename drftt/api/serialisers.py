import datetime

from rest_framework import serializers
from .models import Game, GameLevel, TeamAnswers, GamePlay, Promt, TeamPlace
from django.contrib.auth.models import User



class GameSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['game_number', 'game_name', 'game_go', 'game_start', 'game_finish']


class GameLevelSerialiser(serializers.ModelSerializer):
    class Meta:
        model = GameLevel
        fields = ['number', 'name', 'task', 'geo_lat', 'geo_lng',]


class TeamSerialiser(serializers.ModelSerializer):
    answers_team = serializers.PrimaryKeyRelatedField(many=True, read_only=True, )

    class Meta:
        model = User
        fields = ('id', 'username', 'answers_team')
        #todo починить вывод ответов или убить это сериалайзер


class AnswerSerialiser(serializers.ModelSerializer):
    team = serializers.ReadOnlyField(source='team.username')

    class Meta:
        model = TeamAnswers
        fields = ('game', 'level', 'team', 'answer', 'created')


class PromtSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Promt
        fields = []


class GamePlaySerialiser(serializers.ModelSerializer):
    class Meta:
        model = GamePlay
        fields = ('game', 'level', 'team', 'level_status', 'level_started', 'level_finished', 'getted_promt_counter')

class GameSummarySerialiser(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    levelname = serializers.ReadOnlyField(source='level.name')
    level_penalty = serializers.ReadOnlyField(source='level_penalty ')
    class Meta:
        model = TeamPlace
        fields = ('summ_penalty', 'user', 'level', 'levelname', 'level_status', 'level_penalty', 'total_finished')



