from django.urls import path
from login import views

urlpatterns = [
    path('', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('register/', views.RegisterView.as_view()),
]
