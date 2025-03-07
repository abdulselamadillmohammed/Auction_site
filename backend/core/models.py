# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    # 'username' is unique by default. The 'verified' flag will be used to mark accounts verified by your system.
    verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username

class Auction(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_now_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='auction_images/', null=True, blank=True)


    created_by = models.ForeignKey(User, related_name='auctions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    
    winner = models.ForeignKey(User, null=True, blank=True, related_name='won_auctions', on_delete=models.SET_NULL)
    
    # Placeholder for Stripe integration (e.g., to store a payment intent or charge ID)
    # stripe_payment_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

    def finalize(self):
        """
        Finalizes the auction: if the auction has ended, determines the highest bid,
        sets the winner, and marks the auction as inactive.
        """
        if self.is_active and self.end_time < timezone.now():
            highest_bid = self.bids.order_by('-bid_amount').first()
            if highest_bid:
                self.winner = highest_bid.bidder
            self.is_active = False
            self.save()

class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, related_name='bids', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} bid {self.bid_amount} on {self.auction.title}"
