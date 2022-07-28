from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
# from city_game_api.api.models import Game


class GameTests(APITestCase):
    def test_start_game(self):
        url = reverse('game')
        response = self.client.get(url, format('json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
