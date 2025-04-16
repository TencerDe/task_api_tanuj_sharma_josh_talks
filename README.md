# Task Manager API

// 

# Task Manager API

## Overview

Created reuqested api's for Josh talks assignment round and testing details are included in this documentation as well

## Features

- User registration and authentication (signup, login, logout)
- CRUD operations for tasks and users
- Assigning tasks to multiple users
- Middleware for session token validation

## Endpoints

### Authentication

- **Signup**: `POST /api/auth/signup/`
  - Registers a new user.
  - Required fields: `name`, `email`, `password`
  - Example request body:
    ```json

A user is already registered but if you want to register a new user you can try with any credentials of your choice.

    {
      "name": "",
      "email": "",
      "password": ""
    }
    ```

- **Login**: `POST /api/auth/login/`
  - Authenticates a user and generates a session token.
  - Required fields: `email`, `password`
  - Example request body:
    ```json
    {
      "email": "tanuj@gmail.com",
      "password": "test123"
    }
    ```

- **Logout**: `POST /api/auth/logout/`
  - Logs out a user by invalidating the session token.
  - Requires `Authorization` header with the session token.
  - You will receive a session token when hitting the Login api, paste that session token in value field of header section
  - And for key field Register "Authorization"

### Tasks

- **List Tasks**: `GET /api/tasks/`
  - Retrieves a list of all tasks.

- **Create Task**: `POST /api/tasks/`
  - Creates a new task.
  - Example request body:
    ```json
    I have created 3 tasks like 'running','gym','padhai'. So only enter out of these 3 tasks in this api. Description and name cabn be your choice 
    {
      "name": "New Task",
      "description": "Task description",
      "task_type": "running",
      "status": "pending"
    }
    ```

- **Retrieve Task**: `GET /api/tasks/{task_id}/`
  - Retrieves details of a specific task.

- **Assign Users to Task**: `POST /api/tasks/{task_id}/assign/`
  - Assigns multiple users to a specific task.
  - Example request body:
    ```json
    {
      "user_ids": [1, 2, 3]
    }
    ```

### Users

- **List Users**: `GET /api/users/`
  - Retrieves a list of all users.

- **Retrieve User Tasks**: `GET /api/users/{user_id}/tasks/`
  - Retrieves all tasks assigned to a specific user.

## Models

### User

- `name`: CharField
- `email`: EmailField (unique)
- `mobile`: CharField (unique)
- `password`: CharField (hashed)
- `session_token`: UUIDField (nullable, blank)
- `is_active`: BooleanField (default: True)

### Task

- `name`: CharField
- `description`: TextField
- `created_at`: DateTimeField (auto_now_add)
- `task_type`: CharField (choices: running, gym, padhai)
- `status`: CharField (choices: pending, in_progress, done, default: pending)
- `completed_at`: DateTimeField (nullable, blank)
- `assigned_to`: ManyToManyField (User, related_name='tasks', blank=True)

## Middleware

### SessionTokenMiddleware

- Validates the session token provided in the `Authorization` header for all requests except authentication endpoints (`/api/auth/login/`, `/api/auth/signup/`).


**All rights reserved to Tanuj Sharma aka TencerDe. this project is made for Josh Talks backend engineer profile.**