# chat/middleware.py

import time
from django.core.cache import cache
from django.http import JsonResponse

class ThrottleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 5  # 5 requests
        self.duration = 60  # per minute

    def __call__(self, request):
        ip = self.get_client_ip(request)
        if not self.is_allowed(ip):
            return JsonResponse({'error': 'Too many requests'}, status=429)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_allowed(self, ip):
        requests = cache.get(ip, [])
        now = time.time()
        # filter out old requests
        requests = [req for req in requests if now - req < self.duration]

        if len(requests) >= self.rate_limit:
            return False

        requests.append(now)
        cache.set(ip, requests, timeout=self.duration)
        return True
