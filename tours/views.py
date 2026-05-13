from rest_framework import generics
from django.db.models import Q
from utils.lang import LangMixin
from .models import Tour
from .serializers import TourListSerializer, TourDetailSerializer


class TourListView(LangMixin, generics.ListAPIView):
    serializer_class = TourListSerializer

    def get_queryset(self):
        qs = Tour.objects.filter(is_active=True).prefetch_related('images')
        featured = self.request.query_params.get('featured')
        search = self.request.query_params.get('search')
        difficulty = self.request.query_params.get('difficulty')
        
        if featured == 'true': qs = qs.filter(is_featured=True)
        if difficulty: qs = qs.filter(difficulty=difficulty)
        if search:
            qs = qs.filter(Q(title_uz__icontains=search) | Q(description_uz__icontains=search))
        return qs


class TourDetailView(LangMixin, generics.RetrieveAPIView):
    queryset = Tour.objects.prefetch_related('images')
    serializer_class = TourDetailSerializer
    lookup_field = 'slug'
