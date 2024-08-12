from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views import View

from login.models import UserData


class LoginView(View):

    def get(self, request):
        return TemplateResponse(request, "login.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return TemplateResponse(request, "login.html", {"message": "Failed to login, invalid credentials"})
        login(request, user)
        return HttpResponseRedirect('/')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login/')


class RegisterView(View):

    def get(self, request):
        return TemplateResponse(request, "register.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        password_again = request.POST['password_again']
        email = request.POST['email']
        if any(v == '' for v in (username, password, password_again)):
            return TemplateResponse(request, "register.html", {"message": "Please fill in all fields"})
        if password_again != password:
            return TemplateResponse(request, "register.html", {"message": "Passwords dont match"})
        try:
            new_user = User.objects.create_user(username=username, password=password)
        except Exception:
            return TemplateResponse(request, "register.html", {"message": "Failed to make account, user already exists"})
        UserData.objects.create(user=new_user, email=email)
        return HttpResponseRedirect('/login/')
