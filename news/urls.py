from django.urls import path
from .views import NewsListView, NewsDetailView, news_options

urlpatterns = [
    path('', NewsListView.as_view(), name='news-list'),
    path('options/', news_options, name='news-options'),
    path('<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),
]
