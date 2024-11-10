from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from chatting.models import ChatGroup, ChatGroupUser, ChatMessage, UserMessage
from chatting.src import utility
from general_src.base_view import BaseView


class ChatRoomView(BaseView):
    def get(self, request, group_id: int = None):
        names = utility.get_user_mapping([request.user])
        group_data = utility.get_group_data(request.user)
        if group_id is not None:
            user_ids = {cgu.user.pk for cgu in ChatGroupUser.objects.filter(group_id=group_id)}
            if request.user.pk not in user_ids:
                return TemplateResponse(request, "403.html")
        messages = ChatMessage.objects.filter(chat_group_id=group_id).order_by("date")[:50]
        # read all the messages when opening a chat
        UserMessage.objects.filter(message__chat_group_id=group_id, user=request.user, message_read=False).update(
            message_read=True
        )
        formatted_messages = []
        for message in messages:
            formatted_messages.append(
                {
                    "message": message.message,
                    "image_url": message.image.url if message.image else "",
                    "username": message.sender.username,
                    "date": message.date.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        return TemplateResponse(
            request,
            "chatroom.html",
            {
                "current": "chatting",
                "names": names,
                "group_id": group_id,
                "group_data": group_data,
                "messages": formatted_messages,
            },
        )


class NewChatRoomView(BaseView):
    def get(self, request, user_ids):
        ids = user_ids.split(";")
        users = User.objects.filter(pk__in=ids).order_by(Lower("username"))
        group = ChatGroup.create_or_get_group(request.user, list(users))
        return redirect(f"/chatroom/{group.pk}")


class ChatChallengeView(BaseView):
    def get(self, request, user_name: str):
        challenge_user = User.objects.get(username=user_name)
        utility.send_system_message([challenge_user], f"{request.user.username} challenges you to a match!")
        return redirect("/chatroom")
