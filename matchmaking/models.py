from django.contrib.auth.models import User
from django.db import models


class MatchRequests(models.Model):

    class Meta:
        db_table = "match_requests"

    asker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mask_asker')
    start = models.DateTimeField()
    end = models.DateTimeField()
    challenger = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name='mask_challenger')

    class MatchTypes(models.TextChoices):
        CHALLENGE = "Challenge"
        REQUEST = "Match request"

    match_type = models.CharField(max_length=32, choices=MatchTypes.choices)