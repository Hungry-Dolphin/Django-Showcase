from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='pdf')
    clearance = models.IntegerField(default=1)

    def __str__(self):
        return self.title
