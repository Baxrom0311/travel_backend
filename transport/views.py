from rest_framework import generics, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, inline_serializer
from django.db.models import Max, Min
from utils.lang import LangMixin
from utils.query_params import reject_unknown_query_params
from .models import TransportRoute
from .serializers import TransportFilterSerializer, TransportRouteSerializer


@extend_schema(parameters=[TransportFilterSerializer])
class TransportListView(LangMixin, generics.ListAPIView):
    """
    GET /api/transport/
    Query params:
      type : taxi | bus | train
      lang : uz | en | ru  (default: uz)
    """
    serializer_class = TransportRouteSerializer

    def get_queryset(self):
        qs = TransportRoute.objects.all()
        reject_unknown_query_params(self.request.query_params, {'type'})
        filters = TransportFilterSerializer(data=self.request.query_params.dict())
        filters.is_valid(raise_exception=True)
        route_type = filters.validated_data.get('type')
        if route_type:
            qs = qs.filter(transport_type=route_type)
        return qs


class TransportDetailView(LangMixin, generics.RetrieveAPIView):
    """GET /api/transport/{id}/   ?lang=uz|en|ru"""
    queryset = TransportRoute.objects.all()
    serializer_class = TransportRouteSerializer


@extend_schema(
    responses=inline_serializer(
        name='TransportOptionsResponse',
        fields={
            'success': serializers.BooleanField(),
            'types': serializers.ListField(child=serializers.DictField()),
            'badge_styles': serializers.ListField(child=serializers.DictField()),
            'price': serializers.DictField(child=serializers.IntegerField(allow_null=True)),
            'duration': serializers.DictField(child=serializers.IntegerField(allow_null=True)),
        },
    )
)
@api_view(['GET'])
def transport_options(request):
    """GET /api/transport/options/ — Frontend filterlari uchun metadata"""
    reject_unknown_query_params(request.query_params, set())
    price = TransportRoute.objects.aggregate(min=Min('price_min'), max=Max('price_max'))
    duration = TransportRoute.objects.aggregate(min=Min('duration_min'), max=Max('duration_max'))

    return Response({
        'success': True,
        'types': [
            {'value': value, 'label': label}
            for value, label in TransportRoute.TYPE_CHOICES
        ],
        'badge_styles': [
            {'value': value, 'label': label}
            for value, label in TransportRoute.BADGE_STYLE_CHOICES
        ],
        'price': price,
        'duration': duration,
    })
