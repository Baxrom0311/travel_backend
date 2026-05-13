from django.urls import path
from .views import TransportDetailView, TransportListView, transport_options

urlpatterns = [
    path('', TransportListView.as_view(), name='transport-list'),
    path('options/', transport_options, name='transport-options'),
    path('<int:pk>/', TransportDetailView.as_view(), name='transport-detail'),
]
