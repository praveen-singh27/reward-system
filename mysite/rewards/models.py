from django.db import models
from authentication.models import UserAccount 

class App(models.Model):
    appname = models.CharField(max_length=255)
    link = models.URLField()
    logo = models.ImageField(upload_to='app_logos/')
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)
    points = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return f"{self.appname} - {self.points} Points"


def user_directory_path(instance, filename):
    # Save files in "screenshots/user_<user_id>/filename"
    return f'screenshots/user_{instance.user.id}/{filename}'


class Screenshot(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    screenshot = models.ImageField(upload_to=user_directory_path)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.app.appname} Screenshot"
    