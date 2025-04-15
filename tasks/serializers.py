# tasks/serializers.py
from rest_framework import serializers
from .models import User, Task
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Handles conversion between User instances and JSON format.
    """
    class Meta:
        model = User
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    Handles conversion between Task instances and JSON format.
    Includes custom validation for task status.
    """
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Task
        fields = '__all__'

    def validate_status(self, value):
        """
        Validate that the status is one of the allowed choices.
        """
        if value not in ['pending', 'in_progress', 'completed']:
            raise serializers.ValidationError("Invalid task status.")
        return value

    def update(self, instance, validated_data):
        """
        Custom update method to handle completion time when status is set to completed.
        """
        if 'status' in validated_data and validated_data['status'] == 'completed':
            instance.completed_at = timezone.now()
        return super().update(instance, validated_data)
