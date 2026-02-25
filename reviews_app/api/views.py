from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response

from reviews_app.models import Review
from .filters import ReviewFilter
from .permissions import IsReviewOwner
from .serializers import ReviewCreateSerializer, ReviewSerializer, ReviewUpdateSerializer
from .validators import (
    validate_customer_can_create_review,
    validate_no_duplicate_review,
    validate_only_allowed_patch_fields,
)


class ReviewListCreateView(generics.ListCreateAPIView):
    """List reviews and allow authenticated customers to create reviews."""

    queryset = Review.objects.all().order_by('-updated_at')
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = [
        'updated_at',
        'rating',
    ]

    def get_serializer_class(self):
        """Use create serializer for POST and read serializer otherwise."""
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def create(self, request, *args, **kwargs):
        """Create a review after role and duplicate checks."""
        validate_customer_can_create_review(request.user)

        business_user_id = request.data.get('business_user')
        exists = bool(
            business_user_id and Review.objects.filter(
                business_user_id=business_user_id,
                reviewer=request.user,
            ).exists()
        )
        validate_no_duplicate_review(exists)

        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            review = serializer.save()
        except Exception:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single review."""

    lookup_url_kwarg = 'id'
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """Require ownership for patch/delete and authentication for reads."""
        if self.request.method in ('PATCH', 'DELETE'):
            return [permissions.IsAuthenticated(), IsReviewOwner()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        """Use update serializer for PATCH and read serializer otherwise."""
        if self.request.method == 'PATCH':
            return ReviewUpdateSerializer
        return ReviewSerializer

    def patch(self, request, *args, **kwargs):
        """Update allowed review fields and return the updated review."""
        allowed_fields = {'rating', 'description'}
        validate_only_allowed_patch_fields(request.data, allowed_fields)

        review = self.get_object()
        serializer = self.get_serializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ReviewSerializer(review).data, status=status.HTTP_200_OK)