from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
app_name = "accounts"

urlpatterns = [
    path('auth/',auth_view,name="auth"),
    path('login/',user_login,name="login"),
    path('register/',register,name="register"),
    path('send_otp/',send_otp,name="send_otp"),
    path('add_contacts/',add_contact,name="add_contacts"),
    path('add_vehicle/',add_vehicle,name="add_vehicle"),
    path('verify_mobile/',verify_otp,name="verify_mobile"),
     path('complete_profile/',verify_otp,name="complete_profile"),
]

