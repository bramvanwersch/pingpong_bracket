# Generated by Django 4.2.14 on 2024-09-22 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scoreboard", "0004_move_scores_to_results"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Scores",
        ),
    ]
