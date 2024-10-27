import os

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from general_src import image_handling
from login.models import UserData


class UploadLoginImage(APIView):
    def post(self, request):
        user_data = UserData.objects.get(user=request.user)
        file = request.FILES["file"]
        try:
            image_handling.verify_image(file)
        except RuntimeError as e:
            return HttpResponse(str(e), status=400)
        if user_data.profile_picture.name != "default_profile_picture.png":
            try:
                os.remove(user_data.profile_picture.path)
            except FileNotFoundError:
                pass
        user_data.profile_picture = file
        user_data.save()
        return HttpResponse()


class GetProfileImage(APIView):
    def get(self, request):
        user_data = UserData.objects.get(user=request.user)
        return JsonResponse({"url": user_data.profile_picture.url})
