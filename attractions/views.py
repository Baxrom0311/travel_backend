from rest_framework import generics, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Q

from utils.lang import LangMixin
from utils.query_params import reject_unknown_query_params
from .models import Attraction
from .serializers import AttractionListSerializer, AttractionDetailSerializer


class AttractionFilterSerializer(serializers.Serializer):
    featured = serializers.BooleanField(required=False)
    search = serializers.CharField(max_length=100, required=False)


class AttractionListView(LangMixin, generics.ListAPIView):
    """GET /api/attractions/"""
    serializer_class = AttractionListSerializer

    def get_queryset(self):
        qs = Attraction.objects.prefetch_related('images').all()
        reject_unknown_query_params(self.request.query_params, {'featured', 'search'})
        filters = AttractionFilterSerializer(data=self.request.query_params.dict())
        filters.is_valid(raise_exception=True)
        params = filters.validated_data
        if 'featured' in params:
            qs = qs.filter(is_featured=params['featured'])
        if params.get('search'):
            s = params['search']
            qs = qs.filter(
                Q(name_uz__icontains=s) | Q(name_en__icontains=s) | Q(name_ru__icontains=s) |
                Q(description_uz__icontains=s)
            )
        return qs.order_by('order')


class AttractionDetailView(LangMixin, generics.RetrieveAPIView):
    """GET /api/attractions/{id}/"""
    queryset = Attraction.objects.prefetch_related('images')
    serializer_class = AttractionDetailSerializer


@api_view(['GET'])
def attraction_options(request):
    counts = Attraction.objects.aggregate(
        total=Count('id'),
        featured=Count('id', filter=Q(is_featured=True)),
    )
    return Response({
        'success': True,
        'counts': counts,
    })


@api_view(['GET'])
def attraction_related(request, pk: int):
    """GET /api/attractions/{id}/related/ — shunga o'xshash joylar."""
    try:
        current = Attraction.objects.get(pk=pk)
    except Attraction.DoesNotExist:
        return Response({'success': False, 'error': 'Not found'}, status=404)

    related = Attraction.objects.prefetch_related('images') \
        .exclude(pk=pk).order_by('-is_featured', 'order')[:4]

    lang = request.query_params.get('lang', 'uz')
    return Response({
        'success': True,
        'data': AttractionListSerializer(
            related, many=True, context={'request': request, 'lang': lang}
        ).data,
    })
