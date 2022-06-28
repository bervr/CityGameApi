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
        fields = ('number', 'name', 'task', 'geo_lat', 'geo_lng', 'promt=None')


class TeamSerialiser(serializers.ModelSerializer):
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="answers_team", )

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
        model = GameLevel
        fields = ('promt1',)


class GamePlaySerialiser(serializers.ModelSerializer):
    class Meta:
        model = GamePlay
        fields = ('game', 'level', 'team', 'level_status', 'level_started', 'level_finished', 'getted_promt_counter')
