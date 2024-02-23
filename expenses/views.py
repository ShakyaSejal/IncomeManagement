from django.shortcuts import render, redirect
from .models import Category, Expenses
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
from datetime import datetime


# Create your views here.
# def index(request):
#     return render(request, 'expenses/index.html')

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expenses.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expenses.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expenses.objects.filter(
            description__icontains=search_str, owner=request.user) | Expenses.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)
    
    
@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expenses.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)

    return render(request,'expenses/add_expense.html')

@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expenses.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'categories': categories,
        'values': expense
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html', context)
        
        date = request.POST['expense_date']
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/edit_expense.html', context)
        category = request.POST['category']
        if not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/edit_expense.html', context)
        
        description = request.POST['description']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit_expense.html', context)
        
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()
        messages.success(request, 'Expense updated successfully in the database')
        return redirect('expenses')


def expense_summary(request):
    """ about expenses -> which category 
        amount, time of expense 
    """
    current_date = datetime.date.today()
    four_months_ago = current_date-datetime.timedelta(days=30*4)
    expenses = Expenses.objects.filter(owner=request.user, date__gte=four_months_ago, date__lte=current_date)
    finalresult = {}
    """
    expense -> category -> amount
    """
    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return {'category': category, 'amount': amount}
    
    for x in expenses:
        for y in category_list:
            finalresult[y] = get_expense_category_amount(y)
    return JsonResponse({'expense_summary': finalresult}, safe=False)

    

def stats_view(request):
    return render(request, 'expenses/stats.html')

def delete_expense(request, id):
    expense = Expenses.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed successfully')
    return redirect('expenses')
# postman 




