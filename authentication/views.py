from django.shortcuts import render ,redirect
from django.contrib import auth
from django.views import View
from django.contrib import messages
import json
from django.http import JsonResponse
from .models import User



# Create your views here.
# class regisview(View):
class emailvalidation(View):
    def post(self,request):
       data = json.loads(request.body)
       email =  data['email']
    #    if not validated_email(email):
    #         return JsonResponse({'email _error':'Email is invalid'}, status= 400)
       if User.objects.filter(email=email).exists():
          return JsonResponse({'email_error':'sorry email is use, choose another email'},status =409)
       return JsonResponse({'email_valid':True})
    
class usernamevalidation(View):
        def post(self,request):
                data = json.loads(request.body)
                username =  data['username']
                if not str(username):
                    return JsonResponse({'username _error':'username should only contain alphanumeric character'}, status= 400)
                if User.objects.filter(username=username).exists():
                     return JsonResponse({'username_error':'sorry username is use, choose another username'},status =409)
                return JsonResponse({'username_valid':True})


class loginview(View):
    def get(self,request):
     return render (request ,'authentication/login.html')
    def post(self,request):
     username = request.POST('username')
     password = request.POST('password')
     if username and password:
        user = auth.authentication (username=username , password= password)
        if user:
           if user.is_active:
               auth.login(request, user)
               messages.success(request,"welcome," +user.username +"you are now logged in")
               return redirect('expenses')
           messages.error(request,"account is not active, pleasecheck again")
           return render (request ,'authentication/login.html')

        messages.error(request,"invalid credentials , please try again later")
        return render (request ,'authentication/login.html')
     messages.error(request,"please fill al the field in  the form!!")
     return render (request ,'authentication/login.html')

class logoutview(View):
   def post(self, request):
      auth.logout(request)
      messages.success(request,"you have been logged out")
      return redirect('login')
    

