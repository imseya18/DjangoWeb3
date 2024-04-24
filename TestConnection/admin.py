from django.contrib import admin

from TestConnection.models import Tournament, Match


# Register your models here.
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'tournament_id', 'timestamp', 'player1_score', 'player2_score',
                    'player1_id', 'player2_id', 'winner_id')


class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'tournament_id', 'timestamp', 'player1_score', 'player2_score',
                    'player1_id', 'player2_id', 'winner_id')


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Match, MatchAdmin)