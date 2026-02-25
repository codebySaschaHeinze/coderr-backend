from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role-based user type."""

    USER_TYPE_CHOICES = (
        ('customer', 'customer'),
        ('business', 'business'),
    )

    email = models.EmailField(unique=True)
    type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)