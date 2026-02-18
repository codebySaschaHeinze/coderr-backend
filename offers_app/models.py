from django.conf import settings
from django.db import models


class Offer(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='offers',
    )

    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Offer({self.id}) {self.title}'
    

class OfferDetail(models.Model):

    OFFER_TYPE_CHOICES = (
        ('basic', 'basic'),
        ('standard', 'standard'),
        ('premium', 'premium'),
    )

    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE,
        related_name='details',
    )

    title = models.CharField(max_length=250)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['offer', 'offer_type'],
                name='unique_offer_type_per_offer',
            )
        ]

    def __str__(self):
        return f'Offerdetail({self.id}) {self.offer_type}'
    
