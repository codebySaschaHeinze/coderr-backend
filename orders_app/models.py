from django.conf import settings
from django.db import models


class Order(models.Model):
    """Represents an order between a customer and a business user."""

    STATUS_CHOICES = (
        ('in_progress', 'in_progress'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled'),
    )

    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders_as_customer',
    )

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders_by_business',
    )

    title = models.CharField(max_length=250)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable string representation of the order."""
        return f'Order({self.id})'