from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet, 
    get_user_tasks, 
    UserViewSet,
    signup,
    login,
    logout
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')

# Define URL patterns
urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    
    # Authentication URLs
    path('auth/signup/', signup, name='signup'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    
    # Task URLs
    path('tasks/', TaskViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='task-list'),
    
    path('tasks/<int:pk>/', TaskViewSet.as_view({
        'get': 'retrieve',
    }), name='task-detail'),
    
    # User's tasks URL
    path('users/<int:user_id>/tasks/', get_user_tasks, name='user-tasks'),
    
    # Task assignment URL
    path('tasks/<int:task_id>/assign/', TaskViewSet.as_view({
        'post': 'assign'
    }), name='task-assign'),
]
