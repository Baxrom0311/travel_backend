from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Count
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


MODEL_MAP = {
    'hotel': ('hotels', 'hotel'),
    'attraction': ('attractions', 'attraction'),
    'restaurant': ('restaurants', 'restaurant'),
    'tour': ('tours', 'tour'),
}


class ReviewCreateView(generics.CreateAPIView):
    """POST /api/reviews/"""
    serializer_class = ReviewCreateSerializer
    queryset = Review.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'success': True, 'message': 'Fikringiz uchun rahmat! Tasdiqlangandan keyin chop etiladi.'},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['GET'])
def list_reviews(request, target_type, target_id):
    """GET /api/reviews/{target_type}/{target_id}/"""
    if target_type not in MODEL_MAP:
        return Response({'success': False, 'error': 'Invalid target_type'}, status=400)

    app_label, model_name = MODEL_MAP[target_type]
    try:
        ct = ContentType.objects.get(app_label=app_label, model=model_name)
    except ContentType.DoesNotExist:
        return Response({'success': False, 'error': 'Model not found'}, status=404)

    reviews = Review.objects.filter(
        content_type=ct,
        object_id=target_id,
        is_approved=True
    )
    
    stats = reviews.aggregate(
        avg_rating=Avg('rating'),
        total=Count('id'),
    )

    return Response({
        'success': True,
        'stats': {
            'avg_rating': round(stats['avg_rating'] or 0, 1),
            'total': stats['total'],
        },
        'results': ReviewSerializer(reviews[:20], many=True).data,
    })
