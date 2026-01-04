# inventory_manager/middleware.py

from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware to enforce login on all pages except allowed ones.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = [
            '/login/',
            '/register/',
            '/logout/',
            settings.STATIC_URL,
            '/admin/',
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not any(request.path.startswith(path) for path in self.public_paths):
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)
