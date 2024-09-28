from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.template.response import TemplateResponse
from django.views import View


class ChatRoomView(View):

    def get(self, request, room_name: str = "general"):
        names = {u.username: f"u_{u.pk}" for u in User.objects.all().order_by(Lower('username'))}
        del names[request.user.username]
        return TemplateResponse(request, "chatroom.html",
                                {"current": "chatting", "names": names, "room_name": room_name})
