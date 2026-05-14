from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Testimonial
from .serializers import TestimonialSerializer


@api_view(['GET'])
def testimonials_list(request):
    """Faol sharhlar ro'yxati."""
    qs = Testimonial.objects.filter(is_active=True).order_by('order', '-created_at')
    serializer = TestimonialSerializer(qs, many=True)
    return Response(serializer.data)
