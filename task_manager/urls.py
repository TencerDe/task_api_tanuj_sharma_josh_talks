from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

# Main URL configuration for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin interface
    path('api/', include('tasks.urls')),  # Include tasks app URLs under /api/
    path('api/token-auth/', obtain_auth_token),  # Token authentication endpoint
]
