from django.urls import path
from . import views
from .views import loginview ,usernamevalidation,logoutview ,registerview, emailvalidation





urlpatterns = [
    path('login',loginview.as_view() , name='login'),
    path('logiout', logoutview.as_view() , name='logout'),
    path('register', registerview.as_view() , name='register'),
    path('validate-username', usernamevalidation.as_view() , name='validate-username'),
    path('validate-username', emailvalidation.as_view() , name='validate-email'),




   
]