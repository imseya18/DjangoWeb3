from .models import Match, Tournament
from .serializers import Matchserializer, Tournament_group_data
import json

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


def tournament_routine_db(storescore):
    if Tournament.objects.exists():
        print(f" il y a {Tournament.objects.count()} match dans la db")
        for tournament in Tournament.objects.all():
            tnx = storescore.add_tournament(tournament.match_id, tournament.tournament_id, tournament.player1_score,
                                            tournament.player2_score, tournament.player1_id, tournament.player2_id,
                                            tournament.winner_id)
            if tnx is not None:
                print("la TX est reussi je delete")
                delete_tournament_from_db(tournament.tournament_id)

def match_routine_db(storescore):
    if Match.objects.exists():
        print(f" il y a {Match.objects.count()} match dans la db")
        for match in Match.objects.all():
            tnx = storescore.add_match(match.match_id, 0, match.player1_score, match.player2_score,
                                       match.player1_id,
                                       match.player2_id, match.winner_id)
            if tnx is not None:
                print("la TX est reussi je delete")
                delete_match_from_db(match.match_id)

def convert_tournament_to_json(raw_tournament):
    tournament = []
    for match in raw_tournament:
        dictionnaire = {
            "match_id": match[0],
            "player1_score": match[1],
            "player2_score": match[2],
            "player1_id": match[3],
            "player2_id": match[4],
            "winner_id": match[5],
        }
        tournament.append(dictionnaire)
    return json.dumps(tournament, indent=4)


def convert_match_to_json(raw_match):
    match = {
            "match_id": raw_match[0],
            "player1_score": raw_match[1],
            "player2_score": raw_match[2],
            "player1_id": raw_match[3],
            "player2_id": raw_match[4],
            "winner_id": raw_match[5],
        }
    return json.dumps(match, indent=4)
