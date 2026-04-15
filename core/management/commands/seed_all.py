from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run all seed commands in the correct order."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Reset seed data where supported.")
        parser.add_argument("--count-orders", type=int, default=12, help="How many orders to seed.")
        parser.add_argument("--seed", type=int, default=1337, help="Random seed for deterministic results.")

    def handle(self, *args, **options):
        reset = options["reset"]
        count_orders = options["count_orders"]
        rnd_seed = options["seed"]

        call_command("seed_guest_users")

        if reset:
            call_command("seed_offers", reset=True, seed=rnd_seed)
        else:
            call_command("seed_offers")

        if reset:
            call_command("seed_orders", reset=True, count=count_orders, seed=rnd_seed)
        else:
            call_command("seed_orders", count=count_orders, seed=rnd_seed)

        if reset:
            call_command("seed_reviews", reset=True, seed=rnd_seed)
        else:
            call_command("seed_reviews", seed=rnd_seed)

        self.stdout.write(self.style.SUCCESS("All seeds executed."))