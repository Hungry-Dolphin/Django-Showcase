from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    clearance = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    send_in = models.ForeignKey(ChatRoom, related_name='chatroom', on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clearance = models.PositiveIntegerField(default=1)

    def choices(self):
        choice = [(x, f'{x}')for x in range(1, self.clearance+1)]
        return choice
