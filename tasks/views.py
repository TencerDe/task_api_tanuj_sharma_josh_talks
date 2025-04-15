from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Task, User
from .serializers import TaskSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

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
@api_view(['GET'])
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
@api_view(['POST'])
def assign_task(request, task_id):
    """
    Assign multiple users to a specific task.
    Accepts a list of user IDs in the request body.
    """
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    user_ids = request.data.get('user_ids', [])
    
    if not isinstance(user_ids, list):
        return Response({"error": "user_ids must be a list"}, status=400)

    users = User.objects.filter(id__in=user_ids)
    if not users:
        return Response({"error": "No valid users found"}, status=400)

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
