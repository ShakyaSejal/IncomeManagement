from django.urls import path
from . import views
from .views import loginview, usernamevalidation, emailvalidation, logoutview, registerview
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    

    path('registration', registerview.as_view(), name='registration'),
    path('login', loginview.as_view() , name='login'),
    # path('register', registerview.as_view(), name='register'),
    path('logout', logoutview.as_view(), name='logout'),
    path('validate-username', csrf_exempt(usernamevalidation.as_view()), name='validate-username'),

    path('validate-email', csrf_exempt(emailvalidation.as_view()), name='validate-email'),
    path('activate/<uidb64>/<token>', views.verificationview.as_view(), name='activate'),
]