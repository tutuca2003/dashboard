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

    # --- Estados de la Acción ---
    TRADE_STATUS = [
        ('0', 'EVALUAR'),
        ('1', 'OPERATIVA'),
        ('2', 'INACTIVA'),
        ('3', 'NUEVA'),  # Estado para el botón azul
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
        """
        Lógica de Guardado: 
        1. Estampa la fecha con formato destacado [dd/mm/aaaa] >> al inicio.
        2. Si ya detecta una fecha al inicio, no hace nada para evitar duplicados.
        """
        fecha_hoy = timezone.now().strftime("%d/%m/%Y")
        # Formato visual que se destaca del resto del texto
        formato_destacado = f"[{fecha_hoy}] >> "

        # Usamos una expresión regular para detectar si ya hay una fecha al inicio.
        # r'^\[\d{2}/\d{2}/\d{4}\]' busca exactamente "[dos-números/dos-números/cuatro-números]"
        ya_tiene_fecha = re.match(r'^\[\d{2}/\d{2}/\d{4}\]', self.Observaciones)

        if not ya_tiene_fecha:
            # Si el campo está vacío o no tiene fecha, la agregamos
            # Esto une la fecha nueva con lo que ya estaba escrito (si hubiera algo)
            self.Observaciones = f"{formato_destacado}{self.Observaciones}"
        
        # Guardamos el modelo
        super().save(*args, **kwargs)

    def admin_url(self):
        """Genera el enlace directo para editar esta acción en el Admin de Django"""
        return reverse('admin:portfolio_stock_change', args=[self.id])

    def __str__(self):
        return f"{self.symbol} - {self.name if self.name else ''}"