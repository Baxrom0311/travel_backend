from django.db import models


class NewsletterSubscription(models.Model):
    LANGUAGE_CHOICES = [
        ('uz', "O'zbek"),
        ('en', 'English'),
        ('ru', 'Русский'),
    ]

    email = models.EmailField(unique=True, verbose_name="Email")
    language = models.CharField(max_length=3, choices=LANGUAGE_CHOICES, default='uz')
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Obunachi"
        verbose_name_plural = "Obunachilar"
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
