from django.http import JsonResponse
from .models import User


class SessionTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Print for debugging
        print("Request Headers:", request.headers)
        
        # Exclude authentication endpoints from middleware
        excluded_paths = ['/api/auth/login/', '/api/auth/signup/']
        if request.path in excluded_paths:
            return self.get_response(request)

        # Check for session token in headers
        session_token = request.headers.get('Authorization')

        if not session_token:
            return JsonResponse(
                {"error": "No session token provided"}, 
                status=401
            )

        # Verify session token
        try:
            user = User.objects.get(
                session_token=session_token,
                is_active=True
            )
            request.user = user
            print("User found:", user.email)  # Debug print
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "Invalid or expired session token"}, 
                status=401
            )

        return self.get_response(request) 