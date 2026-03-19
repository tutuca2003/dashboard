from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Stock
from bull import sheets_service
from datetime import datetime

@receiver(post_save, sender=Stock)
def sync_to_sheets(sender, instance, created, **kwargs):
    """
    Cada vez que guardas en el Admin, esto se ejecuta solo.
    """
    try:
        sheet = sheets_service.conectar_sheet()
        simbolo = instance.symbol.upper()
        
        # Buscar fila o crear nueva
        try:
            celda = sheet.find(simbolo)
            fila = celda.row
        except:
            fila = len(sheet.col_values(1)) + 1

        ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Escribimos TODO de una vez al guardar
        sheet.update_acell(f'A{fila}', simbolo)
        sheet.update_acell(f'B{fila}', f'=GOOGLEFINANCE("{simbolo}"; "price")')
        sheet.update_acell(f'C{fila}', f'=GOOGLEFINANCE("{simbolo}"; "name")')
        
        # Si tienes estrategia o fair value, los mandamos también
        '''
        if instance.strategy:
            sheet.update_acell(f'E{fila}', instance.get_strategy_display())
        
        sheet.update_acell(f'I{fila}', f'Auto-Sync: {ahora}')
        '''
        print(f"⚡ Señal: {simbolo} sincronizado automáticamente con Excel.")
    except Exception as e:
        print(f"❌ Error en señal: {e}")