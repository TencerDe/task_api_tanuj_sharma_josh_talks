# Task Manager API

## Table of Contents
- [Project Overview](#project-overview)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
  - [User Management](#user-management)
  - [Task Management](#task-management)
- [Testing Guide](#testing-guide)
  - [Sample API Requests](#sample-api-requests)
  - [Test Credentials](#test-credentials)
- [Troubleshooting](#troubleshooting)

## Project Overview

A Django REST Framework-based Task Manager API that enables:
- User management
- Task creation and tracking
- Task assignment to multiple users
- Task status management

### Tech Stack
- Python 3.x
- Django 5.2
- Django REST Framework
- SQLite3 Database

## Setup Instructions

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Installation Steps

1. **Clone the Repository**
```bash
git clone https://github.com/TencerDe/task_api_tanuj_sharma_josh_talks.git
cd task_manager
```

2. **Create Virtual Environment**

# Windows
python -m venv venv
venv\Scripts\activate

3. **Install Dependencies**

pip install django
pip install djangorestframework

4. **Run Migrations**

python manage.py makemigrations
python manage.py migrate


5. **Start Server**

python manage.py runserver

The API will be available at `http://127.0.0.1:12/`

## API Documentation

### User Management

#### 1. Create User
http
POST /api/users/
Content-Type: application/json

{
    "name": "Tanuj Sharma",
    "email": "tanuj@example.com",
    "mobile": "1234567890"
}


Response:
json
{
    "id": 1,
    "name": "Tanuj Sharma",
    "email": "tanuj@example.com",
    "mobile": "1234567890"
}

#### 2. List Users
http
GET /api/users/


#### 3. Get User Details
http
GET /api/users/{id}/


### Task Management

#### 1. Create Task with User Assignment
http
POST /api/tasks/
Content-Type: application/json

{
    "name": "Test Task",
    "description": "This is a test task",
    "task_type": "bug",
    "status": "pending",
    "assigned_to": [1]
}


Response:
json
{
    "id": 1,
    "name": "Test Task",
    "description": "This is a test task",
    "task_type": "bug",
    "status": "pending",
    "created_at": "2024-04-15T12:00:00Z",
    "completed_at": null,
    "assigned_to": [1]
}


#### 2. Assign Users to Task
http
POST /api/tasks/{task_id}/assign/
Content-Type: application/json

{
    "user_ids": [1, 2]
}


#### 3. Get User's Tasks
http
GET /api/users/{user_id}/tasks/


Response:
json
[
    {
        "id": 1,
        "name": "Test Task",
        "description": "This is a test task",
        "task_type": "bug",
        "status": "pending",
        "created_at": "2024-04-15T12:00:00Z",
        "completed_at": null,
        "assigned_to": [1]
    }
]


## Testing Guide

### Sample API Requests

#### Using cURL

1. **Create User**
bash
curl -X POST http://127.0.0.1:12/api/users/ \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Tanuj Sharma",
           "email": "tanuj@example.com",
           "mobile": "1234567890"
         }'


2. **Create Task with Assignment**
bash
curl -X POST http://127.0.0.1:12/api/tasks/ \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Test Task",
           "description": "This is a test task",
           "task_type": "bug",
           "status": "pending",
           "assigned_to": [1]
         }'


#### Using Postman

1. **Create User Request**
- Method: POST
- URL: `http://127.0.0.1:12/api/users/`
- Headers: `Content-Type: application/json`
- Body: User JSON (as shown above)

2. **Create Task Request**
- Method: POST
- URL: `http://127.0.0.1:12/api/tasks/`
- Headers: `Content-Type: application/json`
- Body: Task JSON (as shown above)

### Test Credentials

#### Test User 1
json
{
    "name": "Tanuj Sharma",
    "email": "john@example.com",
    "mobile": "1234567890"
}


#### Test User 2
Change the 'name','email','mobile' for registering new user.


#### Sample Task
json
{
    "name": "Test Task",
    "description": "This is a test task",
    "task_type": "bug",
    "status": "pending",
    "assigned_to": [1]
}


## Data Models

### User Model
python
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)


### Task Model
python
class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    completed_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ManyToManyField(User, related_name='tasks')


## Troubleshooting

### Common Issues and Solutions

1. **Task Assignment Not Working**
- Verify user exists using `GET /api/users/{id}/`
- Ensure correct user ID in assignment request
- Check task creation response for assigned_to field

2. **User Creation Failed**
- Ensure unique email and mobile number
- Check format of mobile number (10 digits)
- Verify all required fields are provided

3. **Cannot Get User's Tasks**
- Confirm user ID exists
- Verify task assignment was successful
- Check task creation included assigned_to field

### Error Responses

1. **User Not Found (404)**
json
{
    "detail": "Not found."
}


2. **Validation Error (400)**
json
{
    "email": ["Enter a valid email address."],
    "mobile": ["Ensure this field has exactly 10 digits."]
}


## API Status Codes

- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Server Error

## Testing Sequence

1. Create a user
2. Verify user creation
3. Create a task with user assignment
4. Verify task creation
5. Check user's tasks
6. Update task status
7. Verify task update

## Support

For issues or questions:
1. Check the troubleshooting guide
2. Verify request format and data
3. Ensure server is running
4. Check database migrations

---

**All rights reserved to Tanuj Sharma aka TencerDe. this project is made for Josh Talks backend engineer profile.**
