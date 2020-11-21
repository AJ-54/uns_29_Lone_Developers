from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
# Create your views here.
from django.views import View
import pyotp
from django.http import HttpResponse
import os
from Accidents.models import *
from accounts.models import *
from django.conf import settings
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from django.utils.decorators import method_decorator
#voice login
# username, password = "daksh999168@gmail.com", "winnerwinner"
# voice = Voice()
# voice.login(username, password)

#9991689861
def send_otp(request) :
    if request.session.get('session_otps',True) :
            request.session['session_otps'] = []
    
    otp = pyotp.TOTP(pyotp.random_base32()).now()
    request.session['session_otps'] +=otp
    message_to_broadcast = ("Have you played the incredible TwilioQuest "
                                                "yet? Grab it here: https://www.twilio.com/quest")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    recepient = '+91 9991689861'
    client.messages.create(to=recepient,
                            from_=settings.TWILIO_NUMBER,
                            body=message_to_broadcast)
    print("sent")
    
    return 0




class Login(View) :
    template_name = "accounts/auth.html"

    def get(self,request) :
        return render(request,self.template_name)
    
    def post(self,request) :
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username,password)
        if user is not None  :
            login(user)
            return redirect('/dashboard')
        else :
            return redirect(reverse('accounts:register'))
            

user_login = Login.as_view() 





@method_decorator(csrf_exempt,name='dispatch')
class Register(View) :
    template_name = "accounts/auth.html"
    
    def post(self,request) :
        username = request.POST["username"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        email = request.POST["email"]
        
        if User.objects.filter(email= email).exists() :
            print("same email")
            messages.error(request,"Email already exists !")
        elif User.objects.filter(profile__phone= phone).exists() :
            print("same phone")
            messages.error(request,"Phone already exists !")
        else :
             print("ok user")
            #  user = User.objects.create(username=username,email=email)
            #  user.profile.phone = phone
            #  user.set_password(password)
            #  user.save()
             send_otp(request)
             print("worked")

             return redirect(reverse("accounts:verify_mobile"))
        return render(request,"accounts/auth.html")


register = Register.as_view()





class Verify(View) :
    template_name = "accounts/verify_otp.html"

    def post(self,requset,pk) :
        otp = request.POST["otp"]
        if otp in requset.session["session_otps"] :
            messages.success(request,"Otp verification complete !!")
            user = User.objects.get(pk = pk)
            user.profile.is_verified = True
            user.save()
            return redirect(reverse("accounts:add_contacts"))
        else :
            messages.error(request,"Wrong Otp !!")
            return render(request,self.template_name)

verify_otp = Verify.as_view()




class AddContacts(View) :
         def post(self,requset) :
             pass
add_contacts = AddContacts.as_view()


