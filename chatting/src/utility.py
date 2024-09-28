from datetime import datetime
from typing import Dict, List

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.functions import Lower

from chatting.models import ChatGroupUser, ChatMessage, UserMessage
from login.models import User


def get_user_mapping(exclude_users: List["User"] = None) -> Dict[str, int]:
    names = {u.username: u.pk for u in User.objects.all().order_by(Lower("username"))}
    if exclude_users is None:
        exclude_users = []
    for user in exclude_users:
        del names[user.username]
    return names


def get_group_mapping(requesting_user: User) -> Dict[str, str]:
    user_groups = (
        ChatGroupUser.objects.filter(user=requesting_user).order_by(Lower("group__name")).select_related("group")
    )
    group_names = {ug.group.name: f"{ug.group.pk}" for ug in user_groups}
    return group_names


def send_message(message: str, sender: User, group_id: str):
    other_users = [cgu.user_id for cgu in ChatGroupUser.objects.filter(group_id=group_id)]
    chat_message = ChatMessage.objects.create(
        message=message, sender=sender, date=datetime.now(), chat_group_id=group_id
    )
    UserMessage.objects.create(message=chat_message, message_read=True, user=sender)
    for user_id in other_users:
        UserMessage.objects.create(message=chat_message, message_read=True, user_id=user_id)
    channel_layer = get_channel_layer("default")
    async_to_sync(channel_layer.group_send)(
        group_id,
        {
            "type": "send_message",
            "message": chat_message.message,
            "username": chat_message.sender.username,
            "date": chat_message.date.strftime("%Y-%m-%d %H:%M:%S"),
        },
    )
