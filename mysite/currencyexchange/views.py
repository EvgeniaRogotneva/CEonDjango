from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime, timezone
from .models import TimeAndCourse
from .forms import AddRate, GetRate
import pytz
import json


def get_ten_rates():
    return TimeAndCourse.objects.order_by('-id')[:10]


def index(request):
    return render(request, 'currencyexchange/index.html', {'title': 'Currency Exchange', 'rates': get_ten_rates()})


def add_rate_by_api(request):
    if request.content_type == 'application/json':
        content = json.loads(request.body.decode())

        form = AddRate(content)

        if form.is_valid():
            form.save()
        else:
            errors = form.errors

    return HttpResponse('Rate has been added', status=200)


def add_rate(request):
    errors = None
    if request.method == "POST":
        form = AddRate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        errors = form.errors
    form = AddRate()
    context = {'form': form, 'errors': errors, 'rates': get_ten_rates()}
    return render(request, 'currencyexchange/add_rate.html', context)


def get_rate_from_bd_with_date(currency_code, time):
    rate = TimeAndCourse.objects.filter(currency_code=currency_code).filter(time__lte=time).order_by('-time')
    if rate.count():
        return rate[0]
    else:
        return None


def get_rate_for_pair(request: HttpRequest):
    if request.method == "POST":
        print('request.content_type', request.content_type)
        if request.content_type == 'application/json':
            print('we are here')
            return HttpResponse('we received your json')
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