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
            "player1_score": match[6],
            "player2_score": match[7],
            "player1_id": match[3],
            "player2_id": match[4],
            "winner_id": match[5],
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
        return storescore.add_match(validated_data)
    else:
        return Response(match_data.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def tournament_get_api(request, tournament_id):
    storescore = settings.STORE_SCORE
    tournament = storescore.get_tournament_by_id(tournament_id)
    tournament_json = []
    if tournament is not None:
        for match in tournament:
            match_json = Matchserializer(data={
                "match_id": match[0],
                "tournament_id": match[1],
                "timestamp": match[2],
                "player1_score": match[6],
                "player2_score": match[7],
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
        if tnx is not None:
            print(tnx['transactionHash'].hex())
            return Response(data=validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(raw_tournament.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def GetMatchByPlayerApi(request, player_id):
    storescore = settings.STORE_SCORE
    matchs = storescore.get_match_by_player(player_id)
    return_matchs = []
    if matchs is not None:
        for match in matchs:
            match_json = Matchserializer(data={
                "match_id": match[0],
                "tournament_id": match[1],
                "timestamp": match[2],
                "player1_score": match[6],
                "player2_score": match[7],
                "player1_id": match[3],
                "player2_id": match[4],
                "winner_id": match[5],
            })
            if match_json.is_valid():
                return_matchs.append(match_json.data)
        return Response(return_matchs)
    else:
        error_message = "No matchs found with player_id {0}".format(player_id)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)