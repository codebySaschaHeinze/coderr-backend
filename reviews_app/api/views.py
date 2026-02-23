from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response

from reviews_app.models import Review
from .filters import ReviewFilter
from .permissions import IsReviewOwner
from .serializers import ReviewCreateSerializer, ReviewSerializer, ReviewUpdateSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all().order_by('-updated_at')
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = [
        'updated_at',
        'rating',
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def create(self, request, *args, **kwargs):
        if request.user.type != 'customer':
            return Response(status=status.HTTP_403_FORBIDDEN)

        business_user_id = request.data.get('business_user')
        if business_user_id and Review.objects.filter(
            business_user_id=business_user_id,
            reviewer=request.user
        ).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            review = serializer.save()
        except Exception:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
    

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_url_kwarg = 'id'
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ('PATCH', 'DELETE'):
            return [permissions.IsAuthenticated(), IsReviewOwner()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ReviewUpdateSerializer
        return ReviewSerializer
    
    def patch(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = self.get_serializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ReviewSerializer(review).data, status=status.HTTP_200_OK)