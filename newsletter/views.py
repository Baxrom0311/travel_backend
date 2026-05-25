from rest_framework import serializers, status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from django.utils import timezone
from .models import NewsletterSubscription


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['email', 'language']


class NewsletterThrottle(ScopedRateThrottle):
    scope = 'newsletter'


@api_view(['POST'])
@throttle_classes([NewsletterThrottle])
def subscribe(request):
    """POST /api/newsletter/subscribe/"""
    serializer = SubscribeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    email = serializer.validated_data['email']
    language = serializer.validated_data.get('language', 'uz')

    sub, created = NewsletterSubscription.objects.get_or_create(
        email=email,
        defaults={'language': language, 'is_active': True},
    )
    if not created:
        if not sub.is_active:
            sub.is_active = True
            sub.unsubscribed_at = None
            sub.save()
            return Response({'success': True, 'message': 'Obunangiz qaytadan faollashtirildi'})
        return Response({'success': True, 'message': 'Siz allaqachon obuna bo\'lgansiz'})

    return Response(
        {'success': True, 'message': 'Muvaffaqiyatli obuna bo\'ldingiz!'},
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
def unsubscribe(request):
    """POST /api/newsletter/unsubscribe/"""
    email = request.data.get('email')
    if not email:
        return Response({'success': False, 'error': 'Email kerak'}, status=400)
    
    try:
        sub = NewsletterSubscription.objects.get(email=email)
        sub.is_active = False
        sub.unsubscribed_at = timezone.now()
        sub.save()
        return Response({'success': True, 'message': 'Obunangiz bekor qilindi'})
    except NewsletterSubscription.DoesNotExist:
        return Response({'success': False, 'error': 'Email topilmadi'}, status=404)
