from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from offers_app.models import Offer, OfferDetail


User = get_user_model()


class Command(BaseCommand):
    help = 'Seed demo offers (Offers + 3 OfferDetails each).'

    def handle(self, *args, **options):
        business_user = User.objects.filter(type='business').first()
        if not business_user:
            self.stdout.write(self.style.ERROR('No business user found. Run your guest-user seed first.'))
            return

        if Offer.objects.exists():
            self.stdout.write(self.style.WARNING('Offers already exist. Seed aborted.'))
            return

        demo_offers = [
            {
    'title': 'Webseiten-Design',
    'description': 'Moderne, responsive Landingpage + Styleguide.',
    'details': [
        {
            'title': 'Basic',
            'revisions': 2,
            'delivery_time_in_days': 5,
            'price': '199.00',
            'features': ['Landingpage', 'Responsives Layout'],
            'offer_type': 'basic',
        },
        {
            'title': 'Standard',
            'revisions': 5,
            'delivery_time_in_days': 7,
            'price': '399.00',
            'features': ['2 Seiten', 'Responsives Layout', 'SEO-Basics'],
            'offer_type': 'standard',
        },
        {
            'title': 'Premium',
            'revisions': 10,
            'delivery_time_in_days': 10,
            'price': '699.00',
            'features': ['Bis zu 5 Seiten', 'Animationen', 'SEO + Performance'],
            'offer_type': 'premium',
        },
    ],
},
{
    'title': 'Logo & Marken-Startpaket',
    'description': 'Sauberes Logo + kleines Marken-Starter-Kit.',
    'details': [
        {
            'title': 'Basic',
            'revisions': 2,
            'delivery_time_in_days': 3,
            'price': '99.00',
            'features': ['1 Logo-Konzept', 'PNG-Export'],
            'offer_type': 'basic',
        },
        {
            'title': 'Standard',
            'revisions': 4,
            'delivery_time_in_days': 5,
            'price': '199.00',
            'features': ['2 Konzepte', 'PNG + SVG', 'Farben'],
            'offer_type': 'standard',
        },
        {
            'title': 'Premium',
            'revisions': 6,
            'delivery_time_in_days': 7,
            'price': '349.00',
            'features': ['3 Konzepte', 'Komplettes Marken-Kit', 'Mini-Styleguide'],
            'offer_type': 'premium',
        },
    ],
},
{
    'title': 'API-Integration',
    'description': 'Integration einer REST-API in dein Frontend.',
    'details': [
        {
            'title': 'Basic',
            'revisions': 1,
            'delivery_time_in_days': 2,
            'price': '149.00',
            'features': ['1 Endpoint', 'Fehlerbehandlung'],
            'offer_type': 'basic',
        },
        {
            'title': 'Standard',
            'revisions': 2,
            'delivery_time_in_days': 4,
            'price': '299.00',
            'features': ['Bis zu 3 Endpoints', 'Loading-States', 'Doku'],
            'offer_type': 'standard',
        },
        {
            'title': 'Premium',
            'revisions': 3,
            'delivery_time_in_days': 6,
            'price': '499.00',
            'features': ['Bis zu 6 Endpoints', 'Auth-Flow', 'Tests'],
            'offer_type': 'premium',
        },
    ],
},
        ]

        created_offers = 0
        created_details = 0

        for o in demo_offers:
            offer = Offer.objects.create(
                user=business_user,
                title=o['title'],
                description=o['description'],
            )
            created_offers += 1

            for d in o['details']:
                OfferDetail.objects.create(
                    offer=offer,
                    title=d['title'],
                    revisions=d['revisions'],
                    delivery_time_in_days=d['delivery_time_in_days'],
                    price=d['price'],
                    features=d['features'],
                    offer_type=d['offer_type'],
                )
                created_details += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Seed completed: {created_offers} offers, {created_details} offer details created.'
            )
        )