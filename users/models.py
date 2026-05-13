"""
Custom User model with email login.
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Email-based user manager."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email kiritilishi shart')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model with email as USERNAME_FIELD."""
    
    LANGUAGE_CHOICES = [
        ('uz', "O'zbek"),
        ('en', 'English'),
        ('ru', 'Русский'),
    ]

    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    
    # Profile
    first_name = models.CharField(max_length=100, blank=True, verbose_name="Ism")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Familiya")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    country = models.CharField(max_length=80, blank=True, verbose_name="Davlat")
    bio = models.TextField(max_length=500, blank=True, verbose_name="O'zi haqida")
    language = models.CharField(max_length=3, choices=LANGUAGE_CHOICES, default='uz')
    
    # Stats
    is_verified = models.BooleanField(default=False, verbose_name="Email tasdiqlangan")
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name or self.email.split('@')[0]


class UserFavorite(models.Model):
    """User's favorite items (hotels, attractions, restaurants, tours, events)."""
    FAVORITE_TYPES = [
        ('hotel', 'Hotel'),
        ('attraction', 'Attraction'),
        ('restaurant', 'Restaurant'),
        ('tour', 'Tour'),
        ('event', 'Event'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    favorite_type = models.CharField(max_length=20, choices=FAVORITE_TYPES)
    object_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sevimli"
        verbose_name_plural = "Sevimlilar"
        ordering = ['-created_at']
        unique_together = [['user', 'favorite_type', 'object_id']]
        indexes = [
            models.Index(fields=['user', 'favorite_type']),
        ]

    def __str__(self):
        return f"{self.user.email} — {self.favorite_type}#{self.object_id}"
