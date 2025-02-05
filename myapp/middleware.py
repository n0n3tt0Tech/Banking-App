from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.sessions.models import Session
from django.contrib.sessions.middleware import SessionMiddleware


# myapp/middleware.py
class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; img-src 'self' data: https://cdn-icons-png.flaticon.com;"


        return response
    

class AutoRotateSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        super().process_request(request)

        # Check if the session has a 'last_rotated' timestamp
        if 'last_rotated' not in request.session:
            request.session['last_rotated'] = timezone.now().timestamp()
        else:
            # Calculate the time difference
            last_rotated = request.session['last_rotated']
            current_time = timezone.now().timestamp()
            time_diff = current_time - last_rotated

            # If 2 minutes have passed, rotate the session ID
            if time_diff >= 120:  # 120 seconds = 2 minutes
                request.session.cycle_key()
                request.session['last_rotated'] = current_time
