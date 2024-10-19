import os

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from login.models import UserData

ALLOWED_IMAGE_FORMATS = {"jpg", "png", "gif", "webm", "webp", "apng", "svg", "avif"}


class UploadLoginImage(APIView):
    def post(self, request):
        user_data = UserData.objects.get(user=request.user)
        file = request.FILES["file"]
        try:
            extension = file.name.rsplit(".", 1)[1]
        except IndexError:
            return HttpResponse("Unsupported image format", status=400)
        if extension not in ALLOWED_IMAGE_FORMATS:
            return HttpResponse("Unsupported image format", status=400)
        os.remove(user_data.profile_picture.path)
        user_data.profile_picture = request.FILES["file"]
        user_data.save()
        return HttpResponse()


class GetProfileImage(APIView):
    def get(self, request):
        user_data = UserData.objects.get(user=request.user)
        return JsonResponse({"url": user_data.profile_picture.url})
