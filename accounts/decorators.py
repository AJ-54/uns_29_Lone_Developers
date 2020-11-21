from .models import * 
from django.shortcuts import redirect


def user_check(func,*args,**kwargs) :
    def wrapper(request,*args,**kwargs) :
        user = request.user 
        if user is not None :
            if user.profile.is_verified and user.profile.is_complete :
                  return func(request,*args,**kwargs)
            elif not user.profile.is_verified:
                return redirect('accounts:send_otp')
            elif not user.profile.is_complete :
                return redirect('accounts:complete_profile')
            else :
                return redirect('')
                
        else :
            return redirect('accounts:login')

    return wrapper