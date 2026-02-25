from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    """Pagination settings for offer list endpoints."""

    page_size = 10
    page_size_query_param = 'page_size'