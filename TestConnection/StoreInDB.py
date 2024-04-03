from TestConnection.models import *


def add_tournament_to_db(match_id, tournament_id, player1_score, player2_score, player1_name, player2_name, winner):
    new_tournament = Tournament(match_id=match_id, tournament_id=tournament_id, player1_score=player1_score,
                               player2_score=player2_score, player1_name=player1_name, player2_name=player2_name,
                               winner=winner)
    new_tournament.save()

def add_match_to_db(match_id, player1_score, player2_score, player1_name, player2_name, winner):
    new_match = Match(match_id=match_id, player1_score=player1_score, player2_score=player2_score, player1_name=player1_name,
                      player2_name=player2_name, winner=winner)

    new_match.save()
