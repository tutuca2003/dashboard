from django.contrib import admin
from .models import Stock
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import redirect

class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'price', 'fv', 'goto_dashboard_link')

    def goto_dashboard_link(self, obj):
        return format_html('<a class="button" href="{}">🏠 Ir al Dashboard</a>', '/')
    goto_dashboard_link.short_description = 'Dashboard'
    goto_dashboard_link.allow_tags = True
    
    def response_change(self, request, obj):
        """
        Después de guardar un objeto, redirige al dashboard en lugar
        de quedarse en la página de edición.
        """
        return redirect('dashboard')  # 'dashboard' es el nombre de tu URL

admin.site.register(Stock, StockAdmin)





    