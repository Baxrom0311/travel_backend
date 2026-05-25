from rest_framework import generics, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from utils.lang import LangMixin
from utils.cache import PublicCacheMixin
from utils.query_params import reject_unknown_query_params
from .models import Restaurant, Cuisine
from .serializers import (
    RestaurantListSerializer, RestaurantDetailSerializer, CuisineSerializer,
)


class RestaurantFilterSerializer(serializers.Serializer):
    city = serializers.ChoiceField(choices=Restaurant.CITY_CHOICES, required=False)
    featured = serializers.BooleanField(required=False)
    cuisine = serializers.IntegerField(min_value=1, required=False)
    price_range = serializers.ChoiceField(choices=Restaurant.PRICE_CHOICES, required=False)
    search = serializers.CharField(max_length=100, required=False)
    halal = serializers.BooleanField(required=False)
    vegetarian = serializers.BooleanField(required=False)
    ordering = serializers.ChoiceField(
        choices=['rating', '-rating', 'name', '-name', 'price_range', '-price_range'],
        required=False,
    )


class RestaurantListView(PublicCacheMixin, LangMixin, generics.ListAPIView):
    serializer_class = RestaurantListSerializer

    def get_queryset(self):
        qs = Restaurant.objects.prefetch_related('images', 'cuisines').all()
        reject_unknown_query_params(
            self.request.query_params,
            {'city', 'featured', 'cuisine', 'price_range', 'search', 'halal', 'vegetarian', 'ordering'}
        )
        filters = RestaurantFilterSerializer(data=self.request.query_params.dict())
        filters.is_valid(raise_exception=True)
        p = filters.validated_data

        if p.get('city'): qs = qs.filter(city=p['city'])
        if 'featured' in p: qs = qs.filter(is_featured=p['featured'])
        if p.get('cuisine'): qs = qs.filter(cuisines__id=p['cuisine'])
        if p.get('price_range'): qs = qs.filter(price_range=p['price_range'])
        if p.get('search'):
            s = p['search']
            qs = qs.filter(Q(name__icontains=s) | Q(description_uz__icontains=s))
        if 'halal' in p: qs = qs.filter(is_halal=p['halal'])
        if 'vegetarian' in p: qs = qs.filter(is_vegetarian_friendly=p['vegetarian'])
        return qs.order_by(p.get('ordering', '-rating')).distinct()


class RestaurantDetailView(LangMixin, generics.RetrieveAPIView):
    queryset = Restaurant.objects.prefetch_related('images', 'cuisines')
    serializer_class = RestaurantDetailSerializer


class CuisineListView(LangMixin, generics.ListAPIView):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer
    pagination_class = None


@api_view(['GET'])
def restaurant_options(request):
    reject_unknown_query_params(request.query_params, set())
    lang = request.query_params.get('lang', 'uz')
    return Response({
        'success': True,
        'cities': [{'value': v, 'label': l} for v, l in Restaurant.CITY_CHOICES],
        'price_ranges': [{'value': v, 'label': l} for v, l in Restaurant.PRICE_CHOICES],
        'ordering': ['rating', '-rating', 'name', '-name', 'price_range', '-price_range'],
        'cuisines': CuisineSerializer(
            Cuisine.objects.all(), many=True, context={'request': request, 'lang': lang}
        ).data,
    })


@api_view(['GET'])
def restaurant_related(request, pk: int):
    """GET /api/restaurants/{id}/related/"""
    reject_unknown_query_params(request.query_params, set())
    try:
        restaurant = Restaurant.objects.get(pk=pk)
    except Restaurant.DoesNotExist:
        return Response({'success': False, 'error': 'Not found'}, status=404)

    related = Restaurant.objects.prefetch_related('images', 'cuisines').filter(
        city=restaurant.city,
    ).exclude(pk=pk).order_by('-rating')[:4]

    lang = request.query_params.get('lang', 'uz')
    return Response({
        'success': True,
        'data': RestaurantListSerializer(related, many=True, context={'request': request, 'lang': lang}).data,
    })
