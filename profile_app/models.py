from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extended profile information linked to a user."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    file = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable string representation of the profile."""
        return f'Profile({self.user_id})'