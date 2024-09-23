from django.contrib.auth.models import User
from django.db import models


class ChatMessage(models.Model):

    class Meta:
        db_table = "chat_message"

    message = models.CharField(max_length=512)
    date = models.DateTimeField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receivers = models.ManyToManyField(User, through="chatting.UserMessage", related_name='receivers')


class UserMessage(models.Model):
    class Meta:
        db_table = "user_message"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    message_read = models.BooleanField(default=False)
