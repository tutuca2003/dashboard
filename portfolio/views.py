from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Stock
from bull import sheets_service
from datetime import datetime
import time
from django.core.paginator import Paginator # Importante
from django.db.models import Q

@staff_member_required
def update_stock_price(request, pk):
    """
    ESTA VISTA AHORA SOLO "LEE". 
    El registro ya debería existir en el Excel gracias a las Signals.
    """
    stock = get_object_or_404(Stock, pk=pk)
    
    try:
        sheet = sheets_service.conectar_sheet()
        simbolo = stock.symbol.upper()
        
        # 1. Buscamos la fila (ya debería estar ahí)
        try:
            celda = sheet.find(simbolo)
            fila = celda.row
        except:
            # Si por alguna razón no está, la creamos rápido
            fila = len(sheet.col_values(1)) + 1
            sheet.update_acell(f'A{fila}', simbolo)
            sheet.update_acell(f'B{fila}', f'=GOOGLEFINANCE("{simbolo}"; "price")')
            sheet.update_acell(f'C{fila}', f'=GOOGLEFINANCE("{simbolo}"; "name")')

        # 2. Reintento de lectura (esperamos a que Google Finance responda)
        # Hacemos hasta 2 intentos para no ralentizar la web
        for i in range(2):
            datos_fila = sheet.row_values(fila)
            
            # Si la columna B (Precio) y C (Nombre) tienen datos reales, procesamos
            if len(datos_fila) > 2 and datos_fila[1] and datos_fila[2] and datos_fila[2] != "#N/A":
                # Guardar Precio
                try:
                    stock.price = float(datos_fila[1].replace(',', '.'))
                except:
                    pass
                
                # Guardar Nombre
                stock.name = datos_fila[2]
                stock.save()
                break
            
            # Si no, esperamos un poco y reintentamos
            time.sleep(1)

        print(f"✅ Dashboard sincronizado para {simbolo}")

    except Exception as e:
        print(f"🔴 Error al actualizar desde el Dashboard: {e}")
    
    return redirect('dashboard')
'''
@staff_member_required
def dashboard(request):
    """
    Vista principal con filtros.
    """
    stocks = Stock.objects.all().order_by('symbol')

    # Lógica de filtros
    strategy = request.GET.get('strategy')
    trade_status = request.GET.get('trade_status')
    analyzed = request.GET.get('analyzed')

    if strategy:
        stocks = stocks.filter(strategy=strategy)
    if trade_status:
        stocks = stocks.filter(trade_status=trade_status)
    if analyzed in ['true', 'false']:
        stocks = stocks.filter(analyzed=(analyzed == 'true'))

    return render(request, "dashboard.html", {
        "stocks": stocks,
        "current_strategy": strategy,
        "current_trade_status": trade_status,
        "current_analyzed": analyzed,
    })'''

from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Asegurate de importar tu modelo Stock

@login_required # O @staff_member_required según prefieras
def dashboard(request):
    """
    Vista principal: Filtra por Plataformas (OR) y por Estado (AND).
    """
    stocks = Stock.objects.all().order_by('symbol')

    # 1. Capturar Parámetros
    f_xtb = request.GET.get('xtb') == 'true'
    f_bmt = request.GET.get('bmt') == 'true'
    f_qut = request.GET.get('qut') == 'true'
    f_status = request.GET.get('status')

    # 2. Aplicar Filtro de Plataformas (Si hay alguna seleccionada)
    if f_xtb or f_bmt or f_qut:
        query_plataformas = Q()
        if f_xtb: query_plataformas |= Q(xtb=True)
        if f_bmt: query_plataformas |= Q(bmt=True)
        if f_qut: query_plataformas |= Q(qut=True)
        stocks = stocks.filter(query_plataformas)

    # 3. Aplicar Filtro de Estado (Si se eligió uno)
    if f_status in ['0', '1', '2', '3']:
        stocks = stocks.filter(trade_status=f_status)

      # --- Lógica de Paginación ---
    paginator = Paginator(stocks, 12) # 14 acciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "dashboard.html", {
        "stocks": page_obj, # Ahora pasamos el objeto de página
        "current_xtb": f_xtb,
        "current_bmt": f_bmt,
        "current_qut": f_qut,
        "current_status": f_status,
        "current_params": request.GET.urlencode(),
    })




