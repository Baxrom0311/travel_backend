from django.urls import path
from .views import testimonials_list

urlpatterns = [
    path('', testimonials_list, name='testimonials_list'),
]
