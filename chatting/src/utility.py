import datetime
from typing import Dict, List

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.functions import Lower

from chatting.models import ChatGroup, ChatGroupUser, ChatMessage, UserMessage
from login.models import User


def get_user_mapping(exclude_users: List["User"] = None) -> Dict[str, int]:
    names = {u.username: u.pk for u in User.objects.all().order_by(Lower("username"))}
    if exclude_users is None:
        exclude_users = []
    for user in exclude_users:
        del names[user.username]
        del names["System"]
    return names


def get_group_data(requesting_user: User) -> List[Dict[str, str]]:
    user_groups = (
        ChatGroupUser.objects.filter(user=requesting_user).order_by(Lower("group__name")).select_related("group")
    )
    group_data = []
    covered_ids = set()
    for user_group in user_groups:
        if user_group.group.pk in covered_ids:
            continue
        covered_ids.add(user_group.group.pk)
        nr_unread = UserMessage.objects.filter(
            message__chat_group=user_group.group, user=requesting_user, message_read=False
        )
        nr_unread = nr_unread.count()
        group_data.append({"name": user_group.group.name, "db_id": f"{user_group.group.pk}", "nr_unread": nr_unread})
    return group_data


def send_message(chat_message: ChatMessage, sender: User, group_id: str):
    # also through the websocket
    other_users = [cgu.user_id for cgu in ChatGroupUser.objects.filter(group_id=group_id)]
    for user_id in other_users:
        UserMessage.objects.create(message=chat_message, message_read=user_id == sender.pk, user_id=user_id)
    channel_layer = get_channel_layer("default")
    async_to_sync(channel_layer.group_send)(
        group_id,
        {
            "type": "send_message",
            "message": chat_message.message,
            "image_url": chat_message.image.url if chat_message.image else "",
            "username": chat_message.sender.username,
            "date": chat_message.date.strftime("%Y-%m-%d %H:%M:%S"),
        },
    )


def send_system_message(users: List[User], message: str):
    system_user = User.objects.get(username="System")
    for user in users:
        group = ChatGroup.create_or_get_group(system_user, [user])
        chat_message = ChatMessage.objects.create(
            message=message,
            sender=system_user,
            chat_group_id=group.pk,
            date=datetime.datetime.now(),
        )
        send_message(chat_message, system_user, f"{group.id}")
