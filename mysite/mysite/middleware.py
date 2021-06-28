from django.http import HttpResponse
from currencyexchange.models import Key


class FirstMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/api/'):
            return self._get_response(request)
        key = Key.objects.filter(key=request.headers['Api-User-Key'])
        if not key.first():
            return HttpResponse(b'{"Error": "You are not authentificated"}', status=401)
        request.user = key.first().user
        return self._get_response(request)
