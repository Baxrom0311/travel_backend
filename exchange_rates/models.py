from django.db import models


class ExchangeRate(models.Model):
    currency = models.CharField(max_length=3, unique=True)
    rate_to_uzs = models.DecimalField(max_digits=12, decimal_places=4, help_text="1 unit of currency = X UZS")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['currency']

    def __str__(self):
        return f"{self.currency}: {self.rate_to_uzs} UZS"
