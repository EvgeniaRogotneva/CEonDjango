from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta
import json, psycopg2
from django.contrib.auth.models import User
from currencyexchange.models import TimeAndCourse, Key, Permission, Resource, Access, FeatureFlagRawSql
from currencyexchange.forms import AddRate, GetRate, GetRateByApi
from django.contrib.auth.decorators import login_required


def permission_verify(resource, access):
    def internal(function):
        def wrapper(request):
            key = Key.objects.filter(key=request.headers['Api-User-Key'])
            permission = Permission.objects.filter(resource=resource, access=access, user=key[0].user)
            if permission:
                if access == permission[0].access and resource == permission[0].resource:
                    return function(request)
            response = json.dumps({'response': 'You do not have permission for this action'})
            return HttpResponse(response, status=403)
        return wrapper
    return internal


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
@permission_verify(resource=Resource.rate, access=Access.write)
def add_rate_by_api(request):
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


@login_required
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
@permission_verify(resource=Resource.rate, access=Access.read)
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


@login_required()
def _erase_all(request):
    TimeAndCourse.objects.all().delete()
    return render(request, 'currencyexchange/index.html', {'title': 'Currency Exchange', })


@permission_verify(resource=Resource.rate, access=Access.delete)
def erase_all(request):
    return _erase_all(request)


@permission_verify(resource=Resource.user, access=Access.write)
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

def count_average(rate):
    pass


def average_rate(courses):
    cicle = 0
    sum = 0
    for course in courses:
        sum += course.rate
        cicle += 1
    result = sum / cicle
    return result


def query(conn, s):
    cur = conn.cursor()
    cur.execute(s)
    while True:
        result = cur.fetchone()
        if result is None:
            return
        yield result[-1]


def get_average_course_raw_sql(date, currency_code):
    with psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root') as conn:
        conn.autocommit = True
        s = "SELECT * FROM currencyexchange_timeandcourse WHERE currency_code = '{}' AND time >= '{}' AND time < '{}';"\
            .format(currency_code, date, date + timedelta(days=1))
        circle = 0
        sum = 0
        for row in query(conn, s):
            sum += row
            circle += 1
        result = sum / circle
        return {'Date': date.strftime('%Y-%m-%d'), 'Currency': currency_code, 'Average Course': result}


def get_average_course(date, currency_code):
    end = date + timedelta(days=1)
    courses = TimeAndCourse.objects.filter(time__range=(date, end), currency_code=currency_code)
    response = {'Date': date.strftime('%Y-%m-%d'), 'Currency': currency_code, 'Average Course': average_rate(courses)}
    return response


def average_course_by_day(request):
    data = json.loads(request.body)
    key = Key.objects.filter(key=request.headers['Api-User-Key'])
    user_is_featured = FeatureFlagRawSql.objects.filter(user_id=key.first().user.id)
    if user_is_featured.first():
        response = get_average_course_raw_sql(datetime.strptime(data['time'], '%Y-%m-%d'), data['currency_code'])
    else:
        response = get_average_course(datetime.strptime(data['time'], '%Y-%m-%d'), data['currency_code'])
    return HttpResponse(json.dumps(response), status=200)


def average_course_some_days(request):
    data = json.loads(request.body)
    end = datetime.strptime(data['end_date'], '%Y-%m-%d')
    start = datetime.strptime(data['start_date'], '%Y-%m-%d')
    response = []
    while end - start != timedelta(days=0):
        response.append(get_average_course(start, data['currency_code']))
        start += timedelta(days=1)
    response.append(get_average_course(end, data['currency_code']))
    return HttpResponse(json.dumps(response), status=200)
