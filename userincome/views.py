from django.shortcuts import render
from .models import UserIncome, Source
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    """
    This function is used to render the income page
    """
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context ={
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)



    # description = request.GET.get('description')



def search_income(request):
    """
    this view is about searching the income
    """
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)
    

@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income removed successfully')
    return redirect('incomes')
    from django.shortcuts import render
from .models import UserIncome, Source
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    """
    This function is used to render the income page
    """
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPrefrence.objects.get(user=request.user).currency
    context ={
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)



    # description = request.GET.get('description')

@login_required(login_url='/authentication/login')
def add_income(request):
    """
    this view adds income to the income page 
    """
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)
    
    if request.method=='POST':
        amount = request.POST['amount']
        date = request.POST['income_date']
        source = request.POST['source']
        description = request.POST['description']

        if not amount:
            messages.error(request, 'Amount is required to add income')
            return render(request, 'income/add_income.html', context)
        
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/add_income.html', context)
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        
        UserIncome.objects.create(owner=request.user, 
                                  amount=amount, 
                                  date=date, 
                                  source=source, 
                                  description=description)
        messages.success(request, 'Income added successfully')


        return redirect('incomes')



def search_income(request):
    """
    this view is about searching the income
    """
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)
    

@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income removed successfully')
    return redirect('incomes')

@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    source = Source.objects.all()
    context = {
        'income': income,
        'source': source
    }

    if request.method =='GET':
      return render(request, 'income/edit_income.html', context)
    if request.method =='POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render (request, 'income/edit_income.html', context)
        date = request.POST['income_date']
        source = request.POST['source']
        description = request.POST['description']

        if not date:
            messages.error(request,'date is required')
            return render (request, 'income/edit_income.html', context)
        
        if not source:
            messages.error(request,'source is required')
            return render (request, 'income/edit_income.html', context)
        
        if not description:
            messages.error(request,'description is required')
            return render (request, 'income/edit_income.html', context)
        income.owner =  request.user #request.user is the current logged in user
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        income.save()

        messages.success(request,'income removed succesfully inn the database')

        return redirect('income')

       

    
