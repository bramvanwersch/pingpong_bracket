from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


class UserData(Model):

    class Meta:
        db_table = "user_data"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=1000)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    email = models.EmailField(default=None, null=True)

    @property
    def total(self) -> int:
        return self.wins + self.losses + self.ties
