from django.urls import path
from .views import (
    HotelListView,
    HotelDetailView,
    AmenityListView,
    hotel_stats,
    hotel_options,
    hotels_related,
    booking_availability,
    BookingListCreateView,
    BookingDetailView,
    BookingCancelView,
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
    path('hotels/<int:pk>/availability/', booking_availability, name='hotel-availability'),

    # Bookings
    path('bookings/', BookingListCreateView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]
