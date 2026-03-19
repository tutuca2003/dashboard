from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

class Stock(models.Model):

    symbol = models.CharField(max_length=10, unique=True)
    #name = models.CharField(max_length=100)

    name = models.CharField(
        max_length=255, 
        null=True,   # Permite que en SQL se guarde como vacío
        blank=True,  # Permite que en el Admin no te lo pida como obligatorio
        verbose_name="Nombre de la empresa"
    )

    # Precio actual
    price = models.FloatField(default=0.0)

    # Fair values
    fv = models.FloatField(default=0.0)
    #fv_dcf = models.FloatField(default=0.0)
    #fv_avg = models.FloatField(default=0.0)

    # ---- NUEVOS CAMPOS ----

    TRADE_STATUS = [
        ('0', 'EVALUAR'),
        ('1', 'OPERATIVA'),
        ('2', 'INACTIVA'),
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

    #trade_price = models.FloatField(null=True, blank=True)

    bmt = models.BooleanField(default=False)
    xtb = models.BooleanField(default=False)
    qut = models.BooleanField(default=False)

    Observaciones = models.TextField(blank=True)

    def clean(self):
        # Ejecuta la validación base
        super().clean()
        
        # Lógica: Si ninguno es True, lanzamos error
        if not self.bmt and not self.xtb and not self.qut:
            raise ValidationError(
                "Debes seleccionar al menos una plataforma (BMT, XTB o QUT)."
            )

    def save(self, *args, **kwargs):
        # Es buena práctica llamar a full_clean() antes de save() 
        # para que las validaciones de clean() se ejecuten siempre
        self.full_clean()
        super().save(*args, **kwargs)  

    def admin_url(self):
        return reverse('admin:portfolio_stock_change', args=[self.id])


    def __str__(self):
        return f"{self.symbol} - {self.name}"
    

