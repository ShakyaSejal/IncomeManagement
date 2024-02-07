from . import views
from django.urls import path

urlpatterns = [
    path('income', views.index, name="incomes"),
    path('add_income', views.add_income, name="add_income"),

]