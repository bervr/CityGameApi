import datetime
from rest_framework import serializers
from .models import Game, GameLevel, TeamAnswers, GamePlay
from django.contrib.auth.models import User


class GameSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['game_number', 'game_name', 'game_go', 'game_start', 'game_finish']


class GameLevelSerialiser(serializers.ModelSerializer):
    class Meta:
        model = GameLevel
        fields = ['number', 'name', 'task', 'geo_lat', 'geo_lng']


class TeamSerialiser(serializers.ModelSerializer):

    answers_team = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
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
        model = GameLevel
        fields = []


class GamePlaySerialiser(serializers.ModelSerializer):
    class Meta:
        model = GamePlay
        fields = ('game', 'level', 'team', 'level_status', 'level_started', 'level_finished', 'getted_promt_counter')


class GameSummarySerialiser(serializers.BaseSerializer):
    def get_human_time(self, time):
        seconds = int(time)
        millis = str(time-seconds).strip('0')
        human_time = str(datetime.timedelta(seconds=seconds))
        return human_time+millis

    def to_representation(self, instance):
        return instance

