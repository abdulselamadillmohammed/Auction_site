'''
# core/management/commands/finalize_auctions.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Auction

class Command(BaseCommand):
    help = "Finalize auctions that have expired."

    def handle(self, *args, **options):
        expired_auctions = Auction.objects.filter(is_active=True, end_time__lt=timezone.now())
        for auction in expired_auctions:
            auction.finalize()
            self.stdout.write(self.style.SUCCESS(f"Auction '{auction.title}' finalized."))

'''