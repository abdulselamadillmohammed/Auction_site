# core/views.py
from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer, AuctionSerializer, BidSerializer, PlaceBidSerializer, UserSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Auction, Bid
from django.utils import timezone

#token_authentication = ['rest_framework.authentication.TokenAuthentication']
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication  # Import the correct class

User = get_user_model()

# User registration endpoint
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

# Create a new auction listing
class AuctionCreateView(generics.CreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# List all active auctions
class AuctionListView(generics.ListAPIView):
    queryset = Auction.objects.filter(is_active=True)
    serializer_class = AuctionSerializer
    permission_classes = (permissions.AllowAny,)

# Retrieve auction details
class AuctionDetailView(generics.RetrieveAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = (permissions.AllowAny,)

# Place a bid on an auction
class PlaceBidView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, auction_id):
        try:
            auction = Auction.objects.get(id=auction_id)
        except Auction.DoesNotExist:
            return Response({"error": "Auction not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaceBidSerializer(data=request.data, context={'auction': auction})
        if serializer.is_valid():
            bid = Bid.objects.create(
                auction=auction,
                bidder=request.user,
                bid_amount=serializer.validated_data['bid_amount']
            )
            # Payment Integration Note:
            # At this point, you might integrate Stripe to authorize or capture payment.
            # For example, you could create a Stripe PaymentIntent and save its ID to auction.stripe_payment_id.
            # See Stripe's documentation for details.
            return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]  # Correct the assignment to the actual class
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
class UserBidsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bids = Bid.objects.filter(bidder=request.user).select_related('auction')
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)
class UserSellingItemsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        items = Auction.objects.filter(created_by=request.user)
        serializer = AuctionSerializer(items, many=True)
        return Response(serializer.data)


# Optional: Manually finalize an auction (for admin use)
class FinalizeAuctionView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, auction_id):
        try:
            auction = Auction.objects.get(id=auction_id)
        except Auction.DoesNotExist:
            return Response({"error": "Auction not found."}, status=status.HTTP_404_NOT_FOUND)
        
        auction.finalize()
        winner_username = auction.winner.username if auction.winner else None
        return Response({"message": "Auction finalized.", "winner": winner_username})
