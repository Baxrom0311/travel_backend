from django.urls import path
from .views import (
    HotelListView,
    HotelDetailView,
    AmenityListView,
    hotel_stats,
    hotel_options,
    hotels_related,
)

urlpatterns = [
    # Amenities
    path('amenities/', AmenityListView.as_view(), name='amenity-list'),
    
    # Hotels
    path('hotels/', HotelListView.as_view(), name='hotel-list'),
    path('hotels/stats/', hotel_stats, name='hotel-stats'),
    path('hotels/options/', hotel_options, name='hotel-options'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('hotels/<int:pk>/related/', hotels_related, name='hotel-related'),
]
