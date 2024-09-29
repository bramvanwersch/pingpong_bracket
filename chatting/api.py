from django.http import JsonResponse
from rest_framework.views import APIView

from chatting.models import UserMessage


class NumberNotificationsView(APIView):
    def get(self, request):
        nr_messages = UserMessage.objects.filter(user=request.user, message_read=False).count()
        return JsonResponse({"nr_unread": nr_messages})
