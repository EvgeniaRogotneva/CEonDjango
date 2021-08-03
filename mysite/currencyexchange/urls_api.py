from django.urls import path
from . import views

urlpatterns = [
    path('add_rate_by_api', views.add_rate_by_api, name='add_rate_by_api'),
    path('get_rate_for_pair_by_api', views.get_rate_for_pair_by_api, name='get_rate_for_pair_by_api'),
    path('create_user', views.create_user, name='create_user'),
    path('login', views.login, name='login'),
    path('erase_all', views.erase_all, name='erase_all'),
    path('average_course', views.average_course_by_day, name='average_course'),
    path('average_course_some_days', views.average_course_some_days, name='average_course_some_days'),
    ]