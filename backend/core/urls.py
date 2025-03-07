# core/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, AuctionCreateView, AuctionListView, AuctionDetailView,
    PlaceBidView, FinalizeAuctionView, UserProfileView, UserBidsView, UserSellingItemsView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auctions/', AuctionListView.as_view(), name='auction_list'),
    path('auctions/create/', AuctionCreateView.as_view(), name='auction_create'),
    path('auctions/<int:pk>/', AuctionDetailView.as_view(), name='auction_detail'),
    path('auctions/<int:auction_id>/bid/', PlaceBidView.as_view(), name='place_bid'),
    path('auctions/<int:auction_id>/finalize/', FinalizeAuctionView.as_view(), name='finalize_auction'),
    
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('user-bids/', UserBidsView.as_view(), name='user-bids'),
    path('user-selling-items/', UserSellingItemsView.as_view(), name='user-selling-items'),
]
