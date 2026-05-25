from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import logging

from hotels.models import ContactMessage
from .serializers import ContactMessageSerializer

logger = logging.getLogger(__name__)


class ContactCreateView(generics.CreateAPIView):
    """POST /api/contact/"""
    queryset = ContactMessage.objects.none()
    serializer_class = ContactMessageSerializer
    throttle_scope = 'contact'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            msg = serializer.save()
            self._send_notification(msg)
            return Response(
                {'success': True, 'message': 'Xabaringiz muvaffaqiyatli yuborildi!'},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _send_notification(self, msg):
        """Send email notification to admin (best-effort)."""
        try:
            send_mail(
                subject=f'[Visit Khorezm] Yangi xabar: {msg.name}',
                message=f'Ism: {msg.name}\nEmail: {msg.email}\n\n{msg.message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            logger.warning(f'Email notification failed: {e}')
