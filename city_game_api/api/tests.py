import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Game, GameLevel


class GameTests(APITestCase):
    def setUp(self) -> None:
        user_test1 = User.objects.create_user(username='test1', password='1qwertY23')
        user_test1.save()
        user_test2 = User.objects.create_user(username='test2', password='4asdfgH56')
        user_test2.save()

        self.one_game = Game.objects.create(
            game_number=1,
            game_name='first_game',
            game_start=datetime.datetime.now(),
            game_finish=datetime.datetime.now() + datetime.timedelta(hours=5)
        )
        self.one_level = GameLevel.objects.create(
            level_of_game=self.one_game,
            number=1,
            geo_lat=123456.12,
            geo_lng=987654.98,
            name='first_level',
            task='first_task',
            answer='1111',
            promt1='1',
            promt2='11',
            promt3='111'
        )

    # def test_post_answer(self):
    #     url = reverse('api:post_answer')
    #     data = {"game": 1,
    #             "level": 1,
    #             "answer": "777"
    #             }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_game_exists(self):
        url = reverse('api:game', kwargs={"game": self.one_game.game_number})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_level_exists(self):
        url = reverse('api:level', kwargs={"game": self.one_game.game_number, "pk": self.one_level.number})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_level_constrait(self):
        url = reverse('api:level', kwargs={"game": self.one_game.game_number, "pk": 18})
        response = self.client.get(url, format='json')
        print(response)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
