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
# from django.contrib.auth.tokens import account_activation_token
from .utils import account_activation_token
# from .models import User


# Create your views here.
class emailvalidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
             return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry email in use, choose another one'}, status=409)
        
        return JsonResponse({'email_valid': True})


class usernamevalidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
            # if User.objects.filter(username=username).exists():
            #     return JsonResponse({'username_error': 'Sorry username in use, choose another one'}, status=409)
        return JsonResponse({'username_valid': True})
    
class verificationview(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(request.GET['token']))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')
            

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully")
            return redirect('login')
        except Exception as e:
            pass

        return redirect('login')




class registerview(View):
    """
    user data -> username , password and email
    validate user 
    create user account
    
    """
    def get(self,request):
        return render(request, 'authentication/registration.html')
    
    def post(self, request):
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        context = {
            'fieldValues': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short")
                    return render(request, 'authentication/registration.html', context)
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
                    'khanalbju@gmail.com',
                    [email],


                )
                email.send(fail_silently=False)
                messages.success(request, "Account successfully created")
                return render(request, 'authentication/registration.html')  
    
        return render(request, 'authentication/registration.html') 




class loginview(View):

    def get(self,request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST('username')
        password = request.POST('password')

        if username and password:
            user = auth.authentication(username=username , password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Welcome, "+
                                    user.username+" you are now logged in")
                    return redirect('expenses')
                messages.error(request, "Account is not active, please check your email")
                return render(request, 'authentication/login.html')
            messages.error(request, "Invalid credentials, please try again!!")
            return render(request, 'authentication/login.html')
        messages.error(request, "Please fill all fields in the form!!")
        return render(request, 'authentication/login.html')

class logoutview(View):
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