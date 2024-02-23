from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="expenses"),
    path('add_expenses', views.add_expenses, name="add_expenses"),
    path('edit_expense/<int:id>', views.expense_edit, name="expense_edit"),
    #path('search_expenses', views.search_expenses, name="search_expenses"),
    path('search_expenses', csrf_exempt(views.search_expenses), name="search_expenses"),
    path('expense_summary', csrf_exempt(views.expense_summary), name="expense_summary"),
    path('delete_expense/<int:id>', views.delete_expense, name="delete_expense"),
    path('statistics', views.stats_view, name="statistics"),

]