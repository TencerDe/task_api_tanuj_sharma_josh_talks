from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, get_user_tasks, UserViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')

# The API URLs are determined automatically by the router
# Additionally, we include the URL for user-specific tasks
urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
    path('users/<int:user_id>/tasks/', get_user_tasks, name='user-tasks'),  # Custom endpoint for user tasks
]
