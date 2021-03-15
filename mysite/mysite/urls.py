from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('currencyexchange.urls')),
    path('currencyexchange/', include('currencyexchange.urls')),
    path('admin/', admin.site.urls),
]
