from django.db import models


class News(models.Model):
    title_uz = models.CharField(max_length=200, verbose_name="Sarlavha (UZ)")
    title_en = models.CharField(max_length=200, verbose_name="Sarlavha (EN)", blank=True)
    title_ru = models.CharField(max_length=200, verbose_name="Sarlavha (RU)", blank=True)
    
    slug = models.SlugField(unique=True, verbose_name="URL slug")
    
    excerpt_uz = models.TextField(verbose_name="Qisqa tavsif (UZ)", max_length=300)
    excerpt_en = models.TextField(verbose_name="Qisqa tavsif (EN)", max_length=300, blank=True)
    excerpt_ru = models.TextField(verbose_name="Qisqa tavsif (RU)", max_length=300, blank=True)
    
    content_uz = models.TextField(verbose_name="To'liq matn (UZ)")
    content_en = models.TextField(verbose_name="To'liq matn (EN)", blank=True)
    content_ru = models.TextField(verbose_name="To'liq matn (RU)", blank=True)
    
    cover_image = models.ImageField(upload_to='news/', verbose_name="Asosiy rasm")
    
    author = models.CharField(max_length=100, verbose_name="Muallif", blank=True)
    
    is_featured = models.BooleanField(default=False, verbose_name="Asosiy")
    is_published = models.BooleanField(default=True, verbose_name="Chop etilgan")
    
    published_at = models.DateTimeField(verbose_name="Chop etilgan sana")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-published_at']

    def __str__(self):
        return self.title_uz


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
