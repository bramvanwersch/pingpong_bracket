from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, QuerySet, Q


class Scores(Model):

    class Meta:
        db_table = "scores"

    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player1")
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player2")
    p1_score = models.IntegerField()
    p2_score = models.IntegerField()
    p1_rate_change = models.FloatField(default=0.0)
    p2_rate_change = models.FloatField(default=0.0)
    date = models.DateTimeField()

    @classmethod
    def get_player_scores(cls, player: User) -> QuerySet["Scores"]:
        return cls.objects.filter(Q(player1=player) | Q(player2=player))