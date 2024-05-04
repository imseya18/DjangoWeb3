from .models import Match, Tournament,TxHash
from .serializers import Matchserializer, Tournament_group_data
import json
from django.db.models import Q
from tabulate import tabulate

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
            return_code = storescore.add_tournament(tournament_dict, True)
            if return_code is True:
                print("la TX est reussi je delete")
                delete_tournament_from_db(tournament.tournament_id)


def match_routine_db(storescore):
    if Match.objects.exists():
        print(f" il y a {Match.objects.count()} match dans la db")
        for match in Match.objects.all():
            match_dict = match.__dict__
            match_dict.pop('_state')
            match_dict.pop('id')
            return_code = storescore.add_match(match_dict, True)
            if return_code is True:
                print("la TX est reussi je delete")
                delete_match_from_db(match.match_id)


def get_match_by_playerId_db(playerId):
    matches = Match.objects.filter(Q(player1_id=playerId) | Q(player2_id=playerId))
    if matches.exists():
        match_list = list(matches.values())
        serialize = Matchserializer(data=match_list, many=True)
        if serialize.is_valid():
            validate_data = serialize.validated_data
            for match in validate_data:
                match['from_blockchain'] = False
            print(tabulate(validate_data, headers="keys", tablefmt="grid"))
            return validate_data
    else:
        return None


def add_tx_to_db(match_id, tournament_id, tx):
    new_tnx = TxHash(match_id=match_id, tournament_id=tournament_id, tx_hash=tx)
    new_tnx.save()


def get_tx_from_db(data):
    if data['tournament_id'] == 0 and TxHash.objects.filter(match_id=data['match_id']).exists():
        tnx = TxHash.objects.get(match_id=data['match_id'])
        return tnx.tx_hash
    elif data['tournament_id'] != 0 and TxHash.objects.filter(tournament_id=data['tournament_id']).exists():
        tnx = TxHash.objects.get(tournament_id=data['tournament_id'])
        return tnx.tx_hash
    else:
        return None
