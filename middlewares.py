from tiny_web.middleware import Middleware


class MethodOverrideMiddleware(Middleware):
    def process_request(self, request):
        if request.method == 'POST':
            _method = request.POST.get('_method')
            if _method:
                request.method = _method
        return request
