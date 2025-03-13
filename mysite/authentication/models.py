from django.db import models

class UserAccount(models.Model):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
