from django.db import models

# Create your models here.

from main.models import CustomUser

class Chat(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files', blank=True)
    file_name = models.CharField(max_length=100, blank=True)
    file_type = models.CharField(max_length=100, blank=True)
    file_size = models.PositiveIntegerField(blank=True)
    thumbnail = models.ImageField(upload_to='chat_thumbnails', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
