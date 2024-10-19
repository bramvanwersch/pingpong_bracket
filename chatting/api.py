import datetime

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from chatting.models import ChatMessage, UserMessage
from general_src import image_handling


class NumberNotificationsView(APIView):
    def get(self, request):
        nr_messages = UserMessage.objects.filter(user=request.user, message_read=False).count()
        return JsonResponse({"nr_unread": nr_messages})


class SendImage(APIView):
    def post(self, request, group_id: str):
        file = request.FILES["file"]
        try:
            image_handling.verify_image(file)
        except RuntimeError as e:
            return HttpResponse(str(e), status=400)

        message = ChatMessage.objects.create(
            sender=request.user, image=file, chat_group_id=group_id, message="", date=datetime.datetime.now()
        )
        return JsonResponse({"db_id": message.pk})
