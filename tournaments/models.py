from django.contrib.auth.models import User
from django.db import models


class Tournament(models.Model):
    class Meta:
        db_table = "tournament"

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    start_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)

    class TournamentState(models.Choices):
        NOT_STARTED = "Not started"
        RUNNING = "Running"
        FINISHED = "Finished"

    status = models.CharField(max_length=16, choices=TournamentState.choices)

    class TournamentType(models.Choices):
        SINGLE_ELIMINATION = "Single elimination"
        SEEDING_AND_SINGLE_ELIMINATION = "Seeding and single elimination"

    tournament_type = models.CharField(max_length=64, choices=TournamentType.choices)

    invite_only = models.BooleanField(default=False)


class TournamentGame(models.Model):
    class Meta:
        db_table = "tournament_game"

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    # id of the matches linked to this game
    match_id = models.UUIDField(null=True, default=None)

    # match can be played latest at this time. If not played result is randomed
    end_date = models.DateField()

    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player1", default=None, null=True)
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player2", default=None, null=True)

    class GameType(models.Choices):
        ELIMINATION = "Elimination"
        SEEDING = "Seeding"

    game_type = models.CharField(max_length=32, choices=GameType.choices)

    # in case of a bracket match there is a round and a number of the match in that round. This is sufficient to determine
    # the bracket structure
    round_number = models.IntegerField(null=True, default=None)
    round = models.IntegerField(null=True, default=None)

    # if a round is here purely for convenience sake
    is_dummy = models.BooleanField(default=False)


class TournamentParticipant(models.Model):
    class Meta:
        db_table = "tournament_participant"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    place = models.IntegerField(null=True, default=None)
