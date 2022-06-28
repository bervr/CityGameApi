
from .serialisers import GameLevelSerialiser, GamePlaySerialiser, GameSerialiser,\
    TeamSerialiser, AnswerSerialiser, PromtSerialiser
from .models import Game, GameLevel,  TeamAnswers,  GamePlay
from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404


class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerialiser

class GameDetail(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerialiser

class GameLevelList(generics.ListAPIView):
    queryset = GameLevel.objects.all()
    serializer_class = GameLevelSerialiser

class GetPromt(generics.RetrieveAPIView):
    queryset = GameLevel.objects.all()
    serializer_class = PromtSerialiser

    def get(self, request, *args, **kwargs):
        data = super().get(request, *args, **kwargs)
        # opened_promts = data.team_promts
        self.pk = kwargs['pk']
        self.num = kwargs['num']
        self.user = request.user
        # self.queryset = GameLevel.objects.filter(level=self.pk).promt_dict[f'promt{self.num}']
        # GamePlay.one_promt_geted(self.pk, self.num, self.user)
        data['num'] = kwargs['num']
        data['pk'] = kwargs['pk']
        data['user'] = request.user
        return data
    #
    def get_queryset(self):
        data = super().get_queryset()

        self.queryset = GameLevel.objects.filter(level_of_game =self.kwargs['pk']) #.promt_dict[f'promt{self.kwargs["num"]}']
        return self.queryset







class GameLevelDetail(generics.RetrieveAPIView):
    queryset = GameLevel.objects.all()
    serializer_class = GameLevelSerialiser


class TeamList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = TeamSerialiser

class TeamDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = TeamSerialiser

class AnswersList(generics.ListAPIView):
    queryset = TeamAnswers.objects.all()
    serializer_class = AnswerSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self,serialiser):
        serialiser.save(team=self.request.user)

class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamAnswers.objects.all()
    serializer_class = AnswerSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#
# class PromtList(generics.ListAPIView):
#     queryset = Promt.objects.all()
#     serializer_class = PromtSerialiser
#
# class PromtDetail(generics.RetrieveAPIView):
#     queryset = Promt.objects.all()
#     serializer_class = PromtSerialiser




class GamePlayList(generics.ListAPIView):
    queryset = GamePlay.objects.all()
    serializer_class = GamePlaySerialiser
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class GamePlayDetail(generics.RetrieveAPIView):
    queryset = GamePlay.objects.all()
    serializer_class = GamePlaySerialiser
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

