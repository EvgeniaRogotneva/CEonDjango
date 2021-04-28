
class FirstMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        print('FirstMiddleware before')
        response = self._get_response(request)
        print('FirstMiddleware after')
        return response
