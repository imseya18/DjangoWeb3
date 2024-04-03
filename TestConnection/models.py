from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator


class Tournament(models.Model):
    match_id = ArrayField(models.BigIntegerField(), default=list)
    tournament_id = models.BigIntegerField()
    player1_score = ArrayField(models.BigIntegerField(
            validators=[MinValueValidator(limit_value=0),
                        MaxValueValidator(limit_value=255)]), default=list)
    player2_score = ArrayField(models.BigIntegerField(
            validators=[MinValueValidator(limit_value=0),
                        MaxValueValidator(limit_value=255)]), default=list)
    player1_id = ArrayField(models.CharField(max_length=255), default=list)
    player2_id = ArrayField(models.CharField(max_length=255), default=list)
    winner_id = ArrayField(models.CharField(max_length=255), default=list)


class Match(models.Model):
    match_id = models.BigIntegerField()
    player1_score = models.BigIntegerField()
    player2_score = models.BigIntegerField()
    player1_id = models.CharField(max_length=255)
    player2_id = models.CharField(max_length=255)
    winner_id = models.CharField(max_length=255)
