from django.conf import settings
from django.shortcuts import render
from .StoreInDB import (delete_match_from_db, delete_tournament_from_db, convert_tournament_to_json,
                        convert_match_to_json)
from .models import Match, Tournament


def match_add(request):
    storescore = settings.STORE_SCORE
    if Match.objects.exists():
        print(f" il y a {Match.objects.count()} match dans la db")
        for match in Match.objects.all():
            tnx = storescore.add_match(match.match_id, 0, match.player1_score, match.player2_score, match.player1_id,
                                       match.player2_id, match.winner_id)
            if tnx is not None:
                print("la TX est reussi je delete")
                delete_match_from_db(match.match_id)
    storescore.add_match(17, 0, 1, 2, "jeremy", "johnny", "johnny")
    return render(request, "main.html")


def match_get(request):
    storescore = settings.STORE_SCORE
    match = storescore.get_match_by_id(17)
    if match is not None:
        match_json = convert_match_to_json(match)
        print(match_json)
    return render(request, "main.html")


def tournament_add(request):
    storescore = settings.STORE_SCORE
    if Tournament.objects.exists():
        print(f" il y a {Tournament.objects.count()} match dans la db")
        for tournament in Tournament.objects.all():
            tnx = storescore.add_tournament(tournament.match_id, tournament.tournament_id, tournament.player1_score,
                                            tournament.player2_score, tournament.player1_id, tournament.player2_id,
                                            tournament.winner_id)
            if tnx is not None:
                print("la TX est reussi je delete")
                delete_tournament_from_db(tournament.tournament_id)
    storescore.add_tournament([28, 29, 30, 31], 5, [1, 2, 3, 4], [4, 3, 2, 1], ["jeremy", "Mathieu", "jeremy", "Mathieu"], ["Johnny", "jeremy", "Mathieu", "jeremy"], ["jeremy", "Mathieu", "jeremy", "Mathieu"])
    return render(request, "main.html")


def tournament_get(request):
    storescore = settings.STORE_SCORE
    tournament = storescore.get_tournament_by_id(5)
    if tournament is not None:
        json_tournament = convert_tournament_to_json(tournament)
        print(json_tournament)
    return render(request, "main.html")
