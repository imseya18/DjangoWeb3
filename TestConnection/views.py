from django.conf import settings
from django.shortcuts import render
from .StoreInDB import (tournament_routine_db, match_routine_db)
from .models import Match, Tournament
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Matchserializer, Tournament_group_data
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['GET'])
def match_get_api(request,match_id):
    storescore = settings.STORE_SCORE
    match = storescore.get_match_by_id(match_id)
    if match is not None:
        match_json = Matchserializer(data={
            "match_id": match[0],
            "tournament_id": match[1],
            "timestamp": match[2],
            "player1_score": match[3],
            "player2_score": match[4],
            "player1_id": match[5],
            "player2_id": match[6],
            "winner_id": match[7],
        })
        if match_json.is_valid():
            return Response(match_json.data)
    else:
        error_message = "No match found with id {0}".format(match_id)
        return Response({"error": error_message}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])  #Verif token
def match_post_api(request):
    storescore = settings.STORE_SCORE
    match_data = Matchserializer(data=request.data)
    if match_data.is_valid():
        validated_data = match_data.validated_data
        match_routine_db(storescore)
        tnx = storescore.add_match(validated_data['match_id'],
                                   validated_data['tournament_id'],
                                   validated_data['timestamp'],
                                   validated_data['player1_score'],
                                   validated_data['player2_score'],
                                   validated_data['player1_id'],
                                   validated_data['player2_id'],
                                   validated_data['winner_id'])
        if tnx is not None:
            print(tnx['transactionHash'].hex())                                                                 #check TX est bien passer sinon renvoyer une erreur
        return Response(data=match_data.data, status=status.HTTP_201_CREATED)
    else:
        return Response(match_data.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def tournament_get_api(request, tournament_id):
    storescore = settings.STORE_SCORE
    tournament = storescore.get_tournament_by_id(tournament_id)
    tournament_json = []
    if tournament is not None:
        for match in tournament:
            match_json = Matchserializer(data={   #pas sur des valeur a verif
                "match_id": match[0],
                "tournament_id": match[1],
                "timestamp": match[2],
                "player1_score": match[3],
                "player2_score": match[4],
                "player1_id": match[5],
                "player2_id": match[6],
                "winner_id": match[7],
            })
            if match_json.is_valid():
                tournament_json.append(match_json.data)
        return Response(tournament_json)
    else:
        error_message = "No tournament found with id {0}".format(tournament_id)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def tournament_post_api(request):                   #Verif token
    storescore = settings.STORE_SCORE
    raw_tournament = Matchserializer(data=request.data, many=True)
    if raw_tournament.is_valid():
        validated_data = raw_tournament.validated_data
        tournament_data = Tournament_group_data(validated_data)
        tournament_routine_db(storescore)
        balance_before = storescore.get_balance()
        tnx = storescore.add_tournament(tournament_data['match_ids'],
                                        tournament_data['tournament_ids'][0],
                                        tournament_data['timestamp'],
                                        tournament_data['player1_scores'],
                                        tournament_data['player2_scores'],
                                        tournament_data['player1_ids'],
                                        tournament_data['player2_ids'],
                                        tournament_data['winner_ids'])
        print(f" la transaction a couter: {storescore.get_transaction_cost(balance_before, storescore.get_balance())}$")
        print(tnx)                                                              # check TX est bien passer sinon renvoyer une erreur
        return Response(data=validated_data, status=status.HTTP_201_CREATED)
    else:
        return Response(raw_tournament.errors, status=status.HTTP_400_BAD_REQUEST)






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


#def match_add(request):
#    storescore = settings.STORE_SCORE
#    if Match.objects.exists():
#        print(f" il y a {Match.objects.count()} match dans la db")
#        for match in Match.objects.all():
#            tnx = storescore.add_match(match.match_id, 0, match.player1_score, match.player2_score, match.player1_id,
#                                       match.player2_id, match.winner_id)
#            if tnx is not None:
#                print("la TX est reussi je delete")
#                delete_match_from_db(match.match_id)
#    tnx = storescore.add_match(37, 0, 1, 2, "jeremy", "johnny", "johnny")
#    print(tnx)
#    return render(request, "main.html")


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


#def tournament_add(request):
#    storescore = settings.STORE_SCORE
#    if Tournament.objects.exists():
#        print(f" il y a {Tournament.objects.count()} match dans la db")
#        for tournament in Tournament.objects.all():
#            tnx = storescore.add_tournament(tournament.match_id, tournament.tournament_id, tournament.player1_score,
#                                            tournament.player2_score, tournament.player1_id, tournament.player2_id,
#                                            tournament.winner_id)
#            if tnx is not None:
#                print("la TX est reussi je delete")
#                delete_tournament_from_db(tournament.tournament_id)
#    storescore.add_tournament([28, 29, 30, 31], 5, [1, 2, 3, 4], [4, 3, 2, 1], ["jeremy", "Mathieu", "jeremy", "Mathieu"], ["Johnny", "jeremy", "Mathieu", "jeremy"], ["jeremy", "Mathieu", "jeremy", "Mathieu"])
#    return render(request, "main.html")


