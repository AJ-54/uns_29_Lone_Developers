from django.db import models

from django.contrib.auth.models import User

# Create your models here.

Vehicle_Choices = (
            ('Car','Car'),
            ('Bike','Bike'),
            ('Scooty','Scooty')
)


Choice_Types = (
            ('to_family','Family'),
            ('to_hospital','Hospital')
)


class Vehicle(models.Model):
    vehicle = models.CharField(max_length=100,choices=Vehicle_Choices,default='Car')
    user = models.ForeignKey(User,related_name='vehicles',on_delete=models.CASCADE)
    number = models.IntegerField(default=0000)



class Hospital(models.Model):
    hospital_name = models.CharField(max_length=256)
    hospital_longitude = models.IntegerField(default=0)
    hospital_lattitude = models.IntegerField(default=0)
    phone_no = models.IntegerField(default=0)

    def __str__(self) :
        return self.hospital_name



class Accident(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    vehicles = models.ManyToManyField(Vehicle, blank=True,null=True)
    longitude = models.IntegerField(default=0)
    latitude = models.IntegerField(default=0)
    hospital = models.ForeignKey(Hospital,related_name='accidents',on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self) :
        return str(self.id)



class Image(models.Model):
    accident = models.ForeignKey(Accident,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='AccidentImages')



class Notification(models.Model):

        
    accident = models.ForeignKey(Accident,related_name='notifications',on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=256,choices=Choice_Types,default='to_family')
    timestamp = models.DateTimeField(auto_now=True)
    content = models.TextField()






