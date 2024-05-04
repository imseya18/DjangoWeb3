from django.conf import settings
from django.shortcuts import render
from .StoreInDB import (tournament_routine_db, match_routine_db, get_match_by_playerId_db, get_tx_from_db)
from .models import Match, Tournament
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Matchserializer, Tournament_group_data, SendDbMatchToSerializer
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['GET'])
def match_get_api(request,match_id):
    storescore = settings.STORE_SCORE
    match = storescore.get_match_by_id(match_id)
    if match is not None:
        match_json = SendDbMatchToSerializer(match)
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
        return storescore.add_match(validated_data, False)
    else:
        return Response(match_data.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def tournament_get_api(request, tournament_id):
    storescore = settings.STORE_SCORE
    tournament = storescore.get_tournament_by_id(tournament_id)
    tournament_json = []
    if tournament is not None:
        for match in tournament:
            match_json = SendDbMatchToSerializer(match)
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
        return storescore.add_tournament(tournament_data, False)
    else:
        return Response(raw_tournament.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def GetMatchByPlayerApi(request, player_id):
    storescore = settings.STORE_SCORE
    matchs_from_BC = storescore.get_match_by_player(player_id)
    matchs_from_DB = get_match_by_playerId_db(player_id)
    print(f'valeur de match_BC: {matchs_from_BC}')
    print(f'valeur de match_DB: {matchs_from_DB}')
    if matchs_from_BC is None and matchs_from_DB is None:
        error_message = "No matchs found with player_id {0}".format(player_id)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if matchs_from_DB is None:
            matchs_from_DB = []
        return_matchs = []
        if matchs_from_BC is not None:
            for match in matchs_from_BC:
                match_json = SendDbMatchToSerializer(match)
                if match_json.is_valid():
                    match_data = match_json.data
                    match_data['from_blockchain'] = True
                    match_data['tx_hash'] = get_tx_from_db(match_data)
                    return_matchs.append(match_data)
        return_matchs = return_matchs + matchs_from_DB
        return Response(return_matchs, status=status.HTTP_200_OK)


@api_view(['get'])
def test(request, player_id):
    get_match_by_playerId_db(player_id)

