# Generated by Django 5.1 on 2024-08-11 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchrequests',
            name='actual_time',
        ),
        migrations.AddField(
            model_name='matchrequests',
            name='match_type',
            field=models.CharField(choices=[('Challenge', 'Challenge'), ('Match request', 'Request')], default='Match request', max_length=32),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Challenges',
        ),
    ]