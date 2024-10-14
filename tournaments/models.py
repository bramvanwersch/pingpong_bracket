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

    status = models.CharField(max_length=16, choices=TournamentState.choices, default=TournamentState.NOT_STARTED)

    class TournamentType(models.Choices):
        SINGLE_ELIMINATION = "Single elimination"
        # DOUBLE_ELIMINATION = "Double elimination"
        SEEDING_AND_SINGLE_ELIMINATION = "Seeding and single elimination"
        # SEEDING_AND_DOUBLE_ELIMINATION = "Seeding and double elimination"

    tournament_type = models.CharField(max_length=64, choices=TournamentType.choices)

    invite_only = models.BooleanField(default=False)


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


class TournamentParticipant(models.Model):
    class Meta:
        db_table = "tournament_participant"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    place = models.IntegerField(null=True, default=None)
