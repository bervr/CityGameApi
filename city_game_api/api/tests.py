import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Game, GameLevel, GamePlay
import factory
import logging

logger = logging.getLogger('factory')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    game_name = factory.Faker("name")
    game_start = factory.LazyFunction(datetime.datetime.now)
    game_finish = factory.LazyFunction(datetime.datetime.now)


class GameLevelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GameLevel

    number = factory.Sequence(lambda n: '%d' % n)
    level_of_game = factory.SubFactory(GameFactory)
    geo_lat = factory.Faker("latitude")
    geo_lng = factory.Faker("longitude")
    name = factory.Faker("name")
    task = factory.Faker("sentence")
    answer = factory.Faker("name")


class GamePlayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GamePlay

    game = factory.SubFactory(GameFactory)
    level = factory.SubFactory(GameLevelFactory)
    team = factory.SubFactory(User)


class GameTests(APITestCase):
    def setUp(self) -> None:
        user_test1 = User.objects.create_user(username='test1', password='1qwertY23')
        user_test1.save()
        user_test2 = User.objects.create_user(username='test2', password='4asdfgH56')
        user_test2.save()
        self.one_game = GameFactory()
        with factory.debug():
            self.one_level = GameLevelFactory(level_of_game=self.one_game, number=1, answer=1111, promt1=1)
            GamePlayFactory(game=self.one_game, level=self.one_level, team=user_test1)

    # def test_post_answer(self):
    #     url = reverse('api:post_answer')
    #     data = {"game": 1,
    #             "level": 1,
    #             "answer": "777"
    #             }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_game_exists(self):
        url = reverse('api:game', kwargs={"game": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_game_not_exists(self):
        url = reverse('api:game', kwargs={"game": 50})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_level_exists(self):
        url = reverse('api:level', kwargs={"game": 1, "pk": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_level_constrait(self):
        url = reverse('api:level', kwargs={"game": 1, "pk": 18})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_play_get_promt(self):
        url = reverse('api:promt', kwargs={"game": 1, "pk": 1, "num": 1})
        response = self.client.get(url, format='json')
        user = User.objects.get(username='test1')
        client = APIClient()
        client.force_authenticate(user=user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "1")
