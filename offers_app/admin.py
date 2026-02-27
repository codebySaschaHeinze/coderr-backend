from django.contrib import admin

from .models import Offer, OfferDetail


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):


    list_display = ('id', 'user', 'title', 'created_at')
    search_fields = ('title', 'user__username', 'user__email')
    list_filter = ('created_at',)
    list_select_related = ('user',)


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
 

    list_display = ('id', 'offer', 'offer_type', 'title', 'price', 'delivery_time_in_days', 'revisions')
    search_fields = ('title', 'offer__title', 'offer__user__username', 'offer__user__email')
    list_filter = ('offer_type',)
    list_select_related = ('offer', 'offer__user')