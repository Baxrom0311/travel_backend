from rest_framework import generics, status
from rest_framework.response import Response
from hotels.models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactCreateView(generics.CreateAPIView):
    """POST /api/contact/"""
    queryset = ContactMessage.objects.none()
    serializer_class = ContactMessageSerializer
    throttle_scope = 'contact'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'success': True, 'message': 'Xabaringiz muvaffaqiyatli yuborildi!'},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
