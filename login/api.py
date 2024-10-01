from django.http import HttpResponse
from rest_framework.views import APIView

from login.models import UserData


class UploadLoginImage(APIView):
    def post(self, request):
        user_data = UserData.objects.get(user=request.user)
        user_data.profile_picture = request.FILES["file"]
        user_data.save()
        return HttpResponse()
