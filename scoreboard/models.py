from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, QuerySet, Q


class Result:

    WIN = 'Win'
    LOSS = 'Loss'
    TIE = 'Tie'


class MatchResult(Model):

    class Meta:
        db_table = "match_result"

    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player')
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opponent')
    player_score = models.IntegerField()
    opponents_score = models.IntegerField()
    date = models.DateTimeField()
    rate_change = models.FloatField()
    match_id = models.UUIDField()

    @classmethod
    def get_player_scores(cls, player: User, opponent: User = None) -> QuerySet["MatchResult"]:
        queryset = cls.objects.filter(player=player)
        if opponent is None:
            return queryset.order_by("-date")
        return queryset.filter(opponent=opponent).order_by("-date")

    def get_result(self) -> str:
        if self.player_score > self.opponents_score:
            return Result.WIN
        if self.opponents_score > self.player_score:
            return Result.LOSS
        return Result.TIE
