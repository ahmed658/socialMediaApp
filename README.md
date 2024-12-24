# socialMediaApp
# Social Media App - High-Quality Documentation

This is a Python-based social media application built with **FastAPI**. It provides a RESTful API to handle users, posts, votes, and authentication. This document explains the application structure, main components, and future paths for API routes.

---

## Application Structure

The application is modular and consists of the following key components:

1. **Models**: Defines database tables and their relationships (`models.py`).
2. **Schemas**: Manages data validation and serialization using Pydantic (`schemas.py`).
3. **Authentication**: Handles user authentication and token generation (`oauth2.py`).
4. **Database**: Configures database connection and ORM setup (`database.py`).
5. **Utilities**: Provides utility functions for password hashing and verification (`utils.py`).
6. **Main Application**: Bootstraps the FastAPI application and integrates routers (`main.py`).
7. **Configuration**: Reads environment variables for dynamic configuration (`config.py`).

---

## Components Overview

### **1. Models (`models.py`)**
Defines database tables for `Post`, `User`, and `Vote`.

- **Post**:
  - Represents a social media post.
  - Fields: `id`, `title`, `content`, `published`, `created_at`, `owner_id`.
  - Relationships: Links to the `User` table (`owner` field).

- **User**:
  - Represents application users.
  - Fields: `id`, `email`, `password`, `created_at`.
  - Relationships: None directly in this model, but linked to posts and votes.

- **Vote**:
  - Represents a user's vote on a post.
  - Fields: `user_id`, `post_id`, `vote_dir`.

---

### **2. Schemas (`schemas.py`)**
Defines data validation and serialization schemas using Pydantic.

- **PostBase**: Base schema for posts (`title`, `content`, `published`).
- **UserOut**: Schema for user data returned from API (`email`, `id`, `created_at`).
- **Token**: Schema for authentication tokens (`access_token`, `token_type`).
- **VoteCreate**: Handles vote creation requests (`post_id`, `vote_dir`).

---

### **3. Authentication (`oauth2.py`)**
Handles user authentication and access token generation.

- **Token Generation**:
  - `create_access_token(data: dict)`: Generates a JWT token with an expiration.
  
- **Token Verification**:
  - `verify_access_token(token: str, credentials_exception)`: Decodes and validates JWT tokens.

- **Current User Retrieval**:
  - `get_current_user(token: str, db: Session)`: Fetches the current authenticated user from the database.

---

### **4. Database (`database.py`)**
Configures the connection to a PostgreSQL database using SQLAlchemy.

- **Database URL**:
  - Dynamically constructed using environment variables.
  
- **Session Management**:
  - `SessionLocal`: Manages database sessions.
  - `get_db()`: Dependency function to provide database session.

- **Base**:
  - SQLAlchemy's declarative base for ORM mappings.

---

### **5. Utilities (`utils.py`)**
Provides helper functions for password security.

- **Password Hashing**:
  - `hashPassword(password: str)`: Hashes a plain text password.
  
- **Password Verification**:
  - `verify_password(password: str, hashedpassword: str)`: Verifies a plain text password against a hashed password.

---

### **6. Configuration (`config.py`)**
Reads environment variables using Pydantic's `BaseSettings`.

- **Settings**:
  - Database credentials: `database_hostname`, `database_name`, `database_port`, `database_username`, `database_password`.
  - Security settings: `secret_key`, `algorithm`, `access_token_expire_minutes`.

- **Environment File**:
  - Variables are sourced from an `.env` file.

---

### **7. Main Application (`main.py`)**
Bootstraps the FastAPI application and integrates routers.

- **Routers**:
  - `post.router`: Manages post-related routes 
  - `user.router`: Handles user-related routes 
  - `auth.router`: Provides authentication endpoints 
  - `vote.router`: Manages vote-related routes 

---
## Router Overview

The application has four routers, each dedicated to a specific domain:

1. **Post Router (`post.py`)**: Handles operations on posts.
2. **Vote Router (`vote.py`)**: Manages user votes on posts.
3. **User Router (`user.py`)**: Manages user accounts.
4. **Authentication Router (`auth.py`)**: Provides user authentication and token management.

---

## 1. Post Router

### **Base Path**: `/posts`

### **Endpoints**

