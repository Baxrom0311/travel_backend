from django.urls import path
from .views import TourListView, TourDetailView

urlpatterns = [
    path('', TourListView.as_view(), name='tour-list'),
    path('<slug:slug>/', TourDetailView.as_view(), name='tour-detail'),
]
