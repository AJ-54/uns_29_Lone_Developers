from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
app_name = "accounts"

urlpatterns = [
    path('login/',user_login,name="login"),
    path('register/',register,name="register"),
    path('send_otp/<int:pk>/',send_otp,name="send_otp"),
    path('add_contacts/',verify_otp,name="add_contacts"),
]