#### **POST `/`**
- **Description**: Creates a new post.
- **Request Body**: 
  - `title` (string): Title of the post.
  - `content` (string): Content of the post.
  - `published` (boolean, optional): Whether the post is published (default is `True`).
- **Response**: 
  - Status Code: `201 Created`.
  - Body: The created post's details.
- **Authorization**: Requires authentication.

#### **GET `/`**
- **Description**: Retrieves a list of posts.
- **Query Parameters**:
  - `limit` (integer, optional): Number of posts to return (default: `10`).
  - `skip` (integer, optional): Number of posts to skip (default: `0`).
  - `search` (string, optional): Search query for filtering posts.
- **Response**:
  - Status Code: `200 OK`.
  - Body: List of posts with vote counts.

#### **GET `/{id}`**
- **Description**: Retrieves a specific post by its ID.
- **Path Parameters**:
  - `id` (integer): ID of the post.
- **Response**:
  - Status Code: `200 OK`.
  - Body: Post details.
- **Error**: Returns `404 Not Found` if the post does not exist.

#### **DELETE `/{id}`**
- **Description**: Deletes a specific post by its ID.
- **Path Parameters**:
  - `id` (integer): ID of the post.
- **Response**:
  - Status Code: `204 No Content`.
- **Authorization**: Requires authentication. Only the post owner can delete.
- **Error**: 
  - `404 Not Found`: Post not found.
  - `401 Unauthorized`: Post does not belong to the current user.

#### **PUT `/{id}`**
- **Description**: Updates a specific post by its ID.
- **Path Parameters**:
  - `id` (integer): ID of the post.
- **Request Body**:
  - `title` (string): New title.
  - `content` (string): New content.
  - `published` (boolean): Whether the post is published.
- **Response**:
  - Status Code: `200 OK`.
  - Body: Updated post details.
- **Authorization**: Requires authentication. Only the post owner can update.
- **Error**: 
  - `404 Not Found`: Post not found.
  - `401 Unauthorized`: Post does not belong to the current user.

---

## 2. Vote Router

### **Base Path**: `/votes`

### **Endpoints**

#### **POST `/`**
- **Description**: Casts a vote on a post.
- **Request Body**:
  - `post_id` (integer): ID of the post to vote on.
  - `vote_dir` (integer): Direction of the vote (`1` for upvote, `0` for downvote).
- **Response**:
  - Status Code: `201 Created`.
  - Body: The vote details.
- **Authorization**: Requires authentication.
- **Error**: Returns `404 Not Found` if the post does not exist.

#### **DELETE `/`**
- **Description**: Deletes a user's vote on a post.
- **Request Body**:
  - `post_id` (integer): ID of the post to remove the vote from.
- **Response**:
  - Status Code: `204 No Content`.
- **Authorization**: Requires authentication.
- **Error**: Returns `404 Not Found` if the vote does not exist.

---

## 3. User Router

### **Base Path**: `/users`

### **Endpoints**

#### **POST `/`**
- **Description**: Creates a new user account.
- **Request Body**:
  - `email` (string): Email address of the user.
  - `password` (string): Password for the account.
- **Response**:
  - Status Code: `201 Created`.
  - Body: User details (excluding password).
- **Error**: Returns `409 Conflict` if the email is already registered.

#### **GET `/{id}`**
- **Description**: Retrieves a user by their ID.
- **Path Parameters**:
  - `id` (integer): ID of the user.
- **Response**:
  - Status Code: `200 OK`.
  - Body: User details.
- **Error**: Returns `404 Not Found` if the user does not exist.

---

## 4. Authentication Router

### **Base Path**: `/login`

### **Endpoints**

#### **POST `/login`**
- **Description**: Authenticates a user and returns an access token.
- **Request Body**:
  - `username` (string): User's email address.
  - `password` (string): User's password.
- **Response**:
  - Status Code: `200 OK`.
  - Body:
    - `access_token`: The JWT access token.
    - `token_type`: Token type (e.g., `bearer`).
- **Error**: Returns `403 Forbidden` if the credentials are invalid.

---

## Usage Instructions

### Prerequisites
1. Install Python 3.10 or higher.
2. Set up a PostgreSQL database.
3. Create an `.env` file with the following variables:
   ```env
   database_hostname=localhost
   database_name=socialmedia
   database_port=5432
   database_username=postgres
   database_password=yourpassword
   secret_key=your_secret_key
   algorithm=HS256
   access_token_expire_minutes=30

