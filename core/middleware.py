from django.conf import settings
from .models import Client

class CustomDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        try:
            client = Client.objects.get(custom_domain=host)
            request.client = client
        except Client.DoesNotExist:
            request.client = None

        response = self.get_response(request)
        return response