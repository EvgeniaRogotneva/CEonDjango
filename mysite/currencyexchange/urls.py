from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_rate', views.add_rate, name='add_rate'),
    path('get_rate_for_pair', views.get_rate_for_pair, name='get_rate_for_pair'),
    path('erase_all', views.erase_all, name='erase_all'),
]
