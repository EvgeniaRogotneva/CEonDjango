from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime, timezone
from .models import TimeAndCourse, Key
from .forms import AddRate, GetRate, GetRateByApi
import pytz
import json
from django.contrib.auth.models import User


def request_validation(func):
    def wrapper(request):
        if request.method != "POST" or request.content_type != 'application/json':
            response = json.dumps({'response': 'I receive only POST request with json content type'})
            return HttpResponse(response, status=400)
        return func(request)
    return wrapper


def get_ten_rates():
    return TimeAndCourse.objects.order_by('-id')[:10]


def index(request):
    return render(request, 'currencyexchange/index.html', {'title': 'Currency Exchange', 'rates': get_ten_rates()})


@request_validation
def add_rate_by_api(request):
    print('request.session', request.session.get_expiry_date())
    if request.content_type == 'application/json':
        content = json.loads(request.body.decode())
        form = AddRate(content)
        if form.is_valid():
            form.save()
            response = json.dumps({'response': 'Rate has been added'})
            return HttpResponse(content=response, content_type='application/json', status=200)
        response = form.errors.as_json()
        return HttpResponse(response, status=400)
    response = json.dumps({'response': 'I receive only POST request with json content type'})
    return HttpResponse(response, status=400)


def add_rate(request):
    errors = None
    form = AddRate(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            form = AddRate()
            context = {'form': form, 'response': 'Info has been added', 'rates': get_ten_rates()}
            return render(request, 'currencyexchange/add_rate.html', context)
        errors = form.errors.as_data()
    context = {'form': form, 'errors': errors, 'rates': get_ten_rates()}
    return render(request, 'currencyexchange/add_rate.html', context)


@request_validation
def get_rate_for_pair_by_api(request: HttpRequest):
    content = json.loads(request.body.decode())
    content['time'] = datetime.fromisoformat(content['time'])
    form = GetRateByApi(content)
    if form.is_valid():
        from_rate = TimeAndCourse.objects.get_rate_from_bd_with_date(
            form.cleaned_data['from_currency_code'], form.cleaned_data['time'])
        to_rate = TimeAndCourse.objects.get_rate_from_bd_with_date(
            form.cleaned_data['to_currency_code'], form.cleaned_data['time'])
        if from_rate and to_rate:
            rate = from_rate.rate / to_rate.rate
            response = json.dumps(
                {'response': '1 ' + from_rate.currency_code + ' equals ' + str(rate) + ' ' + to_rate.currency_code})
        else:
            response = json.dumps({'response': 'I do not have enough information about currencies rate'})

        return HttpResponse(response, status=200)
    return HttpResponse(form.errors, status=400)


def get_rate_for_pair(request: HttpRequest):
    if request.method == "POST":
        form = GetRate(request.POST)
        errors = None
        answer = None
        if form.is_valid():
            from_rate = TimeAndCourse.objects.get_rate_from_bd_with_date(
                form.cleaned_data['from_currency_code'], form.cleaned_data['time'])
            to_rate = TimeAndCourse.objects.get_rate_from_bd_with_date(
                form.cleaned_data['to_currency_code'], form.cleaned_data['time'])
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


def create_user(request):
    data = json.loads(request.body)
    user = User.objects.create_user(data['username'], data['email'], data['password'])
    user.save()
    key = Key(key=data['key'], user=user)
    key.save()
    response = {'Response': 'User ' + user.get_username() + ' has been added'}
    return HttpResponse(json.dumps(response), status=200)

def login(request):
    pass
