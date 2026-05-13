from django.urls import path
from .views import (
    RestaurantListView, RestaurantDetailView,
    CuisineListView, restaurant_options,
)

urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant-list'),
    path('options/', restaurant_options, name='restaurant-options'),
    path('cuisines/', CuisineListView.as_view(), name='cuisine-list'),
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
]
