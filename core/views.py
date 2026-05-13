"""Core views: home summary, API overview, search."""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers

from hotels.models import Hotel
from hotels.serializers import HotelListSerializer
from transport.models import TransportRoute
from transport.serializers import TransportRouteSerializer
from attractions.models import Attraction
from attractions.serializers import AttractionListSerializer
from events.models import Event
from events.serializers import EventListSerializer
from news.models import News
from news.serializers import NewsListSerializer
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantListSerializer
from tours.models import Tour
from tours.serializers import TourListSerializer

from utils.lang import get_lang
from utils.query_params import reject_unknown_query_params


class HomeQuerySerializer(serializers.Serializer):
    hotel_limit = serializers.IntegerField(min_value=1, max_value=20, required=False, default=6)
    transport_limit = serializers.IntegerField(min_value=1, max_value=20, required=False, default=3)
    attraction_limit = serializers.IntegerField(min_value=1, max_value=20, required=False, default=6)
    event_limit = serializers.IntegerField(min_value=1, max_value=20, required=False, default=4)
    news_limit = serializers.IntegerField(min_value=1, max_value=20, required=False, default=4)
    restaurant_limit = serializers.IntegerField(min_value=1, max_value=20, required=False, default=4)
    tour_limit = serializers.IntegerField(min_value=1, max_value=20, required=False, default=3)


@api_view(['GET'])
def home_summary(request):
    """GET /api/home/ — Bosh sahifa uchun aggregated data."""
    allowed = {'hotel_limit', 'transport_limit', 'attraction_limit', 'event_limit', 'news_limit', 'restaurant_limit', 'tour_limit', 'lang'}
    reject_unknown_query_params(request.query_params, allowed)
    q = HomeQuerySerializer(data=request.query_params.dict())
    q.is_valid(raise_exception=True)
    p = q.validated_data
    lang = get_lang(request)
    ctx = {'request': request, 'lang': lang}

    hotels = Hotel.objects.prefetch_related('images', 'amenities').filter(is_featured=True).order_by('-rating')[:p['hotel_limit']]
    transport = TransportRoute.objects.all()[:p['transport_limit']]
    attractions = Attraction.objects.prefetch_related('images').filter(is_featured=True).order_by('order')[:p['attraction_limit']]
    events = Event.objects.filter(is_active=True, is_featured=True).prefetch_related('images')[:p['event_limit']]
    news = News.objects.filter(is_published=True, is_featured=True).prefetch_related('images')[:p['news_limit']]
    restaurants = Restaurant.objects.prefetch_related('images', 'cuisines').filter(is_featured=True)[:p['restaurant_limit']]
    tours = Tour.objects.filter(is_active=True, is_featured=True)[:p['tour_limit']]

    return Response({
        'success': True,
        'lang': lang,
        'stats': {
            'total_hotels': Hotel.objects.count(),
            'urgench_hotels': Hotel.objects.filter(city='urgench').count(),
            'khiva_hotels': Hotel.objects.filter(city='khiva').count(),
            'total_attractions': Attraction.objects.count(),
            'featured_attractions': Attraction.objects.filter(is_featured=True).count(),
            'transport_routes': TransportRoute.objects.count(),
            'total_events': Event.objects.filter(is_active=True).count(),
            'total_news': News.objects.filter(is_published=True).count(),
            'total_restaurants': Restaurant.objects.count(),
            'total_tours': Tour.objects.filter(is_active=True).count(),
        },
        'featured_hotels': HotelListSerializer(hotels, many=True, context=ctx).data,
        'transport': TransportRouteSerializer(transport, many=True, context=ctx).data,
        'attractions': AttractionListSerializer(attractions, many=True, context=ctx).data,
        'events': EventListSerializer(events, many=True, context=ctx).data,
        'news': NewsListSerializer(news, many=True, context=ctx).data,
        'restaurants': RestaurantListSerializer(restaurants, many=True, context=ctx).data,
        'tours': TourListSerializer(tours, many=True, context=ctx).data,
    })


@api_view(['GET'])
def api_overview(request):
    return Response({
        'success': True,
        'service': 'Visit Khorezm API',
        'version': '3.0',
        'supported_langs': ['uz', 'en', 'ru'],
        'endpoints': {
            'home': '/api/home/',
            'search': '/api/search/?q=...',
            'hotels': '/api/hotels/',
            'amenities': '/api/amenities/',
            'transport': '/api/transport/',
            'attractions': '/api/attractions/',
            'events': '/api/events/',
            'news': '/api/news/',
            'restaurants': '/api/restaurants/',
            'tours': '/api/tours/',
            'contact': '/api/contact/',
            'reviews': '/api/reviews/',
            'newsletter': '/api/newsletter/subscribe/',
        },
    })


@api_view(['GET'])
def global_search(request):
    """GET /api/search/?q=..."""
    q = request.query_params.get('q', '').strip()
    if len(q) < 2:
        return Response({'success': False, 'error': 'Query must be at least 2 characters'}, status=400)

    lang = get_lang(request)
    ctx = {'request': request, 'lang': lang}
    limit = min(int(request.query_params.get('limit', 5)), 20)

    from django.db.models import Q

    hotels = Hotel.objects.prefetch_related('images').filter(
        Q(name__icontains=q) | Q(name_en__icontains=q) | Q(name_ru__icontains=q)
    )[:limit]
    attractions = Attraction.objects.prefetch_related('images').filter(
        Q(name_uz__icontains=q) | Q(name_en__icontains=q) | Q(name_ru__icontains=q)
    )[:limit]
    events = Event.objects.filter(
        Q(title_uz__icontains=q) | Q(title_en__icontains=q) | Q(title_ru__icontains=q),
        is_active=True,
    )[:limit]
    news = News.objects.filter(
        Q(title_uz__icontains=q) | Q(title_en__icontains=q) | Q(title_ru__icontains=q),
        is_published=True,
    )[:limit]
    restaurants = Restaurant.objects.prefetch_related('images').filter(
        Q(name__icontains=q) | Q(name_en__icontains=q) | Q(name_ru__icontains=q)
    )[:limit]
    tours = Tour.objects.filter(
        Q(title_uz__icontains=q) | Q(title_en__icontains=q) | Q(title_ru__icontains=q),
        is_active=True,
    )[:limit]

    return Response({
        'success': True,
        'query': q,
        'results': {
            'hotels': HotelListSerializer(hotels, many=True, context=ctx).data,
            'attractions': AttractionListSerializer(attractions, many=True, context=ctx).data,
            'events': EventListSerializer(events, many=True, context=ctx).data,
            'news': NewsListSerializer(news, many=True, context=ctx).data,
            'restaurants': RestaurantListSerializer(restaurants, many=True, context=ctx).data,
            'tours': TourListSerializer(tours, many=True, context=ctx).data,
        },
        'counts': {
            'hotels': hotels.count(),
            'attractions': attractions.count(),
            'events': events.count(),
            'news': news.count(),
            'restaurants': restaurants.count(),
            'tours': tours.count(),
        },
    })
