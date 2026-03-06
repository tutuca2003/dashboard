from django.db import models

class Stock(models.Model):

    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    # Precio actual
    price = models.FloatField(default=0.0)

    # Fair values
    fv_simple = models.FloatField(default=0.0)
    fv_dcf = models.FloatField(default=0.0)
    fv_avg = models.FloatField(default=0.0)

    # ---- NUEVOS CAMPOS ----

    TRADE_STATUS = [
        ('none', 'Nada'),
        ('buy', 'Comprado (Long)'),
        ('sell', 'Vendido (Short)'),
    ]

    trade_status = models.CharField(
        max_length=10,
        choices=TRADE_STATUS,
        default='none'
    )

    trade_price = models.FloatField(null=True, blank=True)

    analyzed = models.BooleanField(default=False)

    notes = models.TextField(blank=True)

    alert_price = models.FloatField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    STRATEGY_CHOICES = [
        ('trading', 'Trading'),
        ('long_term', 'Cartera'),
    ]

    strategy = models.CharField(
        max_length=20,
        choices=STRATEGY_CHOICES,
        default='trading',
    )

    def __str__(self):
        return f"{self.symbol} - {self.name}"
    

