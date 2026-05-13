from rest_framework import generics, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone

from utils.lang import LangMixin
from utils.query_params import reject_unknown_query_params
from .models import Event
from .serializers import EventListSerializer, EventDetailSerializer


class EventFilterSerializer(serializers.Serializer):
    featured = serializers.BooleanField(required=False)
    upcoming = serializers.BooleanField(required=False)
    search = serializers.CharField(max_length=100, required=False)
    is_free = serializers.BooleanField(required=False)


class EventListView(LangMixin, generics.ListAPIView):
    """GET /api/events/"""
    serializer_class = EventListSerializer

    def get_queryset(self):
        qs = Event.objects.filter(is_active=True).prefetch_related('images')
        reject_unknown_query_params(
            self.request.query_params,
            {'featured', 'upcoming', 'search', 'is_free'}
        )
        filters = EventFilterSerializer(data=self.request.query_params.dict())
        filters.is_valid(raise_exception=True)
        params = filters.validated_data

        if params.get('featured'):
            qs = qs.filter(is_featured=True)
        if params.get('upcoming'):
            qs = qs.filter(start_date__gte=timezone.now().date())
        if params.get('search'):
            s = params['search']
            qs = qs.filter(
                Q(title_uz__icontains=s) | Q(title_en__icontains=s) |
                Q(description_uz__icontains=s) | Q(location_uz__icontains=s)
            )
        if 'is_free' in params:
            qs = qs.filter(is_free=params['is_free'])

        return qs.order_by('start_date')


class EventDetailView(LangMixin, generics.RetrieveAPIView):
    queryset = Event.objects.prefetch_related('images')
    serializer_class = EventDetailSerializer


@api_view(['GET'])
def event_options(request):
    """GET /api/events/options/"""
    from django.db.models import Count
    return Response({
        'success': True,
        'counts': Event.objects.filter(is_active=True).aggregate(
            total=Count('id'),
            featured=Count('id', filter=Q(is_featured=True)),
            free=Count('id', filter=Q(is_free=True)),
            upcoming=Count('id', filter=Q(start_date__gte=timezone.now().date())),
        ),
    })
