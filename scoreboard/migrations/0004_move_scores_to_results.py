import uuid

from django.db import migrations

from scoreboard.models import MatchResult


def convert(apps, schema_editor):
    Scores = apps.get_model('scoreboard', 'Scores')
    scores = Scores.objects.all()
    for score in scores:
        match_id = uuid.uuid4()
        MatchResult.objects.create(player_id=score.player1.pk, opponent_id=score.player2.pk, player_score=score.p1_score, opponents_score=score.p2_score, date=score.date, rate_change=score.p1_rate_change, match_id=match_id)
        MatchResult.objects.create(player_id=score.player2.pk, opponent_id=score.player1.pk, player_score=score.p2_score, opponents_score=score.p1_score, date=score.date, rate_change=score.p2_rate_change, match_id=match_id)


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0003_matchresult'),
    ]

    operations = [
        migrations.RunPython(convert),
    ]
