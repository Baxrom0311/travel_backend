from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .models import UserFavorite
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    MyTokenObtainPairSerializer,
    ChangePasswordSerializer,
    UserFavoriteSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'register'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'success': True,
                    'message': "Ro'yxatdan o'tdingiz! Endi kirishingiz mumkin.",
                    'user': UserSerializer(user, context={'request': request}).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class MyTokenObtainPairView(TokenObtainPairView):
    """POST /api/auth/login/ - returns access + refresh tokens + user info."""
    serializer_class = MyTokenObtainPairSerializer
    throttle_scope = 'login'


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PUT/PATCH /api/auth/me/"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """POST /api/auth/change-password/"""
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = request.user
    if not user.check_password(serializer.validated_data['old_password']):
        return Response(
            {'success': False, 'error': "Eski parol noto'g'ri"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(serializer.validated_data['new_password'])
    user.save()
    return Response({'success': True, 'message': "Parol o'zgartirildi"})


# ============ FAVORITES (synced with backend) ============

class FavoriteListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/auth/favorites/"""
    serializer_class = UserFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserFavorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteDeleteView(generics.DestroyAPIView):
    """DELETE /api/auth/favorites/{id}/"""
    serializer_class = UserFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserFavorite.objects.filter(user=self.request.user)


VALID_FAVORITE_TYPES = {t[0] for t in UserFavorite.FAVORITE_TYPES}


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_favorite(request):
    """POST /api/auth/favorites/toggle/  { favorite_type, object_id }"""
    favorite_type = request.data.get('favorite_type')
    object_id = request.data.get('object_id')

    if not favorite_type or not object_id:
        return Response(
            {'success': False, 'error': 'favorite_type and object_id required'},
            status=400,
        )

    if favorite_type not in VALID_FAVORITE_TYPES:
        return Response(
            {'success': False, 'error': f"Invalid favorite_type. Must be one of: {', '.join(sorted(VALID_FAVORITE_TYPES))}"},
            status=400,
        )

    try:
        object_id = int(object_id)
    except (ValueError, TypeError):
        return Response({'success': False, 'error': 'object_id must be an integer'}, status=400)

    fav, created = UserFavorite.objects.get_or_create(
        user=request.user,
        favorite_type=favorite_type,
        object_id=object_id,
    )

    if not created:
        fav.delete()
        return Response({'success': True, 'action': 'removed'})

    return Response({'success': True, 'action': 'added'}, status=201)
