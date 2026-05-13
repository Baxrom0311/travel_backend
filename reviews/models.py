from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Generic reviews for any model (Hotel, Attraction, Restaurant, Tour).
    """
    # Polymorphic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Reviewer info
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=80, blank=True, verbose_name="Davlat")

    # Content
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Reyting (1-5)"
    )
    title = models.CharField(max_length=200, verbose_name="Sarlavha", blank=True)
    comment = models.TextField(verbose_name="Fikr")

    is_approved = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['is_approved', '-created_at']),
        ]

    def __str__(self):
        return f"{self.name} — {self.rating}★"
