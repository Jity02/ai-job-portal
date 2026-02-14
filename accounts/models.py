from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):

    class UserTypes(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        EMPLOYER = "EMPLOYER", "Employer"
        STUDENT = "STUDENT", "Student"

    user_type = models.CharField(
        max_length=20,
        choices=UserTypes.choices,
        default=UserTypes.STUDENT
    )

    # Optional profile enhancements
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # Automatically set admin type if superuser
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.user_type = self.UserTypes.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.user_type})"

class Profile(models.Model):
    USER_TYPE = (
        ('student', 'Student'),
        ('employer', 'Employer'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.username