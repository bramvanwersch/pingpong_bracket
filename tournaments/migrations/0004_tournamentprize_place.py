# Generated by Django 4.2.14 on 2024-10-27 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_alter_tournament_tournament_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentprize',
            name='place',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
