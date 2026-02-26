import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews_app.models import Review

User = get_user_model()

SEED_PREFIX = "[SEED]"
CUSTOMER_GUEST_EMAIL = "andrey@example.com"
BUSINESS_GUEST_EMAIL = "kevin@example.com"


class Command(BaseCommand):
    help = "Seed demo reviews using guest accounts (respects unique constraints)."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true")
        parser.add_argument("--seed", type=int, default=1337)

    def handle(self, *args, **options):
        do_reset = options["reset"]
        rnd_seed = options["seed"]
        random.seed(rnd_seed)

        if do_reset:
            deleted, _ = Review.objects.filter(description__startswith=SEED_PREFIX).delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} seed reviews."))

        reviewer_guest = self._get_user_by_email(CUSTOMER_GUEST_EMAIL)
        business_guest = self._get_user_by_email(BUSINESS_GUEST_EMAIL)

        if not reviewer_guest or not business_guest:
            self.stdout.write(
                self.style.ERROR("Guest users not found. Run `python manage.py seed_guest_user` first.")
            )
            return

        templates = self._templates()

        created = 0

        created += self._upsert_review(
            business_user=business_guest,
            reviewer=reviewer_guest,
            templates=templates,
        )

        other_business_users = (
            User.objects.filter(type="business").exclude(email=BUSINESS_GUEST_EMAIL)
        )
        for bu in other_business_users:
            created += self._upsert_review(
                business_user=bu,
                reviewer=reviewer_guest,
                templates=templates,
            )

        other_reviewers = User.objects.filter(type="customer").exclude(email=CUSTOMER_GUEST_EMAIL)
        for rv in other_reviewers:
            created += self._upsert_review(
                business_user=business_guest,
                reviewer=rv,
                templates=templates,
            )

        self.stdout.write(self.style.SUCCESS(f"Seed reviews upserted. Created new: {created}."))

    def _upsert_review(self, business_user, reviewer, templates) -> int:
        t = random.choice(templates)

        description = f"{SEED_PREFIX} {t['description']}"

        obj, created = Review.objects.update_or_create(
            business_user=business_user,
            reviewer=reviewer,
            defaults={
                "rating": t["rating"],
                "description": description,
            },
        )
        action = "created" if created else "updated"
        self.stdout.write(f"- Review {action}: reviewer={reviewer.email} -> business={business_user.email} ({obj.rating}★)")
        return 1 if created else 0

    def _get_user_by_email(self, email: str):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def _templates(self):
        return [
            {"rating": 5, "description": "Top Kommunikation, schnelle Lieferung."},
            {"rating": 4, "description": "Sauber gearbeitet, kurze Abstimmung, gutes Ergebnis."},
            {"rating": 5, "description": "Sehr zuverlässig und professionell."},
            {"rating": 3, "description": "In Ordnung – ein paar Iterationen waren nötig."},
            {"rating": 2, "description": "Nicht ganz wie erwartet, aber freundlich."},
        ]