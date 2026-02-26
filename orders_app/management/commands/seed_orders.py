from decimal import Decimal
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from orders_app.models import Order

User = get_user_model()


SEED_PREFIX = "[SEED]"


class Command(BaseCommand):
    help = "Seed demo orders (customer<->business) for local development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=12,
            help="How many orders to create (default: 12).",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing seed orders before creating new ones.",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=1337,
            help="Random seed for deterministic results (default: 1337).",
        )

    def handle(self, *args, **options):
        count = options["count"]
        do_reset = options["reset"]
        rnd_seed = options["seed"]

        random.seed(rnd_seed)

        if do_reset:
            deleted, _ = Order.objects.filter(title__startswith=SEED_PREFIX).delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} seed orders."))

        users = list(User.objects.all())
        if len(users) < 2:
            self.stdout.write(
                self.style.ERROR("Need at least 2 users to seed orders (customer + business).")
            )
            return

        guest_user = self._find_guest_user(users)
        business_users = [u for u in users if u != guest_user]
        if not business_users:
            self.stdout.write(self.style.ERROR("No business users found (besides guest)."))
            return

        templates = self._order_templates()

        created = 0
        for i in range(1, count + 1):
            t = random.choice(templates)
            business_user = random.choice(business_users)

            title = f"{SEED_PREFIX} {t['title']} #{i:03d}"

            _, was_created = Order.objects.get_or_create(
                title=title,
                defaults={
                    "customer_user": guest_user,
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

    def _find_guest_user(self, users):
        # Robust: try to detect a "guest" user by common patterns, else fallback to first user.
        for u in users:
            username = (getattr(u, "username", "") or "").lower()
            email = (getattr(u, "email", "") or "").lower()
            if "guest" in username or "guest" in email:
                return u
        return users[0]

    def _order_templates(self):
        # Keep it small and plausible. Prices as Decimal.
        return [
            {
                "title": "Landingpage Audit",
                "revisions": 2,
                "delivery_days": 3,
                "price": Decimal("49.00"),
                "features": ["SEO basics", "Semantic HTML hints", "Performance notes"],
                "offer_type": "basic",
            },
            {
                "title": "API Endpoint Review",
                "revisions": 1,
                "delivery_days": 2,
                "price": Decimal("79.00"),
                "features": ["Status codes", "Serializer feedback", "Permissions check"],
                "offer_type": "standard",
            },
            {
                "title": "Bugfix Paket",
                "revisions": 3,
                "delivery_days": 5,
                "price": Decimal("129.00"),
                "features": ["Repro steps", "Fix", "Regression check"],
                "offer_type": "premium",
            },
            {
                "title": "UI Feinschliff",
                "revisions": 2,
                "delivery_days": 4,
                "price": Decimal("99.00"),
                "features": ["Spacing", "Typography", "Hover/Focus states"],
                "offer_type": "standard",
            },
        ]