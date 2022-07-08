import os, json

from django.core.management.base import BaseCommand
from api.models import Game, GameLevel, GamePlay, Promt
from django.contrib.auth.models import User


JSON_PATH = 'json'

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), encoding='utf-8') as f:
        return json.load(f)
#
class Command(BaseCommand):
    def handle(self, *args, **options):
        games =  load_from_json('game')
        Game.objects.all().delete()
        for game in games:
            new_game = Game(**game)
            new_game.save()

        levels = load_from_json('gamelevel')
        for level in levels:
            game_id = level['level_of_game_id']
            game_obj = Game.objects.get(game_number=game_id)
            level['level_of_game'] = game_obj
            new_level = GameLevel(**level)
            new_level.save()

        promts = load_from_json('promt')
        for promt in promts:
            level_id = promt['level_id']
            level_obj = GameLevel.objects.get(number=level_id)
            promt['level'] = level_obj
            new_promt = Promt(**promt)
            new_promt.save()

        User.objects.create_superuser('bervr', 'bervr@1.local', '12345')
        User.objects.create_user('test-team', 'tt@1.local', '1qwerty23')