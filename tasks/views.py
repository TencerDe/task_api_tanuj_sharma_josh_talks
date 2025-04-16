from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Task, User
from .serializers import TaskSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth.hashers import check_password
import uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt


# TaskViewSet handles CRUD operations for tasks
class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling task operations.
    Provides default CRUD operations and custom actions.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Custom action to assign users to a task.
        Accepts a list of user IDs in the request body.
        """
        task = self.get_object()
        user_ids = request.data.get('user_ids', [])
        if not user_ids:
            return Response({"error": "user_ids is required."}, status=400)

        users = User.objects.filter(id__in=user_ids)
        task.assigned_to.set(users)
        task.save()
        return Response(TaskSerializer(task).data, status=200)

# API endpoint to get all tasks for a specific user
@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_tasks(request, user_id):
    """
    Retrieve all tasks assigned to a specific user.
    Returns 404 if user doesn't exist.
    """
    user = get_object_or_404(User, pk=user_id)
    tasks = user.tasks.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

# API endpoint to assign users to a task

# 
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def assign_task(request):
    """
    Assign multiple users to a specific task.
    Accepts a list of user IDs in the request body.
    """
    task_id = request.data.get('task_id')

    user_ids = request.data.get('user_ids', [])
    
    if not isinstance(user_ids, list):
        return Response({"error": "user_ids must be a list"}, status=400)

    users = User.objects.filter(id__in=user_ids)
    if not users:
        return Response({"error": "No valid users found"}, status=400)

    task = Task.objects.get(id=task_id)

    task.assigned_to.set(users)
    task.save()

    return Response({"message": "Users assigned successfully"})

# UserViewSet handles CRUD operations for users
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling user operations.
    Provides default CRUD operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# Signup View
@permission_classes([AllowAny])
@api_view(['POST'])
def signup(request):
    try:
        data = request.data
        # Basic validation
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"error": f"{field} is required"}, 
                    status=400
                )

        # Check if user already exists
        if User.objects.filter(email=data['email']).exists():
            return Response(
                {"error": "Email already registered"}, 
                status=400
            )

        

        # Create user
        user = User.objects.create(
            name=data['name'],
            email=data['email'],
            password=data['password']  # Will be hashed in model save method
        )

        # Generate session token
        session_token = uuid.uuid4()
        user.session_token = session_token
        user.save()

        return Response({
            "message": "User created successfully"
        }, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

# Login View
@permission_classes([AllowAny])
@api_view(['POST'])
def login(request):
    try:
        data = request.data
        if not data.get('email') or not data.get('password'):
            return Response(
                {"error": "Email and password are required"}, 
                status=400
            )

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=404
            )

        # Verify password
        if not check_password(data['password'], user.password):
            return Response(
                {"error": "Invalid password"}, 
                status=401
            )

        # Generate new session token
        session_token = uuid.uuid4()
        user.session_token = session_token
        user.is_active = True
        user.save()

        return Response({
            "message": "Login successful",
            "session_token": str(session_token)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)

# Logout View
@permission_classes([AllowAny])
@api_view(['POST'])
def logout(request):
    try:
        session_token = request.headers.get('Authorization')
        if not session_token:
            return Response(
                {"error": "No session token provided"}, 
                status=401
            )

        try:
            user = User.objects.get(session_token=session_token)
            user.session_token = None
            user.is_active = False
            user.save()
            return Response({"message": "Logged out successfully"})
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid session token"}, 
                status=401
            )

    except Exception as e:
        return Response({"error": str(e)}, status=500)
