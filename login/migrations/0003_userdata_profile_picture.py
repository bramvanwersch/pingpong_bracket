# Generated by Django 4.2.14 on 2024-10-01 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0002_userdata_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="userdata",
            name="profile_picture",
            field=models.ImageField(default="default_profile_picture.png", upload_to="profile_pictures"),
        ),
    ]
