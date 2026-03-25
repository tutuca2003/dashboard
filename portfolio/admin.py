from django.contrib import admin
from .models import Stock
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import redirect

class StockAdmin(admin.ModelAdmin):
    # Agregamos los campos de parada y profit a la vista de lista para verlos rápido
    list_display = ('symbol', 'price', 'fv', 'long_stop', 'long_profit', 'short_stop', 'short_profit', 'goto_dashboard_link')
    
    # Buscador por símbolo o nombre
    search_fields = ('symbol', 'name')

    # Organización del formulario de edición
    fieldsets = (
        ('Identificación', {
            'fields': ('symbol', 'name', 'trade_status', 'fecha_inactivacion')
        }),
        ('Valores Financieros', {
            'fields': ('price', 'fv')
        }),
        ('Estrategia LONG', {
            'fields': ( 'ref_long', 'long_stop', 'long_profit'),
            #'classes': ('collapse',), # Esto lo hace colapsable si querés (opcional)
        }),
        ('Estrategia SHORT', {
            'fields': ( 'ref_short','short_stop', 'short_profit'),
        }),
        ('Plataformas y Notas', {
            'fields': ('bmt', 'xtb', 'qut', 'Observaciones')
        }),
    )

    def goto_dashboard_link(self, obj):
        return format_html('<a class="button" style="background-color: #417690; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;" href="{}">🏠 Dashboard</a>', '/')
    
    goto_dashboard_link.short_description = 'Ir al Inicio'

    def response_change(self, request, obj):
        """ Redirige al dashboard después de guardar cambios """
        return redirect('dashboard') 

    def response_add(self, request, obj, post_url_continue=None):
        """ Redirige al dashboard también después de crear una acción nueva """
        return redirect('dashboard')

admin.site.register(Stock, StockAdmin)



    