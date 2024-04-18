from rest_framework import serializers


class Matchserializer(serializers.Serializer):
    match_id = serializers.IntegerField()
    tournament_id = serializers.IntegerField()
    player1_score = serializers.IntegerField()
    player2_score = serializers.IntegerField()
    player1_id = serializers.CharField()
    player2_id = serializers.CharField()
    winner_id = serializers.CharField()
