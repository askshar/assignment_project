from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_uploads/')
    filename = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if not self.filename:
            self.filename='default.pdf'
            return self.filename
        return self.filename


class FileText(models.Model):
    file = models.OneToOneField(UserFile, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename