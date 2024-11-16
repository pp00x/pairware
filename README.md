# Pairware Project Documentation

Welcome to **Pairware**, a user-friendly platform designed to help individuals share items, half of sock's pair or a glove's or an airpod's. This documentation provides a comprehensive guide to the project's structure, features, and implementation details, to understand, modify, or extend the application effortlessly.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Installation and Setup](#installation-and-setup)
4. [Application Features](#application-features)
   - [User Authentication](#user-authentication)
   - [Item Posting](#item-posting)
   - [Messaging System](#messaging-system)
   - [Leaderboard](#leaderboard)
   - [Search and Pagination](#search-and-pagination)
   - [User Profiles](#user-profiles)
   - [Notifications](#notifications)
5. [Models Overview](#models-overview)
6. [Views and URL Patterns](#views-and-url-patterns)
7. [Templates and Static Files](#templates-and-static-files)
8. [Additional Configurations](#additional-configurations)
9. [Conclusion](#conclusion)

---

## Introduction

**Pairware** is a Django-based web application aimed at creating a community platform where users can post items they wish to give away and connect with others interested in those items. The application emphasizes ease of use, security, and scalability, providing features like user authentication, item posting, messaging, search functionality, pagination, user profiles, and notifications.

---

## Project Structure

The project follows Django's standard structure with additional directories for templates and static files. Here's an overview:

```
pairware/
├── pairware/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   │   ├── core/
│   │   │   ├── base.html
│   │   │   ├── item_form.html
│   │   │   ├── item_list.html
│   │   │   ├── send_message.html
│   │   │   ├── inbox.html
│   │   │   ├── leaderboard.html
│   │   │   ├── confirm_transaction.html
│   │   │   ├── user_profile.html
│   │   │   ├── notifications.html
│   ├── static/
│       └── (Static files like CSS and JS)
├── templates/
│   ├── registration/
│   │   ├── login.html
│   │   ├── logout.html
│   │   ├── signup.html
│   │   ├── password_reset_form.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_confirm.html
│   │   ├── password_reset_complete.html
│   │   ├── username_recovery.html
│   │   ├── username_recovery_done.html
├── media/
│   └── items/
└── manage.py
```

---

## Installation and Setup

### Prerequisites

- Python 3.x
- Django 3.x or later
- SQLite (default, can be replaced with PostgreSQL or others)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/pp00x/pairware.git
   cd pairware
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (Optional)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

7. **Access the Application**

   Visit `http://localhost:8000` in your web browser.

---

## Application Features

### User Authentication

- **Sign Up**: Users can create an account with a unique username and email.
- **Login/Logout**: Secure authentication mechanisms provided by Django.
- **Password Reset and Username Recovery**: Users can recover their accounts using email verification.

### Item Posting

- **Post Items**: Authenticated users can post items they wish to give away.
- **Categories**: Users can define custom categories for their items.
- **Images and Descriptions**: Upload images and provide detailed descriptions.

### Messaging System

- **Send Messages**: Users can contact item owners through a built-in messaging system.
- **Inbox**: View received messages, which are marked as read upon viewing.

### Leaderboard

- **User Rankings**: Tracks and displays users based on items given and requests fulfilled.
- **Competitive Element**: Encourages community engagement and generosity.

### Search and Pagination

- **Search Functionality**: Users can search for items based on category, description, or location.
- **Pagination**: Items are paginated to improve usability and performance.

### User Profiles

- **Profile Pages**: Each user has a profile displaying their information and posted items.
- **Public Visibility**: Profiles are accessible to other users for better community interaction.

### Notifications

- **Unread Messages Indicator**: Users are notified of unread messages.
- **Transaction Confirmations**: Notifications are sent when an item transaction is confirmed.

---

## Models Overview

### CustomUser

Extends Django's `AbstractUser` to allow future customizations.

```python
class CustomUser(AbstractUser):
    pass
```

### Item

Represents an item posted by a user.

```python
class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='items/')
    location = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
```

### Message

Handles messaging between users.

```python
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
```

### UserRanking

Tracks user rankings based on activity.

```python
class UserRanking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items_given = models.PositiveIntegerField(default=0)
    requests_fulfilled = models.PositiveIntegerField(default=0)
```

### Notification

Manages notifications sent to users.

```python
class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
```

---

## Views and URL Patterns

### Core Views

- **SignUpView**: Handles user registration.
- **item_create**: Allows users to post new items.
- **item_list**: Displays available items with search and pagination.
- **send_message**: Enables messaging to item owners.
- **inbox**: Shows received messages and marks them as read.
- **confirm_transaction**: Lets owners confirm item transactions.
- **leaderboard**: Displays the user rankings.
- **username_recovery**: Facilitates username recovery via email.
- **user_profile**: Shows a user's profile and posted items.
- **notifications_view**: Displays user notifications and marks them as read.

### URL Patterns

Defined in `core/urls.py`:

```python
urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('items/new/', views.item_create, name='item_create'),
    path('items/confirm/<int:item_id>/', views.confirm_transaction, name='confirm_transaction'),
    path('messages/send/<int:item_id>/', views.send_message, name='send_message'),
    path('messages/inbox/', views.inbox, name='inbox'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('username-recovery/', views.username_recovery, name='username_recovery'),
    path('username-recovery/done/', TemplateView.as_view(template_name='registration/username_recovery_done.html'), name='username_recovery_done'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('notifications/', views.notifications_view, name='notifications'),
]
```

---

## Templates and Static Files

### Base Template

Located at `core/templates/core/base.html`, it includes the navigation bar, messages display, and references to static files.

### Template Inheritance

All other templates extend the base template using Django's template inheritance to maintain a consistent look and feel.

### Static Files

Stored in `core/static/`, including CSS, JavaScript, and images. Use `{% static %}` template tag to reference these files.

### Template Highlights

- **item_list.html**: Displays items with search form and pagination controls.
- **item_form.html**: Form for posting new items, including category suggestions.
- **inbox.html**: Lists received messages.
- **user_profile.html**: Shows user information and their posted items.
- **notifications.html**: Displays user notifications.

---

## Additional Configurations

### Settings

- **Templates Directory**: Configured in `pairware/settings.py` to include the project's templates.
- **Static and Media Files**: Set up with `STATIC_URL`, `STATIC_ROOT`, `MEDIA_URL`, and `MEDIA_ROOT`.
- **Email Backend**: Uses console backend for development.

### Database Initialization

Run the following commands to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Superuser Creation

Optional but recommended for admin access:

```bash
python manage.py createsuperuser
```

### Running the Server

Start the development server with:

```bash
python manage.py runserver
```

---


## Conclusion

Pairware is a robust and elegant application designed to facilitate item sharing within a community. With features like user authentication, item posting, messaging, search, pagination, user profiles, and notifications, it provides a comprehensive platform for user interaction. The project's modular structure and adherence to Django best practices make it highly maintainable and extensible for future enhancements.