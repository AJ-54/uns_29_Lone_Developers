from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
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
from .decorators import user_check
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required









#twilioclient
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)









@login_required
def send_otp(request) :

    if "phone" not in request.POST.keys() :
        phone = request.user.profile.phone
    else :
        phone = request.POST["phone"]
    
    if request.session.get('session_otps',True) :
        request.session['session_otps'] = []
    otp = pyotp.TOTP(pyotp.random_base32()).now()
 
    message = client.messages \
                .create(
                     body="Your otp is "+otp,
                     from_=settings.TWILIO_NUMBER,
                     to=phone
                 )
    print(message)
    return HttpResponse("sent") if "phone" not in request.POST.keys() else 0








def auth_view(request) :
    return render(request,"accounts/auth.html")











class Login(View) :
    
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







class Register(View) :
    
    def post(self,request) :
        request.POST = json.loads(request.body)
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
             user = User.objects.create(username=username,email=email)
             user.profile.phone = phone
             user.set_password(password)
             user.save()
             login(user)
             send_otp(request)
             print("worked")

             return redirect(reverse("accounts:verify_mobile"))
        return render(request,"accounts/auth.html")


register = Register.as_view()










class Verify(LoginRequiredMixin,View) :
    template_name = "accounts/verify_otp.html"

    def get(self,request) :
        if requset.user.is_verified and request.user.profile.is_complete :
            return redirect('profile/')
        elif requset.user.is_verified and not request.user.profile.is_complete :
            return redirect('complete_profile/')
        else :
            render(requset,self.template_name)
    
    
    def post(self,request) :
        request.POST = json.loads(request.body)
        otp = request.POST["otp"]
        user = request.user
        phone = request.user.profile.phone

        if  request.session and 'session_otps' in request.session.keys() and otp in request.session['session_otps'] :
            verification_checks["status"] = "approved"
            user.profile.is_verified = True
            user.profile.save()


        # verification_check = client.verify \
        #                    .services(settings.SERVICE_SID) \
        #                    .verification_checks \
        #                    .create(to=phone, code=otp)

        if verification_check.status !='approved' :
            messages.error(request,"Wrong Otp !!")
            return render(request,self.template_name)
        messages.success(request,"Verification Succesful !!")
        return redirect(redirect('add_contacts'))

verify_otp = Verify.as_view()












class CompleteProfile(LoginRequiredMixin,View) :
         template_name = "accounts/complete_profile.html"
         def get(self,requset) :
             return render(requset,self.template_name)


complete_profile= CompleteProfile.as_view()








class AddContact(LoginRequiredMixin,View) :
    def post(self,request) :
      pass

add_contact = AddContact.as_view()









class AddVehicle(LoginRequiredMixin,View) :
    def post(self,request) :
        pass 

add_vehicle = AddVehicle.as_view()















class LogoutView(LoginRequiredMixin,View) :
    def post(self,requset) :
        logout(requset.user)
        return redirect('')


user_logout = LogoutView.as_view()