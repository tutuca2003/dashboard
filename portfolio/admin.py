from django.contrib import admin
from .models import Stock
from django.urls import reverse
from django.utils.html import format_html

'''
class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'strategy', 'price', 'fv_simple', 'fv_dcf', 'fv_avg')

admin.site.register(Stock, StockAdmin)
'''


class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'strategy', 'price', 'fv_simple', 'fv_dcf', 'fv_avg', 'goto_dashboard_link')

    def goto_dashboard_link(self, obj):
        return format_html('<a class="button" href="{}">🏠 Ir al Dashboard</a>', '/')
    goto_dashboard_link.short_description = 'Dashboard'
    goto_dashboard_link.allow_tags = True

admin.site.register(Stock, StockAdmin)