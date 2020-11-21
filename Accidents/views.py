from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.gis.geoip2 import GeoIP2
<<<<<<< HEAD
=======
from googleplaces import GooglePlaces, types, lang 
import requests 
import json 
from .models import *
>>>>>>> 9a23c7b48946af22005ed40a25a0706d20002ebc
from accounts.models import *
from PredictAccident.predict import Classify
from django.conf import settings

<<<<<<< HEAD
BaseUrl = "https://api.foursquare.com/v2/venues/search?ll=20.3667,72.9&categoryId=4bf58dd8d48988d196941735&client_id=T2FYJME0EU3WFFFFYHXHGLA55NN5MHT524NOY5CLZ53SQS51&client_secret=4RO0J4J4WCRTWUS1G5HIQVWP1ZFK0B1QAHERE0IRRLTF5V0Q&limit=5&v=20180628"

=======

BaseUrl = "https://api.foursquare.com/v2/venues/search?ll=20.3667,72.9&categoryId=4bf58dd8d48988d196941735&client_id=T2FYJME0EU3WFFFFYHXHGLA55NN5MHT524NOY5CLZ53SQS51&client_secret=4RO0J4J4WCRTWUS1G5HIQVWP1ZFK0B1QAHERE0IRRLTF5V0Q&limit=5&v=20180628"


>>>>>>> 9a23c7b48946af22005ed40a25a0706d20002ebc
API_KEY = 'AIzaSyA9Y9cZLZChFBgo4tqLF5Xdpfc_2Og9MiM'


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
    return qwe
<<<<<<< HEAD


=======


>>>>>>> 9a23c7b48946af22005ed40a25a0706d20002ebc
classifier = Classify()
@method_decorator(csrf_exempt,name='dispatch')
class AccidentReports(View):
    
    def post(self,request):

        form_data = request.POST
        form_files=request.FILES
        image = form_files.get('image')
        number = form_data.get('number') 

        # Tracking User IP
        ip = visitor_ip_address(request)
        data = get_location(ip)
        print(data)
        latitude = data['latitude']
        longitude = data['longitude']
        print(ip)
        accident = Accident.objects.create(latitude=latitude, longitude=longitude)
        accident_image = Image.objects.create(image= image,accident = accident)
        path = os.join(BASE_DIR,accident_image.image)
        # for image in images :
        #     accident_image = Image.objects.create(image= image,accident = accident)
        #     path = settings.BASE_DIR +"/media/"+str(accident_image.image)
        #     if(classifier.predict_accident(path)):
        #         genuine_images +=1
            

<<<<<<< HEAD
        if classifier.predict_accident(path):
            print("hi")
=======
        if True or genuine_images == len(images) :
            ip = visitor_ip_address(request)
            print(ip)
            print("hi")
            data = get_location(ip)
            print(data)
            latitude = data['latitude']
            longitude = data['longitude']
>>>>>>> 9a23c7b48946af22005ed40a25a0706d20002ebc
            city = data['city']
            region = data['region']

            if Vehicle.objects.filter(number=number).exists():
                vehicle =  Vehicle.objects.get(number=number)
                victim = vehicle.user
                emergency_contacts = victim.profile.emergency_contacts.all()
                return HttpResponse("Done")
            else :
                return HttpResponse("else")
        else:
            print('You are stupid!')
            return HttpResponse("Stupid")

        
accident_reports = AccidentReports.as_view()

def testing(request):
    return render(request,'test/test.html')

def Home(request):
    return render(request,'home.html')




  
  

