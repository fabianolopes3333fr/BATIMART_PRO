from django.contrib.auth import logout
from django.utils import timezone
from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlencode

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_time = timezone.now()
            last_activity = request.session.get('last_activity')

            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                if (current_time - last_activity).seconds > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    params = urlencode({'session_expired': 'true'})
                    return redirect(f'{settings.LOGIN_URL}?{params}')

            request.session['last_activity'] = current_time.isoformat()

        response = self.get_response(request)
        return response