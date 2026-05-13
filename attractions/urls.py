from django.urls import path
from .views import (
    AttractionListView,
    AttractionDetailView,
    attraction_options,
    attraction_related,
)

urlpatterns = [
    path('', AttractionListView.as_view(), name='attraction-list'),
    path('options/', attraction_options, name='attraction-options'),
    path('<int:pk>/', AttractionDetailView.as_view(), name='attraction-detail'),
    path('<int:pk>/related/', attraction_related, name='attraction-related'),
]
