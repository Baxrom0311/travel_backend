from django.urls import path
from .views import TransportDetailView, TransportListView, transport_options

urlpatterns = [
    path('transport/', TransportListView.as_view(), name='transport-list'),
    path('transport/options/', transport_options, name='transport-options'),
    path('transport/<int:pk>/', TransportDetailView.as_view(), name='transport-detail'),
]
