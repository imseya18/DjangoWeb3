from django.conf import settings
from django.shortcuts import render
from .StoreInDB import (delete_match_from_db, delete_tournament_from_db, convert_tournament_to_json,
                        convert_match_to_json)
from .models import Match, Tournament
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Matchserializer
from rest_framework import status
from rest_framework.decorators import api_view

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
    tnx = storescore.add_match(37, 0, 1, 2, "jeremy", "johnny", "johnny")
    print(tnx)
    return render(request, "main.html")


#def match_get(request):
#    storescore = settings.STORE_SCORE
#    match = storescore.get_match_by_id(17)
#    if match is not None:
#        match_json = convert_match_to_json(match)
#        print(match_json)
#    return render(request, "main.html")

#class matchApiView(APIView):
#    def get(self, request, match_id):
#        storescore = settings.STORE_SCORE
#        match = storescore.get_match_by_id(match_id)
#        if match is not None:
#            match_json = Matchserializer(data={
#                "match_id": match[0],
#                "tournament_id": 0,
#                "player1_score": match[1],
#                "player2_score": match[2],
#                "player1_id": match[3],
#                "player2_id": match[4],
#                "winner_id": match[5],
#            })
#            if match_json.is_valid():
#                return Response(match_json.data)
#        else:
#            error_message = "No match found with id {0}".format(match_id)
#            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def match_get_api(request,match_id):
    storescore = settings.STORE_SCORE
    match = storescore.get_match_by_id(match_id)
    if match is not None:
        match_json = Matchserializer(data={
            "match_id": match[0],
            "tournament_id": 0,
            "player1_score": match[1],
            "player2_score": match[2],
            "player1_id": match[3],
            "player2_id": match[4],
            "winner_id": match[5],
        })
        if match_json.is_valid():
            return Response(match_json.data)
    else:
        error_message = "No match found with id {0}".format(match_id)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)


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


#def tournament_get(request):
#    storescore = settings.STORE_SCORE
#    tournament = storescore.get_tournament_by_id(5)
#    if tournament is not None:
#        json_tournament = convert_tournament_to_json(tournament)
#        print(json_tournament)
#    return render(request, "main.html")

#class tournamentApiView(APIView):
#    def get(self, request, tournament_id):
#        storescore = settings.STORE_SCORE
#        tournament = storescore.get_tournament_by_id(tournament_id)
#        tournament_json = []
#        if tournament is not None:
#            for match in tournament:
#                match_json = Matchserializer(data={
#                    "match_id": match[0],
#                    "tournament_id": tournament_id,
#                    "player1_score": match[1],
#                    "player2_score": match[2],
#                    "player1_id": match[3],
#                    "player2_id": match[4],
#                    "winner_id": match[5],
#                })
#                if match_json.is_valid():
#                    tournament_json.append(match_json.data)
#            return Response(tournament_json)
#        else:
#            error_message = "No tournament found with id {0}".format(tournament_id)
#            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def tournament_get_api(request, tournament_id):
    storescore = settings.STORE_SCORE
    tournament = storescore.get_tournament_by_id(tournament_id)
    tournament_json = []
    if tournament is not None:
        for match in tournament:
            match_json = Matchserializer(data={
                "match_id": match[0],
                "tournament_id": tournament_id,
                "player1_score": match[1],
                "player2_score": match[2],
                "player1_id": match[3],
                "player2_id": match[4],
                "winner_id": match[5],
            })
            if match_json.is_valid():
                tournament_json.append(match_json.data)
        return Response(tournament_json)
    else:
        error_message = "No tournament found with id {0}".format(tournament_id)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)