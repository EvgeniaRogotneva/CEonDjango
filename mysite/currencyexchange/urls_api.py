from django.urls import path
from . import views

urlpatterns = [
    path('add_rate_by_api', views.add_rate_by_api, name='add_rate_by_api'),
    path('get_rate_for_pair_by_api', views.get_rate_for_pair_by_api, name='get_rate_for_pair_by_api'),
    path('create_user', views.create_user, name='create_user'),
    path('login', views.login, name='login'),
    ]