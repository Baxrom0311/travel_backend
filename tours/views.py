from rest_framework import generics, serializers
from django.db.models import Q
from utils.lang import LangMixin
from utils.cache import PublicCacheMixin
from utils.query_params import reject_unknown_query_params
from .models import Tour
from .serializers import TourListSerializer, TourDetailSerializer


TOUR_ORDERING_CHOICES = ['-is_featured', 'price', '-price', 'title_uz', '-title_uz', 'duration', '-duration']


class TourFilterSerializer(serializers.Serializer):
    ordering = serializers.ChoiceField(choices=TOUR_ORDERING_CHOICES, required=False)


class TourListView(PublicCacheMixin, LangMixin, generics.ListAPIView):
    serializer_class = TourListSerializer

    def get_queryset(self):
        qs = Tour.objects.filter(is_active=True).prefetch_related('images')
        reject_unknown_query_params(
            self.request.query_params,
            {'featured', 'search', 'difficulty', 'ordering'},
        )
        featured = self.request.query_params.get('featured')
        search = self.request.query_params.get('search')
        difficulty = self.request.query_params.get('difficulty')

        ordering = '-is_featured'
        filter_ser = TourFilterSerializer(data=self.request.query_params)
        filter_ser.is_valid(raise_exception=True)
        ordering = filter_ser.validated_data.get('ordering', '-is_featured')

        if featured == 'true': qs = qs.filter(is_featured=True)
        if difficulty: qs = qs.filter(difficulty=difficulty)
        if search:
            qs = qs.filter(
                Q(title_uz__icontains=search) | Q(title_en__icontains=search) |
                Q(title_ru__icontains=search) | Q(description_uz__icontains=search)
            )
        return qs.order_by(ordering)


class TourDetailView(LangMixin, generics.RetrieveAPIView):
    queryset = Tour.objects.prefetch_related('images')
    serializer_class = TourDetailSerializer
    lookup_field = 'slug'
