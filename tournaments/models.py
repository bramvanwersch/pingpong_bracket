from django.contrib.auth.models import User
from django.db import models


class Tournament(models.Model):

    class Meta:
        db_table = "tournament"

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField()

    class TournamentState(models.Choices):
        NOT_STARTED = 'Not started'
        RUNNING = 'Running'
        FINISHED = 'Finished'

    status = models.CharField(max_length=16, choices=TournamentState.choices)

    class TournamentType(models.Choices):
        SINGLE_ELIMINATION = "Single elimination"
        DOUBLE_ELIMINATION = "Double elimination"
        SEATING_AND_SINGLE_ELIMINATION = "Seating and single elimination"
        SEATING_AND_DOUBLE_ELIMINATION = "Seating and double elimination"

    tournament_type = models.CharField(max_length=64, choices=TournamentType.choices)


class TournamentGame(models.Model):

    class Meta:
        db_table = "tournament_game"

    # id of the matches linked to this game
    match_id = models.UUIDField(null=True, default=None)

    # match can be played earliest at this time
    start_date = models.DateField()
    # match can be played latest at this time. If not played result is randomed
    end_date = models.DateField()

    # in case of a bracket match there is a round and a number of the match in that round. This is sufficient to determine
    # the bracket structure
    round_number = models.IntegerField(null=True, default=None)
    round = models.IntegerField(null=True, default=None)
