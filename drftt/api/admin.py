from django.contrib import admin
from .models import Game, GameLevel, WrongAnswers, Team, GamePlay, Promt
# Register your models here.

admin.site.register(Game)
admin.site.register(Team)
admin.site.register(GameLevel)
admin.site.register(WrongAnswers)
admin.site.register(GamePlay)
admin.site.register(Promt)

# Register your models here.
