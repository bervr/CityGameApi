import datetime
import os, json

from django.core.management.base import BaseCommand
from api.models import Game, GameLevel
from django.contrib.auth.models import User


JSON_PATH = 'json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):
    def handle(self, *args, **options):
        games =  load_from_json('game')
        Game.objects.all().delete()
        for game in games:
            new_game = Game(**game)
            new_game.game_start = datetime.datetime.now()
            new_game.game_finish = datetime.datetime.now()+datetime.timedelta(hours=9)
            new_game.save()

        levels = load_from_json('gamelevel')
        for level in levels:
            game_id = level['level_of_game_id']
            game_obj = Game.objects.get(game_number=game_id)
            level['level_of_game'] = game_obj
            new_level = GameLevel(**level)
            new_level.save()


        User.objects.create_superuser('bervr', 'bervr@1.local', '12345')
        User.objects.create_user('test-team', 'tt@1.local', '1qwerty23')