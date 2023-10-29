from django.db import models
from django.contrib.auth.models import User


class QueryLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.TextField(default='Previous file')
    query = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Query by {self.user.username} at {self.timestamp}'
