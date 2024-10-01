from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from login.models import UserData


class UploadLoginImage(APIView):
    def post(self, request):
        user_data = UserData.objects.get(user=request.user)
        user_data.profile_picture = request.FILES["file"]
        user_data.save()
        return HttpResponse()


class GetProfileImage(APIView):
    def get(self, request):
        user_data = UserData.objects.get(user=request.user)
        return JsonResponse({"url": user_data.profile_picture.url})
