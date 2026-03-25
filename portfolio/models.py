import re
from django.db import models
from django.urls import reverse
from django.utils import timezone

class Stock(models.Model):
    # --- Identificación ---
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(
        max_length=255, 
        null=True,   
        blank=True,  
        verbose_name="Nombre de la empresa"
    )

    # --- Valores Financieros ---
    price = models.FloatField(default=0.0)
    fv = models.FloatField(default=0.0)

    # --- Estrategia (Referencias de Texto) ---
    long_stop = models.CharField(max_length=50, blank=True, null=True, verbose_name="Long Stop Loss")
    long_profit = models.CharField(max_length=50, blank=True, null=True, verbose_name="Long Take Profit")
    ref_long = models.CharField(max_length=100, blank=True, null=True, verbose_name="Referencia Long") # Agregado
    
    short_stop = models.CharField(max_length=50, blank=True, null=True, verbose_name="Short Stop Loss")
    short_profit = models.CharField(max_length=50, blank=True, null=True, verbose_name="Short Take Profit")
    ref_short = models.CharField(max_length=100, blank=True, null=True, verbose_name="Referencia Short") # Agregado

    # --- Estados de la Acción ---
    TRADE_STATUS = [
        ('0', 'EVALUAR'),
        ('1', 'OPERATIVA'),
        ('2', 'INACTIVA'),
        ('3', 'NUEVA'),
        ('sell', 'VENTA'),
    ]

    trade_status = models.CharField(
        max_length=10,
        choices=TRADE_STATUS,
        default='0'
    )

    fecha_inactivacion = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha para evaluar"
    )

    # --- Plataformas (Booleanos) ---
    bmt = models.BooleanField(default=False)
    xtb = models.BooleanField(default=False)
    qut = models.BooleanField(default=False)

    # --- Notas y Seguimiento ---
    Observaciones = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        fecha_hoy = timezone.now().strftime("%d/%m/%Y")
        formato_destacado = f"[{fecha_hoy}] >> "
        
        obs = self.Observaciones or ""
        ya_tiene_fecha = re.match(r'^\[\d{2}/\d{2}/\d{4}\]', obs)

        if not ya_tiene_fecha:
            self.Observaciones = f"{formato_destacado}{obs}"
        
        super().save(*args, **kwargs)

    def admin_url(self):
        return reverse('admin:portfolio_stock_change', args=[self.id])

    def __str__(self):
        return f"{self.symbol} - {self.name if self.name else ''}"