"""Hotels views — faqat hotels/amenities bilan bog'liq."""
from rest_framework import generics, serializers, permissions, status as drf_status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, Count, Max, Min

from utils.lang import LangMixin
from utils.cache import PublicCacheMixin
from utils.query_params import reject_unknown_query_params
from .models import Amenity, Hotel, Booking
from .serializers import (
    AmenitySerializer,
    HotelDetailSerializer,
    HotelFilterSerializer,
    HotelListSerializer,
    BookingSerializer,
)
from .utils import send_booking_confirmation


class HotelListView(PublicCacheMixin, LangMixin, generics.ListAPIView):
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

    def list(self, request, *args, **kwargs):
        reject_unknown_query_params(request.query_params, set())
        return super().list(request, *args, **kwargs)


@api_view(['GET'])
def hotel_stats(request):
    """GET /api/hotels/stats/"""
    reject_unknown_query_params(request.query_params, set())
    from django.utils.cache import patch_cache_control
    resp = Response({
        'success': True,
        'total_hotels': Hotel.objects.count(),
        'urgench_hotels': Hotel.objects.filter(city='urgench').count(),
        'khiva_hotels': Hotel.objects.filter(city='khiva').count(),
        'featured': Hotel.objects.filter(is_featured=True).count(),
        'total_images': Hotel.objects.aggregate(total=Count('images'))['total'],
    })
    patch_cache_control(resp, public=True, max_age=300)
    return resp


@api_view(['GET'])
def hotel_options(request):
    """GET /api/hotels/options/"""
    reject_unknown_query_params(request.query_params, set())
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
    reject_unknown_query_params(request.query_params, set())
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


# ============ BOOKINGS ============

class BookingListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/bookings/"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('hotel')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            send_booking_confirmation(serializer.instance)
            return Response(
                {'success': True, 'data': serializer.data},
                status=drf_status.HTTP_201_CREATED,
            )
        return Response({'success': False, 'errors': serializer.errors}, status=drf_status.HTTP_400_BAD_REQUEST)


class BookingDetailView(generics.RetrieveAPIView):
    """GET /api/bookings/{id}/"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('hotel')


class BookingCancelView(generics.UpdateAPIView):
    """PATCH /api/bookings/{id}/cancel/"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('hotel')

    def patch(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.status in ('cancelled', 'completed'):
            return Response(
                {'success': False, 'error': 'Bu bronni bekor qilib bo\'lmaydi.'},
                status=drf_status.HTTP_400_BAD_REQUEST,
            )
        booking.status = 'cancelled'
        booking.save(update_fields=['status', 'updated_at'])
        return Response({'success': True, 'data': BookingSerializer(booking).data})


@api_view(['GET'])
def booking_availability(request, pk: int):
    """GET /api/hotels/{id}/availability/?check_in=...&check_out=..."""
    from datetime import date as date_type
    reject_unknown_query_params(request.query_params, {'check_in', 'check_out'})

    check_in_str = request.query_params.get('check_in')
    check_out_str = request.query_params.get('check_out')
    if not check_in_str or not check_out_str:
        return Response({'success': False, 'error': 'check_in and check_out required'}, status=400)

    try:
        check_in = date_type.fromisoformat(check_in_str)
        check_out = date_type.fromisoformat(check_out_str)
    except (ValueError, TypeError):
        return Response({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    if check_in >= check_out:
        return Response({'success': False, 'error': 'check_out must be after check_in'}, status=400)

    try:
        hotel = Hotel.objects.get(pk=pk)
    except Hotel.DoesNotExist:
        return Response({'success': False, 'error': 'Hotel not found'}, status=404)

    conflicting = Booking.objects.filter(
        hotel=hotel,
        status__in=('pending', 'confirmed'),
        check_in__lt=check_out,
        check_out__gt=check_in,
    ).count()

    return Response({
        'success': True,
        'available': conflicting == 0,
        'hotel_id': pk,
        'check_in': check_in.isoformat(),
        'check_out': check_out.isoformat(),
    })
