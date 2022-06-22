from django.contrib import admin
from .models import Game, GameLevel, CorrectAnswers, WrongAnswers, Team
# Register your models here.

admin.site.register(Game)
admin.site.register(Team)
admin.site.register(GameLevel)
admin.site.register(CorrectAnswers)
admin.site.register(WrongAnswers)

# Register your models here.
