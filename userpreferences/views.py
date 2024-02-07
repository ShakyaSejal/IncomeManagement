from django.shortcuts import render
from django.conf import settings
import os
import json
from .models import UserPreference
# Create your views here.

def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DiR, 'currencies.json')
    with open(file_path, 'r') as json_data:
        data = json.load(json_data)
        for key, value in data.items():
            currency_data.append({'name': key, 'value':value})

    available = UserPreference.objects.filter(user = request.user).exists()
    user_currency = None

    if available:
        user_currency = UserPreference.objects.get(user = request.user)

    if request.method == 'GET':
        context = {
            'currencies' : currency_data,
            'user_currency' : user_currency,
            'available' : available
        }
        return render(request,'userpreferences/index.html', context)
    else:
        currency = request.POST['currency']
        if available:
            user_currency.currency = currency
            user_currency.save()
        else:
            UserPreference.objects.create(user = request.user, currency=currency)

        message = 'Changes saved successfully'
        context = {
            'currencies' : currency_data,
            'user_currency' : user_currency
        }
    return render(request, 'userpreferences/index.html', context)