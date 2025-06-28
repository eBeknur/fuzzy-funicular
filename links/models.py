from django.db import models
from authUser.models import User
from .utils import generate_url

class Link(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='links/%Y/%m/%d')
    url = models.CharField(default=generate_url)
    description = models.TextField(blank=True)
    views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.author)} - {self.url}'
