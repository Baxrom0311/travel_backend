from django.urls import path
from .views import ReviewCreateView, list_reviews

urlpatterns = [
    path('', ReviewCreateView.as_view(), name='review-create'),
    path('<str:target_type>/<int:target_id>/', list_reviews, name='review-list'),
]
