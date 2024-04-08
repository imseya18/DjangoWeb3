from .models import Match, Tournament


def add_tournament_to_db(match_id, tournament_id, player1_score, player2_score, player1_id, player2_id, winner_id):
    if not Tournament.objects.filter(tournament_id=tournament_id):
        print("Je stock le tournois dans la DB")
        new_tournament = Tournament(match_id=match_id, tournament_id=tournament_id, player1_score=player1_score,
                                player2_score=player2_score, player1_id=player1_id, player2_id=player2_id,
                                winner_id=winner_id)
        new_tournament.save()
    else:
        print("tournois exist deja je ne le stock pas")


def delete_tournament_from_db(tournament_id):
    if Tournament.objects.filter(tournament_id=tournament_id).exists():
        tournament = Tournament.objects.get(tournament_id=tournament_id)
        tournament.delete()
        print(f"tournament {tournament_id} supprimer de la db")
    else:
        print(f"tournament {tournament_id} n'est pas dans la db, pas de suppression")


def add_match_to_db(match_id, player1_score, player2_score, player1_id, player2_id, winner_id):
    if not Match.objects.filter(match_id=match_id).exists():
        print("Je stock le match dans la DB")
        new_match = Match(match_id=match_id, player1_score=player1_score, player2_score=player2_score, player1_id=player1_id,
                          player2_id=player2_id, winner_id=winner_id)
        new_match.save()
    else:
        print("match exist deja je ne le stock pas")


def delete_match_from_db(match_id):
    if Match.objects.filter(match_id=match_id).exists():
        match = Match.objects.get(match_id=match_id)
        match.delete()
        print(f"match {match_id} supprimer de la db")
    else:
        print(f"match {match_id} n'est pas dans la db, pas de suppression")
