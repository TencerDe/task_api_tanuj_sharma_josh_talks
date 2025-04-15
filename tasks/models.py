from django.db import models

# Create your models here.
class User(models.Model):
    """
    User model to store basic user information.
    Each user can be assigned to multiple tasks.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    """
    Task model to store task information.
    Tasks can be assigned to multiple users through M2M relationship.
    """
    # Task type choices for categorizing tasks
    TASK_TYPE_CHOICES = [
        ('bug','Bug'),
        ('feature','Feature'),
        ('improvement', 'Improvement'),
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
    # Many-to-Many relationship with User model
    assigned_to = models.ManyToManyField(User, related_name='tasks', blank=True)

    def __str__(self):
        return self.name
