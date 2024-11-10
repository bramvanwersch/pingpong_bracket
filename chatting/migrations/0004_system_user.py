
from django.db import migrations

from django.contrib.auth.models import User

from login.models import UserData


def create_system_user(apps, schema_editor):
    new_user = User.objects.create_user(username="System", password="very long and secure password like who cares bruv")
    UserData.objects.create(user=new_user, email='admin@veryimlortantorgenisation.kom')


class Migration(migrations.Migration):

    dependencies = [
        ('chatting', '0003_alter_chatmessage_image'),
    ]

    operations = [
        migrations.RunPython(create_system_user),
    ]