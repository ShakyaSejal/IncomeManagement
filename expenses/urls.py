from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="expenses"),
    path('add_expenses', views.add_expenses, name="add_expenses"),
    path('edit_expense/<int:id>', views.expense_edit, name="expense_edit"),
    path('search_expenses', views.search_expenses, name="search_expenses"),
    path('delete_expense/<int:id>', views.delete_expense, name="delete_expense"),


]