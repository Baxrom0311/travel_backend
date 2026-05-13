from django.db import models


class Event(models.Model):
    title_uz = models.CharField(max_length=200, verbose_name="Sarlavha (UZ)")
    title_en = models.CharField(max_length=200, verbose_name="Sarlavha (EN)", blank=True)
    title_ru = models.CharField(max_length=200, verbose_name="Sarlavha (RU)", blank=True)
    
    description_uz = models.TextField(verbose_name="Tavsif (UZ)")
    description_en = models.TextField(verbose_name="Tavsif (EN)", blank=True)
    description_ru = models.TextField(verbose_name="Tavsif (RU)", blank=True)
    
    cover_image = models.ImageField(upload_to='events/', verbose_name="Asosiy rasm")
    
    # Sana va vaqt
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    end_date = models.DateField(verbose_name="Tugash sanasi", blank=True, null=True)
    start_time = models.TimeField(verbose_name="Boshlanish vaqti", blank=True, null=True)
    
    # Joylashuv
    location_uz = models.CharField(max_length=200, verbose_name="Manzil (UZ)")
    location_en = models.CharField(max_length=200, verbose_name="Manzil (EN)", blank=True)
    location_ru = models.CharField(max_length=200, verbose_name="Manzil (RU)", blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    # Narx
    is_free = models.BooleanField(default=True, verbose_name="Bepul")
    price = models.PositiveIntegerField(default=0, verbose_name="Narx (UZS)")
    
    is_featured = models.BooleanField(default=False, verbose_name="Asosiy")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tadbir"
        verbose_name_plural = "Tadbirlar"
        ordering = ['start_date']

    def __str__(self):
        return self.title_uz


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='events/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
