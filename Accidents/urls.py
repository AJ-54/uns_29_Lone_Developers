from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name="Accidents"


urlpatterns = [
    path('reports/',accident_reports,name='reports'),
    path('home/',Home,name='home')
]

