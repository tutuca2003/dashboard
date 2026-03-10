from django.db import models
from django.urls import reverse

class Stock(models.Model):

    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    # Precio actual
    price = models.FloatField(default=0.0)

    # Fair values
    fv = models.FloatField(default=0.0)
    #fv_dcf = models.FloatField(default=0.0)
    #fv_avg = models.FloatField(default=0.0)

    # ---- NUEVOS CAMPOS ----

    TRADE_STATUS = [
        ('none', 'Esperar'),
        ('buy', 'Comprado'),
        ('sell', 'Vendido'),
    ]

    trade_status = models.CharField(
        max_length=10,
        choices=TRADE_STATUS,
        default='none'
    )

    #trade_price = models.FloatField(null=True, blank=True)

    analyzed = models.BooleanField(default=False)

    Observaciones = models.TextField(blank=True)

    #alert_price = models.FloatField(null=True, blank=True)

    #updated_at = models.DateTimeField(auto_now=True)

    STRATEGY_CHOICES = [
        ('xt', 'XTB'),
        ('bm', 'B M'),
        ('qu', 'Quant'),
    ]

    strategy = models.CharField(
        max_length=20,
        choices=STRATEGY_CHOICES,
        default='trading',
    )

    def admin_url(self):
        return reverse('admin:portfolio_stock_change', args=[self.id])


    def __str__(self):
        return f"{self.symbol} - {self.name}"
    

