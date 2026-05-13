from django.urls import path
from .views import EventListView, EventDetailView, event_options

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('options/', event_options, name='event-options'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
]
