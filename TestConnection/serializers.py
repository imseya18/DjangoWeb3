from rest_framework import serializers
from django.core.validators import MinValueValidator

class Matchserializer(serializers.Serializer):
    match_id = serializers.IntegerField(validators=[MinValueValidator(0)])
    tournament_id = serializers.IntegerField(validators=[MinValueValidator(0)])
    timestamp = serializers.IntegerField(validators=[MinValueValidator(0)])
    player1_score = serializers.IntegerField(validators=[MinValueValidator(0)])
    player2_score = serializers.IntegerField(validators=[MinValueValidator(0)])
    player1_id = serializers.IntegerField(validators=[MinValueValidator(0)])
    player2_id = serializers.IntegerField(validators=[MinValueValidator(0)])
    winner_id = serializers.IntegerField(validators=[MinValueValidator(0)])

def Tournament_group_data(validated_data):
    matches = zip(*[item.values() for item in validated_data])
    match_ids, tournament_ids, timestamp, player1_scores, player2_scores, player1_ids, player2_ids, winner_ids = map(list, matches)

    tournament_dict = {
        'match_ids': match_ids,
        'tournament_ids': tournament_ids,
        'timestamp': timestamp,
        'player1_scores': player1_scores,
        'player2_scores': player2_scores,
        'player1_ids': player1_ids,
        'player2_ids': player2_ids,
        'winner_ids': winner_ids
    }
    return tournament_dict