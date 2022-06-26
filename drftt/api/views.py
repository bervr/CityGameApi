
from .serialisers import GameLevelSerialiser, GamePlaySerialiser, GameSerialiser,\
    TeamSerialiser, AnswerSerialiser, PromtSerialiser
from .models import Game, GameLevel,  TeamAnswers,  GamePlay, Promt
from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly



class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerialiser

class GameDetail(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerialiser

class GameLevelViewSet(viewsets.ModelViewSet):
    queryset = GameLevel.objects.all().order_by('name')
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

class PromtList(generics.ListAPIView):
    queryset = Promt.objects.all()
    serializer_class = PromtSerialiser

class PromtDetail(generics.RetrieveAPIView):
    queryset = Promt.objects.all()
    serializer_class = PromtSerialiser

class GamePlayList(generics.ListAPIView):
    queryset = GamePlay.objects.all()
    serializer_class = GamePlaySerialiser
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class GamePlayDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GamePlay.objects.all()
    serializer_class = GamePlaySerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

