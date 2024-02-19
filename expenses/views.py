from django.shortcuts import render, redirect
from .models import Category, Expenses
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
# Create your views here.
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expenses.objects.filter(
            amount__istartswith = search_str, owner=request.user.id) | Expenses.objects.filter(
                date__istartswith = search_str, owner = request.user) | Expenses.objects.filter(
                    description__istartswith = search_str, owner = request.user ) | Expenses.objects.filter(
                        category__istartswith = search_str, owner = request.user ) 
        date = expenses.value()
        return JsonResponse(list(date), safe=False)
@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expenses.objects.filter(owner = request.user)
    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user = request.user).currency
    context = {
        'expenses' :expenses,
        'page_obj': page_obj,
        'currency' : currency
    }
    return render(request, 'expenses/index.html')

def expense_summary(request):
    return render(request, 'expense/expense_summary.html')

def stats_view(request):
    return render(request, 'expense/stats_view.html')

    

def delete_expense(request, id):
    expense = Expenses.objects.get(pk = id)
    expense.delete()
    messages.success(request, 'Expense removed successfully')
    return redirect('expenses')

@login_required(login_url='/authentication/login')

def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values' : request.POST
    }

    if request.method == 'GET':
        return render(request,'expenses/add_expenses.html', context)
    else:
        amount = request.POST['amount']
        date = request.POST['date']
        categories = request.POST['categories']
        description = request.POST['description']

        if not amount :
            messages.error(request, 'Amount is required to add income')
            return render(request, 'expenses/add_expenses.html', context)
    
        if not date :
            messages.error(request, 'Date is required to add income')
            return render(request, 'expenses/add_expenses.html', context)

        if not categories:
            messages.error(request, 'Categories is required to add income')
            return render(request, 'expenses/add_expenses.html', context)
    
        if not description :
            messages.error(request, 'Description is required to add income')
            return render(request, 'income/add_expenses.html', context)
    
        Expenses.objects.create(owner = request.user,
                                  amount = amount,
                                  date = date,
                                  categories = categories,
                                  description = description)
        
        messages.success(request,'expenses added successfully')

        return redirect('expenses')
@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expenses.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'categories': categories,
        'values' :expense

    }

    if request.method =='GET':
      return render(request, 'expense/edit_expense.html', context)
    if request.method =='POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render (request, 'expense/edit_expense.html', context)
        date = request.POST['expense_date']
        categories = request.POST['categories']
        description = request.POST['description']

        if not date:
            messages.error(request,'date is required')
            return render (request, 'expense/edit_expense.html', context)
        
        if not categories:
            messages.error(request,'source is required')
            return render (request, 'income/edit_expense.html', context)
        
        if not description:
            messages.error(request,'description is required')
            return render (request, 'expense/edit_expense.html', context)
        expense.owner =  request.user #request.user is the current logged in user
        expense.amount = amount
        expense.date = date
        expense.categories = categories
        expense.description = description
        expense.save()

        messages.success(request,'expense removed succesfully inn the database')

        return redirect('expense')

       

    
