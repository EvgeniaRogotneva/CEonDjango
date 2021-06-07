from django.http import HttpResponse
from currencyexchange.models import Key


class FirstMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/api/'):
            return self._get_response(request)

        if request.path == '/api/create_user':
            key = Key.objects.filter(key=request.headers['Api-User-Key'])
            if not key.first():
                return HttpResponse(b'{"Error": "You do not have permission to add users"}', status=400)
            if not key.first().user.is_superuser:
                return HttpResponse(b'{"Error": "You do not have permission to add users"}', status=400)

        key = Key.objects.get(key=request.headers['Api-User-Key'])
        if not key:
            return HttpResponse(b'{"Error": "You do not have permission to send request"}', status=400)
        return self._get_response(request)
