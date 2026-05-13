from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, MyTokenObtainPairView, ProfileView,
    change_password,
    FavoriteListCreateView, FavoriteDeleteView, toggle_favorite,
)

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    
    # Profile
    path('me/', ProfileView.as_view(), name='profile'),
    path('change-password/', change_password, name='change-password'),
    
    # Favorites (synced)
    path('favorites/', FavoriteListCreateView.as_view(), name='favorites'),
    path('favorites/toggle/', toggle_favorite, name='toggle-favorite'),
    path('favorites/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
]
