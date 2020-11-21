from django.db import models

from django.contrib.auth.models import User

# Create your models here.

Choice_Types = (
            ('to_family','Family'),
            ('to_hospital','Hospital')
)

class Vehicle(models.Model):
    user = models.ForeignKey(User,related_name='vehicles',on_delete=models.CASCADE)
    number = models.CharField(max_length=256)

class Hospital(models.Model):
    hospital_name = models.CharField(max_length=256)
    hospital_longitude = models.IntegerField(default=0)
    hospital_latitude = models.IntegerField(default=0)
    phone_no = models.IntegerField(default=0)

    def __str__(self) :
        return self.hospital_name



class Accident(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    vehicles = models.ManyToManyField(Vehicle, blank=True)
    longitude = models.IntegerField(default=0)
    latitude = models.IntegerField(default=0)
    hospital = models.ForeignKey(Hospital,related_name='accidents',on_delete=models.CASCADE)

    def __str__(self) :
        return str(self.id)

def directory_path(instance, filename):
    return "PredictAccident/images/{0}".format(filename)

class Image(models.Model):
    accident = models.ForeignKey(Accident,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to= directory_path)

class Notification(models.Model):   
    accident = models.ForeignKey(Accident,related_name='notifications',on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=256,choices=Choice_Types,default='to_family')
    timestamp = models.DateTimeField(auto_now=True)
    content = models.TextField()






