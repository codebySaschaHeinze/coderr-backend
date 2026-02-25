import django_filters

from reviews_app.models import Review


class ReviewFilter(django_filters.FilterSet):
    """Filter set for review list queries."""

    business_user_id = django_filters.NumberFilter(field_name='business_user_id')
    reviewer_id = django_filters.NumberFilter(field_name='reviewer_id')

    class Meta:
        """Configuration for available review filters."""

        model = Review
        fields = [
            'business_user_id',
            'reviewer_id',
        ]