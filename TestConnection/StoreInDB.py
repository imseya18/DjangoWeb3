from .models import Match, Tournament
from .serializers import Matchserializer, Tournament_group_data
import json


def add_tournament_to_db(tournament_data):
    if not Tournament.objects.filter(tournament_id=tournament_data['tournament_id']).exists():
        print("Je stock le tournois dans la DB")
        new_tournament = Tournament(**tournament_data)
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


def add_match_to_db(match_data):
    if not Match.objects.filter(match_id=match_data['match_id']).exists():
        print("Je stock le match dans la DB")
        new_match = Match(**match_data)
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
        print(f" il y a {Tournament.objects.count()} tournois dans la db")
        for tournament in Tournament.objects.all():
            tournament_dict = tournament.__dict__
            tournament_dict.pop('_state')
            tournament_dict.pop('id')
            tnx = storescore.add_tournament(tournament_dict)
            if tnx is not None:
                print("la TX est reussi je delete")
                delete_tournament_from_db(tournament.tournament_id)

def match_routine_db(storescore):
    if Match.objects.exists():
        print(f" il y a {Match.objects.count()} match dans la db")
        for match in Match.objects.all():
            match_dict = match.__dict__
            match_dict.pop('_state')
            match_dict.pop('id')
            tnx = storescore.add_match(match_dict)
            if tnx is not None:
                print("la TX est reussi je delete")
                delete_match_from_db(match.match_id)
