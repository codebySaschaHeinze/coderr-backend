from decimal import Decimal
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from orders_app.models import Order

User = get_user_model()

SEED_PREFIX = "[SEED]"
CUSTOMER_GUEST_EMAIL = "andrey@example.com"
BUSINESS_GUEST_EMAIL = "kevin@example.com"


class Command(BaseCommand):
    help = "Seed demo orders for local development (uses guest accounts if available)."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=12)
        parser.add_argument("--reset", action="store_true")
        parser.add_argument("--seed", type=int, default=1337)

    def handle(self, *args, **options):
        count = options["count"]
        do_reset = options["reset"]
        rnd_seed = options["seed"]
        random.seed(rnd_seed)

        if do_reset:
            deleted, _ = Order.objects.filter(title__startswith=SEED_PREFIX).delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} seed orders."))

        customer = self._get_user_by_email(CUSTOMER_GUEST_EMAIL)
        business_guest = self._get_user_by_email(BUSINESS_GUEST_EMAIL)

        if not customer or not business_guest:
            self.stdout.write(
                self.style.ERROR(
                    "Guest users not found. Run `python manage.py seed_guest_user` first."
                )
            )
            return
        
        business_users = list(User.objects.filter(type="business"))
        if not business_users:
            business_users = [business_guest]

        templates = self._order_templates()

        created = 0
        for i in range(1, count + 1):
            t = random.choice(templates)
            business_user = random.choice(business_users)

            title = f"{SEED_PREFIX} {t['title']} #{i:03d}"

            _, was_created = Order.objects.get_or_create(
                title=title,
                defaults={
                    "customer_user": customer,
                    "business_user": business_user,
                    "revisions": t["revisions"],
                    "delivery_time_in_days": t["delivery_days"],
                    "price": t["price"],
                    "features": t["features"],
                    "offer_type": t["offer_type"],
                    "status": random.choice(["in_progress", "completed", "cancelled"]),
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} seed orders."))

    def _get_user_by_email(self, email: str):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def _order_templates(self):
        return [
            {
                "title": "Landingpage-Analyse",
                "revisions": 2,
                "delivery_days": 3,
                "price": Decimal("49.00"),
                "features": ["SEO-Grundlagen", "Hinweise zu semantischem HTML", "Performance-Notizen"],
                "offer_type": "basic",
            },
            {
                "title": "API-Endpunkt-Review",
                "revisions": 1,
                "delivery_days": 2,
                "price": Decimal("79.00"),
                "features": ["Statuscodes", "Serializer-Feedback", "Prüfung der Berechtigungen"],
                "offer_type": "standard",
            },
            {
                "title": "Bugfix-Paket",
                "revisions": 3,
                "delivery_days": 5,
                "price": Decimal("129.00"),
                "features": ["Reproduktionsschritte", "Fix", "Regressionstest"],
                "offer_type": "premium",
            },
        ]