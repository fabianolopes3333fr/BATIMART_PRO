import logging
from django.conf import settings
from .models import Client

logger = logging.getLogger(__name__)

class CustomDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/accounts/'):
            return self.get_response(request)

        host = request.get_host().split(':')[0]
        logger.debug(f"Processing request for host: {host}")

        try:
            client = Client.objects.get(custom_domain=host)
            request.client = client
            logger.info(f"Found client for custom domain: {host}")
        except Client.DoesNotExist:
            logger.info(f"No client found for custom domain: {host}")
            request.client = None

        if request.client is None:
            if host in settings.ALLOWED_HOSTS:
                default_client = Client.objects.filter(is_active=True).first()
                if default_client:
                    request.client = default_client
                    logger.info(f"Using default active client for allowed host: {host}")
                else:
                    logger.warning(f"No active clients found for allowed host: {host}")
            else:
                logger.warning(f"Host not allowed: {host}")

        response = self.get_response(request)
        return response