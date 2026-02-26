from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from profile_app.models import Profile


class Command(BaseCommand):
    """Seed or update demo guest users for frontend guest login buttons."""

    help = 'Create or update guest users for customer and business login.'

    def handle(self, *args, **options):
        """Create or update the predefined guest accounts and profiles."""
        user_model = get_user_model()

        guest_accounts = [
            {
                'username': 'andrey',
                'password': 'asdasd',
                'email': 'andrey@example.com',
                'user_type': 'customer',
            },
            {
                'username': 'kevin',
                'password': 'asdasd24',
                'email': 'kevin@example.com',
                'user_type': 'business',
            },
        ]

        for account in guest_accounts:
            self.upsert_guest(user_model=user_model, **account)

        self.stdout.write(self.style.SUCCESS('Guest users seeded successfully.'))

    def upsert_guest(self, user_model, username, password, email, user_type):
        """
        Create a guest user if it does not exist, otherwise update it.

        Existing users are updated to ensure credentials and user type stay in
        sync with the frontend guest login configuration.
        """
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'type': user_type,
            },
        )

        user.email = email
        user.type = user_type
        user.is_active = True
        user.set_password(password)
        user.save()

        Profile.objects.get_or_create(user=user)

        status_text = 'created' if created else 'updated'
        self.stdout.write(f'- {username}: {status_text} (profile ok)')