import hashlib
from typing import List

from django.contrib.auth.models import User
from django.db import models


class ChatGroup(models.Model):
    class Meta:
        db_table = "chat_group"

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name="creator")
    users = models.ManyToManyField(User, related_name="users", through="chatting.ChatGroupUser")
    name = models.CharField(max_length=128)
    # this id identifies who is in the group --> as to not create double groups
    group_composition_id = models.BigIntegerField()

    @classmethod
    def create_or_get_group(cls, creator: User, other_users: List[User]) -> "ChatGroup":
        other_users.append(creator)
        usernames = sorted(u.username for u in other_users)
        name = f"Chat between {', '.join(usernames[:-1])} and {usernames[-1]}"
        composition_id = int(hashlib.md5(name.encode()).hexdigest(), 16) % 1_000_000_000_000
        existing_group = ChatGroup.objects.filter(group_composition_id=composition_id).first()
        if existing_group is not None:
            return existing_group
        group = ChatGroup.objects.create(creator=creator, name=name[:128], group_composition_id=composition_id)
        for user in other_users:
            ChatGroupUser.objects.create(user_id=user.id, group_id=group.pk)
        return group


class ChatGroupUser(models.Model):
    class Meta:
        db_table = "chat_group_user"

    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ChatMessage(models.Model):
    class Meta:
        db_table = "chat_message"

    message = models.CharField(max_length=512)
    date = models.DateTimeField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    receivers = models.ManyToManyField(User, through="chatting.UserMessage", related_name="receivers")


class UserMessage(models.Model):
    class Meta:
        db_table = "user_message"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    message_read = models.BooleanField(default=False)

    def __str__(self):
        return f"<User: {self.user.username}, Message: {self.message}, ID: {self.pk}>"
