# core/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Auction, Bid
from django.utils import timezone

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'verified')
        read_only_fields = ('verified',)  # This flag will be updated by your verification process.

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Users are non-verified by default.
        return user

class AuctionSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    highest_bid = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True)  # Include the image field with URL

    class Meta:
        model = Auction
        fields = ['id', 'created_by', 'highest_bid', 'title', 'description', 'starting_price', 'buy_now_price', 'image', 'created_at', 'end_time', 'is_active', 'winner']
        read_only_fields = ('created_by', 'is_active', 'winner', 'created_at')

    def get_highest_bid(self, obj):
        highest_bid = obj.bids.order_by('-bid_amount').first()
        return highest_bid.bid_amount if highest_bid else None

    def validate_end_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("End time must be in the future.")
        return value

class BidSerializer(serializers.ModelSerializer):
    bidder = serializers.ReadOnlyField(source='bidder.username')
    auction = AuctionSerializer(read_only=True)  # Include the auction details

    class Meta:
        model = Bid
        fields = ['id', 'bidder', 'bid_amount', 'timestamp', 'auction']
        read_only_fields = ('bidder', 'timestamp', 'auction')

'''

class PlaceBidSerializer(serializers.Serializer):
    bid_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        auction = self.context.get('auction')
        if not auction.is_active or auction.end_time < timezone.now():
            raise serializers.ValidationError("Auction is not active.")
        
        current_highest_bid = auction.bids.order_by('-bid_amount').first()
        min_bid = auction.starting_price if current_highest_bid is None else current_highest_bid.bid_amount

        if data['bid_amount'] <= min_bid:
            raise serializers.ValidationError(f"Bid must be greater than the current highest bid ({min_bid}).")
        return data


'''
class PlaceBidSerializer(serializers.Serializer):
    bid_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        auction = self.context.get('auction')
        user = self.context.get('user')  # Assuming the user is passed in the context

        if not auction.is_active or auction.end_time < timezone.now():
            raise serializers.ValidationError("Auction is not active.")
        
        if auction.owner == user:  # Check if the user is the one who posted the auction
            raise serializers.ValidationError("You cannot bid on your own auction.")

        current_highest_bid = auction.bids.order_by('-bid_amount').first()
        min_bid = auction.starting_price if current_highest_bid is None else current_highest_bid.bid_amount

        if data['bid_amount'] <= min_bid:
            raise serializers.ValidationError(f"Bid must be greater than the current highest bid ({min_bid}).")
        
        return data

