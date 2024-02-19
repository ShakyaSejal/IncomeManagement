from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.views import View
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.contrib.auth.models import User




# Create your views here.
# class regisview(View):
class emailvalidation(View):
    def post(self,request):
       data = json.loads(request.body)
       email =  data['email']
    #    if not validated_email(email):
    #         return JsonResponse({'email _error':'Email is invalid'}, status= 400)
      #  if User.objects.filter(email=email).exists():
      #     return JsonResponse({'email_error':'sorry email is use, choose another email'},status =409)
       return JsonResponse({'email_valid':True})
    
class usernamevalidation(View):
        def post(self,request):
                data = json.loads(request.body)
                username =  data['username']
                if not str(username):
                    return JsonResponse({'username _error':'username should only contain alphanumeric character'}, status= 400)
               #  if User.objects.filter(username=username).exists():
               #       return JsonResponse({'username_error':'sorry username is use, choose another username'},status =409)
                return JsonResponse({'username_valid':True})
# class verificationView(View):
#     def get(self, request):
#         try:
#             id= force_text(urlsafe_base64_decode(request.GET['token']))


class loginview(View):
    def get(self,request):
     return render (request ,'authentication/login.html')
    def post(self,request):
     username = request.POST('username')
     password = request.POST('password')
   #   if username and password:
   #      user = auth.authentication (username=username , password= password)
   #      if user:
   #         if user.is_active:
   #             auth.login(request, user)
   #             messages.success(request,"welcome," +user.username +"you are now logged in")
   #             return redirect('expenses')
   #         messages.error(request,"account is not active, pleasecheck again")
   #         return render (request ,'authentication/login.html')

   #      messages.error(request,"invalid credentials , please try again later")
   #      return render (request ,'authentication/login.html')
     messages.error(request,"please fill al the field in  the form!!")
     return render (request ,'authentication/login.html')

class logoutview(View):
   def post(self, request):
      auth.logout(request)
      messages.success(request,"you have been logged out")
      return redirect('login')
   

class registerview(View):
    """
    user data -> username , password and email
    validate user 
    create user account
    
    """
    def get(self,request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        context = {
            'values': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short")
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body={
                    "user":user,
                     "domain":current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                      }
                # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))  # converted uid
               # domain name
                link = reverse('activate', kwargs={'uidb64': email_body['uid'],
                                                   'token':email_body['token']}) # uid + token

                activate_url = 'http://'+current_site.domain+link
                email_content = "Activate your account using the link below\n"
                link_to_user = 'Hi '+user.username + ' Please use this link to verify your account\n'+activate_url
                email = EmailMessage(
                    email_content,
                    link_to_user,
                   )
                email.send(fail_silently=False)
                messages.success(request, "Account successfully created")
                return render(request, 'authentication/registration.html')  

        return render(request, 'authentication/registration.html') 
    def post(self, request):
      auth.logout(request)
      messages.success(request, "You have been logged out")
      return redirect('login')


"""
user -> req -> daraz (login , make changes and inactive) -> cookie(id) as a token 
res -> token -> backend 
user -> req+ token -> backend -> token(id) -> data retrive 
url_safe_base64_encode -> + - _ -> / 
"""

    

