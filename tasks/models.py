from django.db import models
from django.contrib.auth.hashers import make_password
import uuid

# Create your models here.

class User(models.Model):
    """
    User model to store basic user information.
    Each user can be assigned to multiple tasks.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128)  # For storing hashed password
    session_token = models.UUIDField(null=True, blank=True)  # For storing session token
    is_active = models.BooleanField(default=True)  # For tracking login status

    def save(self, *args, **kwargs):
        if self._state.adding and self.password:  # Only hash on creation
            self.password = make_password(self.password)
        super().save(*args, **kwargs);

    def __str__(self):
        return self.name
    
class Task(models.Model):
    """
    Task model to store task information.
    Tasks can be assigned to multiple users through M2M relationship.
    """
    # Task type choices for categorizing tasks
    TASK_TYPE_CHOICES = [
           ('running','Running'),
        ('gym','Gym'),
        ('padhai', 'Padhai'),
    ]

    # Task status choices for tracking progress
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completed_at = models.DateTimeField(null=True, blank=True)

    # User model many to may relationship with Task as per the task document
    assigned_to = models.ManyToManyField(User, related_name='tasks', blank=True)

    def __str__(self):
        return self.name
