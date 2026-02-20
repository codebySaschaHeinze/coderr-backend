from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer
from reviews_app.models import Review


User = get_user_model()


class BaseInfoView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        review_count = Review.objects.count()
        avg = Review.objects.aggregate(v=Avg('rating'))['v']
        average_rating = round(float(avg), 1) if avg is not None else 0.0

        business_profile_count = User.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        return Response(
            {
                "review_count": review_count,
                "average_rating": average_rating,
                "business_profile_count": business_profile_count,
                "offer_count": offer_count,
            }
        )