from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('currencyexchange.urls_api')),
    path('', include('currencyexchange.urls')),
    path('currencyexchange/', include('currencyexchange.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
