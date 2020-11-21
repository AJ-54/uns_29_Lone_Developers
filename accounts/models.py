from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.





class Contact(models.Model) :
    user = models.OneToOneField(User,related_name="contact",on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length = 255,blank=True,null=True)
    email = models.EmailField(max_length = 255,blank=True,null=True)
    phone = models.CharField(max_length = 255,blank=True,null=True)




class Profile(models.Model) :
    user = models.OneToOneField(User,related_name="profile",on_delete=models.CASCADE)
    phone = models.IntegerField()
    emergency_contacts = models.ManyToManyField(Contact,related_name="friends_or_family")
    is_verified = models.BooleanField(default=False)

    def __str__(self) :
        return self.user.username


@receiver(post_save,sender=User)
def create_profile_contact(sender,instance,created,**kwargs) :
    if created  :
        profile = Profile.objects.create(user=instance)
        contact = Contact.objects.create(user=instance,name=instance.username,email=instance.email)