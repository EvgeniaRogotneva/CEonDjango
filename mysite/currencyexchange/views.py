from django.http import HttpRequest
from django.shortcuts import render, redirect
from datetime import datetime, timezone
from .models import TimeAndCourse
from .forms import AddRate, GetRate
import pytz


def get_ten_rates():
    return TimeAndCourse.objects.order_by('-id')[:10]


def index(request):
    return render(request, 'currencyexchange/index.html', {'title': 'Currency Exchange', 'rates': get_ten_rates()})


def add_rate(request):
    print('we are in add rate view')
    if request.method == "POST":
        print('flag1')
        form = AddRate(request.POST)
        if form.is_valid():
            print('flag2')
            form.save()
            return redirect('index')
    form = AddRate()
    context = {'form': form}
    return render(request, 'currencyexchange/add_rate.html', context)


def get_rate_from_bd_with_date(currency_code, time):
    rate = TimeAndCourse.objects.filter(currency_code=currency_code).filter(time__lte=time).order_by('-time')
    if rate.count():
        return rate[0]
    else:
        return None


def get_rate_for_pair(request: HttpRequest):
    if request.method == "POST":
        form = GetRate(request.POST)
        errors = None
        answer = None
        if form.is_valid():
            from_rate = get_rate_from_bd_with_date(form.cleaned_data['from_currency_code'], form.cleaned_data['time'])
            to_rate = get_rate_from_bd_with_date(form.cleaned_data['to_currency_code'], form.cleaned_data['time'])
            if from_rate and to_rate:
                rate = from_rate.rate / to_rate.rate
                answer = '1 ' + from_rate.currency_code + ' equals ' + str(rate) + ' ' + to_rate.currency_code
            else:
                errors = 'I do not have enough information about currencies rate'
        else:
            errors = 'Form is not correct'
        return render(request, 'currencyexchange/index.html', {'title': 'Currency Exchange', 'errors': errors,
                                                               'rates': get_ten_rates(), 'answer': answer})
    form = GetRate()
    context = {'form': form}
    return render(request, 'currencyexchange/get_rate_for_pair.html', context)


def erase_all(request):
    TimeAndCourse.objects.all().delete()
    return render(request, 'currencyexchange/index.html', {'title': 'Currency Exchange', })