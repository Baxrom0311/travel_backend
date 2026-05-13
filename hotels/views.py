"""Hotels views — faqat hotels/amenities bilan bog'liq."""
from rest_framework import generics, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, Count, Max, Min

from utils.lang import LangMixin
from utils.query_params import reject_unknown_query_params
from .models import Amenity, Hotel
from .serializers import (
    AmenitySerializer,
    HotelDetailSerializer,
    HotelFilterSerializer,
    HotelListSerializer,
)


class HotelListView(LangMixin, generics.ListAPIView):
    """GET /api/hotels/ — with filters & search."""
    serializer_class = HotelListSerializer

    def get_queryset(self):
        qs = Hotel.objects.prefetch_related('images', 'amenities').all()

        reject_unknown_query_params(
            self.request.query_params,
            {'city', 'featured', 'stars', 'search', 'amenity', 'min_price', 'max_price', 'ordering'},
        )
        filters = HotelFilterSerializer(data=self.request.query_params.dict())
        filters.is_valid(raise_exception=True)
        params = filters.validated_data

        if params.get('city'):
            qs = qs.filter(city=params['city'])
        if 'featured' in params:
            qs = qs.filter(is_featured=params['featured'])
        if params.get('stars'):
            qs = qs.filter(stars=params['stars'])
        if params.get('search'):
            s = params['search']
            qs = qs.filter(
                Q(name__icontains=s) | Q(name_en__icontains=s) | Q(name_ru__icontains=s) |
                Q(address__icontains=s) | Q(description_uz__icontains=s)
            )
        if params.get('amenity'):
            qs = qs.filter(amenities__id=params['amenity'])
        if 'min_price' in params:
            qs = qs.filter(price_per_night__gte=params['min_price'])
        if 'max_price' in params:
            qs = qs.filter(price_per_night__lte=params['max_price'])

        qs = qs.order_by(params.get('ordering', '-rating'))
        return qs.distinct()


class HotelDetailView(LangMixin, generics.RetrieveAPIView):
    """GET /api/hotels/{id}/"""
    queryset = Hotel.objects.prefetch_related('images', 'amenities').all()
    serializer_class = HotelDetailSerializer


class AmenityListView(LangMixin, generics.ListAPIView):
    """GET /api/amenities/"""
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    pagination_class = None


@api_view(['GET'])
def hotel_stats(request):
    """GET /api/hotels/stats/"""
    return Response({
        'success': True,
        'total_hotels': Hotel.objects.count(),
        'urgench_hotels': Hotel.objects.filter(city='urgench').count(),
        'khiva_hotels': Hotel.objects.filter(city='khiva').count(),
        'featured': Hotel.objects.filter(is_featured=True).count(),
        'total_images': Hotel.objects.aggregate(total=Count('images'))['total'],
    })


@api_view(['GET'])
def hotel_options(request):
    """GET /api/hotels/options/"""
    price = Hotel.objects.aggregate(min=Min('price_per_night'), max=Max('price_per_night'))
    amenities = AmenitySerializer(
        Amenity.objects.all(), many=True,
        context={'request': request, 'lang': request.query_params.get('lang', 'uz')},
    )
    return Response({
        'success': True,
        'cities': [{'value': v, 'label': l} for v, l in Hotel.CITY_CHOICES],
        'stars': [1, 2, 3, 4, 5],
        'price': {'min': price['min'], 'max': price['max']},
        'ordering': ['rating', '-rating', 'price_per_night', '-price_per_night', 'stars', '-stars'],
        'amenities': amenities.data,
    })


@api_view(['GET'])
def hotels_related(request, pk: int):
    """GET /api/hotels/{id}/related/ — shunga o'xshash mehmonxonalar."""
    try:
        hotel = Hotel.objects.get(pk=pk)
    except Hotel.DoesNotExist:
        return Response({'success': False, 'error': 'Hotel not found'}, status=404)

    related = Hotel.objects.prefetch_related('images').filter(
        city=hotel.city,
    ).exclude(pk=hotel.pk).order_by('-rating')[:4]

    lang = request.query_params.get('lang', 'uz')
    return Response({
        'success': True,
        'data': HotelListSerializer(related, many=True, context={'request': request, 'lang': lang}).data,
    })
