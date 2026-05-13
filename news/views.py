from rest_framework import generics, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, Count

from utils.lang import LangMixin
from utils.query_params import reject_unknown_query_params
from .models import News
from .serializers import NewsListSerializer, NewsDetailSerializer


class NewsFilterSerializer(serializers.Serializer):
    featured = serializers.BooleanField(required=False)
    search = serializers.CharField(max_length=100, required=False)


class NewsListView(LangMixin, generics.ListAPIView):
    """GET /api/news/"""
    serializer_class = NewsListSerializer

    def get_queryset(self):
        qs = News.objects.filter(is_published=True).prefetch_related('images')
        reject_unknown_query_params(self.request.query_params, {'featured', 'search'})
        filters = NewsFilterSerializer(data=self.request.query_params.dict())
        filters.is_valid(raise_exception=True)
        params = filters.validated_data

        if params.get('featured'):
            qs = qs.filter(is_featured=True)
        if params.get('search'):
            s = params['search']
            qs = qs.filter(
                Q(title_uz__icontains=s) | Q(title_en__icontains=s) |
                Q(content_uz__icontains=s) | Q(excerpt_uz__icontains=s)
            )
        return qs


class NewsDetailView(LangMixin, generics.RetrieveAPIView):
    queryset = News.objects.prefetch_related('images')
    serializer_class = NewsDetailSerializer
    lookup_field = 'slug'


@api_view(['GET'])
def news_options(request):
    return Response({
        'success': True,
        'counts': News.objects.filter(is_published=True).aggregate(
            total=Count('id'),
            featured=Count('id', filter=Q(is_featured=True)),
        ),
    })
