from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.gis.geoip2 import GeoIP2

from .models import *
from PredictAccident.predict import Classify, predict_accident


# Create your views here.

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie


def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location(ip):
    g = GeoIP2()
    qwe = g.city(ip)
    print(qwe)

@method_decorator(csrf_exempt,name='dispatch')
class AccidentReports(View):
    
    def post(self,request):

        form_data = request.POST
        form_files = None 
        if request.FILES:
            form_files=request.FILES
            image = form_files.get('image')
        number = form_data.get('number')
        

        if(True):
        
            if Vehicle.objects.filter(number=number).exists():
                vehicle =  Vehicle.objects.get(number=number)
                victim = vehicle.user
                emergency_contacts = victim.profile.emergency_contacts.all()
            ip = visitor_ip_address(request)
            get_location(ip)
            return HttpResponse("Done")
            

        else:
            print('You are stupid!')
            return HttpResponse("Stupid")

        
accident_reports = AccidentReports.as_view()
