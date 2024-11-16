from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    # You can add additional fields here if needed
    pass

User = get_user_model()

class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)  # User-defined categories
    description = models.TextField()
    image = models.ImageField(upload_to='items/')
    location = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.description[:20]}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username} - {self.content[:20]}"

class UserRanking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items_given = models.PositiveIntegerField(default=0)
    requests_fulfilled = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Rank"


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.user.username}"