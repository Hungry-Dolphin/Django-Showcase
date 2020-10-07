from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
import os
from django.core.exceptions import ValidationError


def upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance}{uuid4().hex}.{ext}'
    return os.path.join('pdf', filename)


def check_extension(pdf):
    errors = []
    ext = os.path.splitext(pdf.path)[1]
    if ext != '.pdf':
        errors.append(f'The file should be a pdf, your file is a {ext}.')
    raise ValidationError(errors)


def check_size(pdf):
    errors = []
    if pdf.size >= 5242880:  # 5Mb
        errors.append(f'The file is larger then 5Mb.')
    raise ValidationError(errors)


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to=upload, validators=[check_extension, check_size])
    clearance = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)


class Comments(models.Model):
    bumps = models.PositiveIntegerField(default=0)
    book = models.ForeignKey(Book, related_name='book', on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = "Comments"
